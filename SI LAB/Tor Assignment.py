from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESCM
import os
import pubkeys

# Private Key reading
with open(r"E:\MUNICS\SI\Assignment 1\CLAVES\LGM", "rb") as key_file:
        private_key =serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
# Public Key reading
with open(r"E:\MUNICS\SI\Assignment 1\CLAVES\LGM_public.pem" , "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
        
# RSA-OAEP Encrypting and decrypting
message = b’encrypt me!’
encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
)
original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )    
# AES-GCM encryption and decryption
data = b"a secret message"
key = AESGCM.generate_key(bit_length=128)
aesgcm = AESGCM(key)
nonce = key
ciphertext = aesgcm.encrypt(nonce, data, None)
aesgcm.decrypt(nonce, ciphertext, None)    

        
# shows Decrypted Message
print("Mensaje desencriptado:", decrypted_data.decode())

pubkeys.pubkeydictionary("LGM")