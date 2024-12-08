from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
import paho.mqtt.client as mqtt
import base64
import DoubleRatchet

SERVIDOR_MQTT = "18.100.158.114"
PUERTO_MQTT = 1883
USUARIO_MQTT = "sinf"
CONTRASENA_MQTT = "HkxNtvLB3GC5GQRUWfsA"
INTERVALO_MANTENIMIENTO = 60
TEMA_ENTRADA = "hnf.in"
TEMA_SALIDA = "hnf.out"

CLAVE_RAIZ = b"manzanaperaraton1020304050ratonperamanzana"

clave_privada_local = None
clave_publica_local = None
clave_publica_remota = None
cliente_mqtt = None

def on_message(mqttc, userdata, mensaje):
    global clave_publica_remota
    contenido = mensaje.payload.decode('utf-8')
    partes = contenido.split(":")

    try:
        if partes[0] == 'start':
            # Procesar mensaje de inicio: solo actualizar clave pública
            clave_publica_remota = x25519.X25519PublicKey.from_public_bytes(base64.b64decode(partes[1].encode('utf-8')))
            print(f"Clave pública inicial recibida:\t{clave_publica_remota.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)}")
            return  # No procesar más en el mensaje inicial

        # Procesar mensajes normales
        public_bytes = base64.b64decode(partes[0].encode('utf-8'))
        iv = base64.b64decode(partes[1].encode('utf-8'))
        ciphertext = base64.b64decode(partes[2].encode('utf-8'))

        # Validar tamaño del IV
        if len(iv) != 16:
            raise ValueError("El tamaño del IV no es válido. Debe ser de 16 bytes.")

        # Actualizar clave pública remota
        nueva_publica_remota = x25519.X25519PublicKey.from_public_bytes(public_bytes)
        clave_publica_remota = nueva_publica_remota
        print(f"Clave pública recibida:\t{nueva_publica_remota.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)}")

        # Derivar claves y descifrar
        clave_derivada = DoubleRatchet.actualizar_clave_dh(clave_privada_local, clave_publica_remota)
        clave_simetrica = DoubleRatchet.actualizar_clave_simetrica(clave_derivada, CLAVE_RAIZ)

        mensaje_descifrado = DoubleRatchet.descifrar(clave_simetrica, iv, ciphertext)
        unpadder = padding.PKCS7(128).unpadder()
        mensaje_plano = unpadder.update(mensaje_descifrado) + unpadder.finalize()
        print("Mensaje recibido:\t" + mensaje_plano.decode('utf-8'))

    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

def configurar_cliente_mqtt(servidor, puerto, tema, usuario, contrasena, keepalive):
    cliente = mqtt.Client()
    cliente.on_message = on_message
    cliente.username_pw_set(usuario, contrasena)
    cliente.connect(servidor, puerto, keepalive)
    cliente.subscribe(tema)
    return cliente

def ciclo_envio():
    contador_envios = 1
    while True:
        global clave_privada_local, clave_publica_local
        cliente_mqtt.loop_start()
        mensaje_usuario = input("\nEscribe tu mensaje: \n").strip()

        if contador_envios > 5:
            # Regenerar claves DH después de 2 mensajes
            clave_privada_local, clave_publica_local = DoubleRatchet.crear_par_claves_dh()
            contador_envios = 1

        # Derivar claves y cifrar mensaje
        clave_derivada = DoubleRatchet.actualizar_clave_dh(clave_privada_local, clave_publica_remota)
        clave_simetrica = DoubleRatchet.actualizar_clave_simetrica(clave_derivada, CLAVE_RAIZ)

        padder = padding.PKCS7(128).padder()
        texto_plano_padded = padder.update(mensaje_usuario.encode('utf-8')) + padder.finalize()

        iv, texto_cifrado = DoubleRatchet.cifrar(clave_simetrica, texto_plano_padded)

        # Codificar datos en Base64
        public_bytes_b64 = base64.b64encode(clave_publica_local.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode('utf-8')
        iv_b64 = base64.b64encode(iv).decode('utf-8')
        ciphertext_b64 = base64.b64encode(texto_cifrado).decode('utf-8')

        # Enviar datos
        cliente_mqtt.publish(TEMA_SALIDA, f"{public_bytes_b64}:{iv_b64}:{ciphertext_b64}")
        contador_envios += 1

def main():
    global clave_privada_local, clave_publica_local, cliente_mqtt

    # Generar claves iniciales
    clave_privada_local, clave_publica_local = DoubleRatchet.crear_par_claves_dh()

    # Configurar cliente MQTT
    cliente_mqtt = configurar_cliente_mqtt(SERVIDOR_MQTT, PUERTO_MQTT, TEMA_ENTRADA, USUARIO_MQTT, CONTRASENA_MQTT, INTERVALO_MANTENIMIENTO)

    # Enviar clave pública inicial con Base64
    public_bytes_b64 = base64.b64encode(clave_publica_local.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode('utf-8')
    cliente_mqtt.publish(TEMA_SALIDA, f"start:{public_bytes_b64}")

    ciclo_envio()

if __name__ == "__main__":
    main()
