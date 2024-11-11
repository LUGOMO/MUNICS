import os
from io import BytesIO
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PIL import Image
import PIL

n = 16

key_dictionary = {}

for i in range(1, n):  
    key = os.urandom(n)
    index = f'{i}'  
    key_dictionary[index] = key

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

# Function to generate the cover set given a compromised node.
def generate_cover_set(node, n):
    cover_set = []
    while node > 1:
        sibling = node + 1 if node % 2 == 0 else node - 1
        cover_set.append(sibling)
        node = node // 2
    return cover_set

# Encrypt exluiding the revoked devices
def encrypt_with_revocation(message, revoked_devices):    
    # Generate a random key k.
    k = os.urandom(16)
    # Generate cover set for revoked devices.
    cover_set_duplicates = []
    # Iterate over all the revoked devices.
    for device in revoked_devices:
        values_coverset = generate_cover_set(device, n)
        for value in values_coverset:
            cover_set_duplicates.append(value)
    cover_set = []
    # Remove duplicated nodes.
    for node in cover_set_duplicates:
        if node not in cover_set:
            cover_set.append(node)
    # Encrypt key k with the devices keys of the cover set.
    key_encryptions = []
    for node in cover_set:
        c = encrypt(key_dictionary[str(node)],k)
        key_encryptions.append(c)
    # Encrypt the content with k.
    content_encryption = encrypt(k, message)
    
    return (key_encryptions, content_encryption)

def decrypt_with_revocation(encrypted_keys, content_encryption, device):
    # Iterate over the cipher keys to find one that matches with the device's key path.
    for k_iv, k_ciphertext in encrypted_keys:
        # It's used to calculate if some key of the parents of the node were used to encrypt.
        i = device
        key_root = None
        # If i = 0 means that there is no more parents nodes. It's used to try to decrypt with the parents keys of the node, iterating over them.
        while i > 0:
            # The decrypt can throw an error if the key is incorrect, so I catch this errors.
            try:
                # Decrypt the key
                key_root = decrypt(key_dictionary[str(i)], k_iv, k_ciphertext)
                iv, ciphertext = content_encryption
                # Decrypt the message
                message = decrypt(key_root, iv, ciphertext)
                try:
                    # Try to open an image with the decrypted bytes.
                    Image.open(BytesIO(message))
                except PIL.UnidentifiedImageError as e:
                    key_root = None
                    print(f"Device cannot decrypt the content with key {i}.")  
            except Exception as e:
                print(f"Decryption attempt failed with key: {i}. Error: {e}")
            # If key found, break
            if key_root is not None:
                break
            # If the key wasn't found, it proves again with node's parent.
            i = i // 2
        # If key found, break
        if key_root is not None:
                break 
    return message


device = 3
with open('image.jpg', 'rb') as f:
    data = f.read()

# Pad the plaintext to a multiple of 16 bytes
padder = padding.PKCS7(128).padder()
padded_plaintext = padder.update(data) + padder.finalize()
revoked_devices = {10,12}
encrypted_result = encrypt_with_revocation(padded_plaintext, revoked_devices)

# Simulate device attempting to decrypt the content.
decrypted_result = decrypt_with_revocation(*encrypted_result, device)
try:
    im = Image.open(BytesIO(decrypted_result))
    # Display image
    im.show()
except PIL.UnidentifiedImageError as e:
    print(f"Device {device} cannot decrypt the content because the device key was compromised.") 
