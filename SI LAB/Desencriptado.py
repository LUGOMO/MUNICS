from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Ruta de la clave privada (en formato OpenSSH)
private_key_path = r"E:\MUNICS\SI\Assignment 1\CLAVES\Claves Originales\LGM"

# Cargar la clave privada del destinatario (LGM)
with open(private_key_path, "rb") as key_file:
    private_key = serialization.load_ssh_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Simulación de recepción de un paquete cifrado (reemplazar con el paquete real recibido)
paquete = b'\x82\xd5\xa8@\xcf\xc6\x8ek\xfdi>\x1dI\xf7\x1fO\xf1\xf1\xdb\xb8\x9f<\xa2\xc2\xdcOB\xf2\x9eWOj\x1f^\x1e\x06\x1d\xd0\xbc{\xb7\xe8\xbe\xa0\xab8~\xd4\xdf8\xba\xf4\xe1\x16\xbd\xfe}\xfa?9\x0b\xad\xf4\xf2>U\xdd,\xa427\xca\xcd\xf7~\xa7\x1a\x8a\x1d\xb0\xdb?e\x8d\x14R\xc8\xe8\xa0\x8c\x00\x97a\xcdR\xd8\xb8\xb0\xea\xf1\xa5\xbeZ\x05\xe6b#\x0c\x81\x1bQ\xc7g#\xce\xb8>\r\xf8\x9f\xa7\x82Z,%\xc8\xcb\x82k\x1e\xe3=\xa7\x04\xd9\xba[\x81\x11\xec\x9f\x10\xfe\xf3\x9d\xb3\xf5\xe2\xd3I>\xdd\x1a\x91\\\xcc\xc9T\xeb\xf0c\xc0<P\x81[P\xee;\x06\xfc\xe5i\x11\x83\xe2v2-B#?\x94""pn \xb4HHn\x0b\xe3\x1d\xc8\xa4\xec\xf9\x89\xeb\xba\x08\x1e|s\xee\xe1}\x0e\xd3\xdb\xfaS|S8r\x0f\x14\xe8\xe4p]\xd4\xb6\xd9\xae$;\xa7\xd2\xbf%a\x80\x1d\x14\xac\xa2\xcc\x8dk\xc5\xff\xdc,]\x97\x04\xc6SaaC!\x11,\x8e\x86\xech\xb7\x95U\x92\xa9\xa7\xb2\xe9\x1e\xc4!)\xb8\x1f\x84j\xdbJ\x90\x8d\x85\xb1n\x0f'
print(f"\nEste es el array del paquete\n:", paquete)
paquete1= paquete[:256]
paquete2= paquete[256:]

# Desencriptar los primeros 256 bytes con la clave privada para obtener la clave simétrica

ksimetrica = private_key.decrypt(
    paquete1,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# # Usar la clave simétrica desencriptada para desencriptar el resto del mensaje
aesgcm = AESGCM(ksimetrica)
nonce = ksimetrica
try:
    mensaje_Desencriptado = aesgcm.decrypt(nonce, paquete2, None)
    print("Mensaje desencriptado exitosamente.")
except Exception as e:
    print(f"Error al desencriptar el mensaje: {e}") 
exit()

# # Verificar si los primeros 5 bytes son \x00\x00end
# header = mensaje_Desencriptado[:5]
# if header == b'\x00\x00end':
#     print("Este mensaje es para ti.")
    
#     # Quitar los primeros 5 bytes (\x00\x00end)
#     mensaje_Desencriptado = mensaje_Desencriptado[5:]
    
#     # Los siguientes 5 bytes son el ID del remitente
#     sender_id = mensaje_Desencriptado[:5]
#     print(f"El mensaje fue enviado por: {sender_id.decode('ascii')}")
    
#     # El contenido restante es el mensaje cifrado
#     mensaje = mensaje_Desencriptado[5:].decode('ascii')
#     print(f"El mensaje es: {mensaje}")

# else:
#     # Si no contiene \x00\x00end, no está destinado a ti
#     print("El mensaje no es para ti.")
