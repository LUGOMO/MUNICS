import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Configuración del servidor MQTT
MQTT_HOST = "18.100.158.114"  # Dirección IP del servidor MQTT
MQTT_PORT = 1883
MQTT_USER = "sinf"  # Usuario del servidor MQTT
MQTT_PASSWORD = "HkxNtvLB3GC5GQRUWfsA"  # Contraseña para el servidor MQTT
TOPIC = "lgm"  # Tópico al que nos suscribimos inicialmente

# Ruta de la clave privada (en formato OpenSSH)
private_key_path = r"E:\MUNICS\SI\CLAVES FINAL\LGM"

# Cargar la clave privada del destinatario (LGM)
with open(private_key_path, "rb") as key_file:
    private_key = serialization.load_ssh_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Función que se llama cuando se recibe un mensaje en el tópico
def on_message(client, userdata, message):
    paquete = message.payload  # Mensaje recibido como paquete en formato binario
    print(f"Mensaje recibido en el tópico {message.topic}: {paquete.hex()}")

    # Paquete 1 será la clave simétrica cifrada, paquete 2 será el mensaje cifrado con la clave simétrica
    paquete1 = paquete[:256]
    paquete2 = paquete[256:]
    
    try:
        # Desencriptar los primeros 256 bytes con la clave privada para obtener la clave simétrica
        ksimetrica = private_key.decrypt(
            paquete1,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Usar la clave simétrica desencriptada para desencriptar el resto del mensaje
        aesgcm = AESGCM(ksimetrica)
        nonce = ksimetrica  # En este caso nonce = ksimetrica
        mensaje_desencriptado = aesgcm.decrypt(nonce, paquete2, None)

        print("Mensaje desencriptado exitosamente.")

        # Verificación si los primeros 5 bytes son '\x00\x00end'
        if mensaje_desencriptado[:5] == b'\x00\x00end':
            print("El mensaje es para ti.")
            mensaje_desencriptado = mensaje_desencriptado[5:]  # Remover los primeros 5 bytes ('\x00\x00end')
            
            # Leer los siguientes 5 bytes y extraer el ID remitente
            id_remitente = mensaje_desencriptado[:5].decode('ascii').strip('\x00')
            print(f"El paquete fue enviado por: {id_remitente}")

            # El resto del mensaje
            mensaje_final = mensaje_desencriptado[5:].decode('ascii')
            print(f"El mensaje es: {mensaje_final}")

        else:
            # Extraer el siguiente topic desde los primeros 5 bytes (ID del siguiente salto)
            siguiente_topic = mensaje_desencriptado[:5].decode('ascii').strip('\x00')
            print(f"El mensaje no es para ti. Reenviando al siguiente tópico: {siguiente_topic}")

            # Eliminar los primeros 5 bytes (ID del destinatario) y reenviar el mensaje al nuevo topic
            mensaje_reenviar = mensaje_desencriptado[5:]
            
            # Enviar el mensaje al siguiente salto del servidor MQTT
            enviar_a_mqtt(mensaje_reenviar, siguiente_topic)
            print(f"Mensaje reenviado al siguiente salto (tópico {siguiente_topic}).")
            print(f"Este es el mensaje a reenviar: {mensaje_reenviar.hex()}")

    except Exception as e:
        print(f"Error al desencriptar el mensaje: {e}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado exitosamente al servidor MQTT")
        client.subscribe(TOPIC)
        print(f"Suscrito al tópico: {TOPIC}")
    else:
        print(f"Error de conexión con código {rc}")

# Función para enviar el paquete al servidor MQTT
def enviar_a_mqtt(paquete, topic):
    client = mqtt.Client()  
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)  
    client.connect(MQTT_HOST, MQTT_PORT, 60)  
    client.publish(topic, paquete)  
    client.disconnect()  
    print(f"Paquete enviado al servidor MQTT en el tópico {topic}.")

# Crear el cliente MQTT
client = mqtt.Client()

# Configurar credenciales de usuario y contraseña
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Asignar las funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectar al servidor MQTT
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Mantener el cliente en escucha
client.loop_forever()
