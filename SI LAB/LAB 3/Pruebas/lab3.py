import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

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

def generate_cover_set(node, n):
    cover_set = []
    while node > 1:
        sibling = node + 1 if node % 2 == 0 else node - 1
        cover_set.append(sibling)
        node = node // 2
    return cover_set

def encrypt_with_revocation(message, revoked_devices):    
    # Generate a random key for the disc.
    k = os.urandom(16)
    # Generate cover set for revoked devices.
    cover_set_duplicates = []
    for device in revoked_devices:
        values_coverset = generate_cover_set(device, n)
        for value in values_coverset:
            cover_set_duplicates.append(value)
    cover_set = []
    for node in cover_set_duplicates:
        if node not in cover_set:
            cover_set.append(node)
    # Encrypt keys for devices in the cover set.
    key_encryptions = []
    for node in cover_set:
        c = encrypt(key_dictionary[str(node)],k)
        key_encryptions.append(c)
    # Encrypt the content.
    content_encryption = encrypt(k, message)
    
    return (key_encryptions, content_encryption)

def decrypt_with_revocation(encrypted_keys, content_encryption, device):
    # Retrieve the key for the given device.
    for k_iv, k_ciphertext in encrypted_keys:
        i = device
        key_root = None
        while i > 0:
            try:
                key_root = decrypt(key_dictionary[str(i)], k_iv, k_ciphertext)
                iv, ciphertext = content_encryption
                try:
                    message = decrypt(key_root, iv, ciphertext)
                except Exception as e:
                    print(f"Decryption attempt failed with key: {key_dictionary[str(device)]}. Error: {e}")
                try:
                    message.decode('utf-8')
                except ValueError as e:
                    key_root = None
                    print(f"Device cannot decrypt the content with key {i}.")  
            except Exception as e:
                print(f"Decryption attempt failed with key: {i}. Error: {e}")
            if key_root is not None:
                break
            i = i // 2
        if key_root is not None:
                break 
    return message

# Example usage:
message = b'This is a secret message.'
device = 3
# Pad the plaintext to a multiple of 16 bytes
padder = padding.PKCS7(128).padder()
padded_plaintext = padder.update(message) + padder.finalize()
revoked_devices = {10}
encrypted_result = encrypt_with_revocation(padded_plaintext, revoked_devices)

# Simulate device 3 attempting to decrypt the content.
decrypted_result = decrypt_with_revocation(*encrypted_result, device)
try:
    print("Decrypted content:", decrypted_result.decode('utf-8'))
except ValueError as e:
    print(f"Device {device} cannot decrypt the content because the device key was compromised.") 
