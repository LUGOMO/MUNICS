from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from PIL import Image
import io
from io import BytesIO

def encrypt(key, plaintext):
    # Generate a random 128-bit IV.
    iv = os.urandom(16)
    
    # Construct an AES-128-CBC Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    ).encryptor()
    
    # Encrypt the plaintext and get the associated ciphertext.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    return (iv, ciphertext)

def decrypt(key, iv, ciphertext):
    # Construct a Cipher object, with the key, iv
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    ).decryptor()
    
    # Decryption gets us the plaintext.
    return decryptor.update(ciphertext) + decryptor.finalize()

# Example usage
key = os.urandom(16)
plaintext = b'This is a secret message.'
with open('image.jpg', 'rb') as f:
    data = f.read()
# Pad the plaintext to a multiple of 16 bytes
padder = padding.PKCS7(128).padder()
padded_plaintext = padder.update(data) + padder.finalize()


# Encrypt the plaintext
iv, ciphertext = encrypt(key, padded_plaintext)
# Decrypt the ciphertext
decrypted_text = decrypt(key, iv, ciphertext)

print("Original Text:", plaintext)
print("Decrypted Text:", decrypted_text)
# Load image from BytesIO
im = Image.open(BytesIO(decrypted_text))

# Display image
im.show()

