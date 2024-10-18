from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from pubkeys import pubkeydictionary
import paho.mqtt.client as mqtt  

# Petición del mensaje
mensaje = input("Escribe aquí tu mensaje: ").encode("ascii")

# Preguntar al usuario si desea ser anónimo
anonymous = input("Si desea enviar su mensaje de manera anónima presione 's' (No? pulse cualquier tecla): ")

# Obtener el diccionario de claves públicas desde pubkeydictionary
publicKeys = pubkeydictionary 

# Bucle para pedir la ruta hasta que todas las claves públicas sean válidas
while True:
    route = input("Introduce aquí la ruta deseada, separada por comas (','): ")

    rutaUsuario = route.split(',')  

    # Crear una lista para almacenar las claves públicas correspondientes a los saltos
    publicKeysOrder = []
    rutas_invalidas = False

    # Recorrer el array rutaUsuario y obtener el valor de publicKeys (clave pública)
    for hop in rutaUsuario:
        if hop in publicKeys:
            clave_publica = 'ssh-rsa ' + publicKeys[hop]  
            publicKeysOrder.append(clave_publica)  
        else:
            print(f"El salto '{hop}' no tiene una clave pública en el diccionario.")
            rutas_invalidas = True  

    # Si no hay ningún salto inválido, salir del bucle
    if not rutas_invalidas:
        break 

# Definir el ID según la peticion del usuario de ser anonimo
if anonymous == "s":
    sender_id = b"none"
else:
    sender_id = b"lgm"

# Función para formatear el ID a 5 bytes
def normalizado_Id(id_str: str):
    return b'\x00' * (5 - len(id_str)) + id_str.encode('ascii')

def concatenado_end_id_mensaje(end: bytes, sender_id: bytes, mensaje: bytes):
    end_padded = b'\x00' * (5 - len(end)) + end
    sender_id_padded = b'\x00' * (5 - len(sender_id)) + sender_id
    result = end_padded + sender_id_padded + mensaje

    # Verificación de tipo bytes
    if not isinstance(result, bytes):
        raise TypeError("El valor debe ser de tipo 'bytes'")
    
    return result

# Fuera del bucle, ciframos el mensaje con la clave simétrica del destinatario
key_destinatario = AESGCM.generate_key(bit_length=128)
aesgcm_destinatario = AESGCM(key_destinatario)

# Ciframos el mensaje original con la clave simétrica del destinatario
end = b'end'
concatenado = concatenado_end_id_mensaje(end, sender_id, mensaje)
final_result = aesgcm_destinatario.encrypt(key_destinatario, concatenado, None)

# Cifrar la clave simétrica del destinatario con su clave pública
clave_publica_destinatario_str = publicKeysOrder[-1]
clave_publica_destinatario = serialization.load_ssh_public_key(
    clave_publica_destinatario_str.encode('ascii'), backend=default_backend()
)
encrypted_key_destinatario = clave_publica_destinatario.encrypt(
    key_destinatario,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Si solo hay un salto, no ejecutamos el bucle
if len(rutaUsuario) == 1:
    # Solo concatenamos la clave simétrica cifrada y el mensaje cifrado, sin agregar ID
    final_result = encrypted_key_destinatario + final_result
    print(f"\nResultado sin ID (un solo salto): {final_result.hex()}")
else:
    # Concatenar el ID del destinatario si hay más de un salto
    final_result = normalizado_Id(rutaUsuario[-1]) + encrypted_key_destinatario + final_result
    

    # Iniciar el bucle para los demás saltos, excepto el destinatario
    for i in range(len(rutaUsuario) - 2, -1, -1):  # Comenzamos desde el penúltimo salto hacia el primero
        hop_actual = rutaUsuario[i]  # El salto actual
        hop_siguiente = rutaUsuario[i + 1]  # El siguiente salto en la ruta

        # Generar una nueva clave simétrica para este salto
        new_key = AESGCM.generate_key(bit_length=128)
        aesgcm = AESGCM(new_key)
        

        # Cifrar el resultado del salto anterior (final_result) con la nueva clave simétrica
        final_result = aesgcm.encrypt(new_key, final_result, None)  # Usamos new_key como nonce
        

        # Obtener la clave pública del salto actual
        clave_publica_hop_str = publicKeysOrder[i]  # Tomamos la clave pública del salto actual
        

        # Cargar la clave pública del salto actual (hop_actual)
        try:
            clave_publica_hop = serialization.load_ssh_public_key(
                clave_publica_hop_str.encode('ascii'), backend=default_backend()
            )
        except ValueError as e:
            print(f"Error al cargar la clave pública del salto '{hop_actual}': {e}")
            break

        # Cifrar la nueva clave simétrica con la clave pública del salto actual (hop_actual)
        encrypted_key = clave_publica_hop.encrypt(
            new_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        

        # Concatenar el ID del siguiente salto con la clave simétrica cifrada y el resultado cifrado
        if i > 0:
            final_result = normalizado_Id(hop_actual) + encrypted_key + final_result
          
        else:
            # En la última iteración (primer salto en la ruta), no concatenamos el ID
            final_result = encrypted_key + final_result
            

# Configuración del servidor MQTT
MQTT_HOST = "18.100.158.114"  # Dirección IP del servidor MQTT
MQTT_PORT = 1883
MQTT_USER = "sinf"  # Usuario del servidor MQTT
MQTT_PASSWORD = "HkxNtvLB3GC5GQRUWfsA"  # Contraseña para el servidor MQTT

# Función para enviar el paquete al servidor MQTT
def enviar_a_mqtt(paquete, topic):
    client = mqtt.Client()  # Crear el cliente MQTT
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)  # Configurar credenciales de usuario y contraseña
    client.connect(MQTT_HOST, MQTT_PORT, 60)  # Conectar al servidor MQTT
    client.publish(topic, paquete)  # Publicar el paquete en el tópico dinámico
    client.disconnect()  # Desconectar del servidor
    print(f"Paquete enviado al servidor MQTT en el tópico {topic}.")

enviar_a_mqtt(final_result, rutaUsuario[0])

# Imprimir el resultado final cifrado
print(f"\nMensaje final cifrado en todas las capas: {final_result}")

