from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
import os

# Crea un par de claves Diffie-Hellman (X25519).
# Retorna la clave privada y la clave pública.
def crear_par_claves_dh():

    clave_privada = x25519.X25519PrivateKey.generate()
    clave_publica = clave_privada.public_key()
    return clave_privada, clave_publica

# Aplica el ratchet Diffie-Hellman.
# Usa la clave privada local y la clave pública remota para derivar una clave compartida.
def actualizar_clave_dh(clave_privada_local, clave_publica_remota):
   
    clave_compartida = clave_privada_local.exchange(clave_publica_remota)
    clave_derivada = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b'handshake data',
    ).derive(clave_compartida)
    return clave_derivada

# Aplica el ratchet simétrico.
# Combina la clave derivada (del ratchet DH) con la clave raíz para generar una nueva clave simétrica.
def actualizar_clave_simetrica(clave_derivada, clave_raiz):
    
    h = HMAC(clave_derivada, hashes.SHA256(), backend=default_backend())
    h.update(clave_raiz)
    return h.finalize()

 
#  Cifra el texto plano usando AES-CBC con la clave simétrica.
#  Genera un vector inicial aleatorio.
def cifrar(clave_simetrica, texto_plano):
   
    vector_inicial = os.urandom(16)
    cifrador = Cipher(
        algorithms.AES(clave_simetrica),
        modes.CBC(vector_inicial),
        backend=default_backend()
    ).encryptor()
    texto_cifrado = cifrador.update(texto_plano) + cifrador.finalize()
    return (vector_inicial, texto_cifrado)


 # Descifra el texto cifrado usando AES-CBC con la clave simétrica y el vector inicial.
def descifrar(clave_simetrica, vector_inicial, texto_cifrado):

    descifrador = Cipher(
        algorithms.AES(clave_simetrica),
        modes.CBC(vector_inicial),
        backend=default_backend()
    ).decryptor()
    texto_plano = descifrador.update(texto_cifrado) + descifrador.finalize()
    return texto_plano
