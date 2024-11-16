import os
import math
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Solicitamos el mensaje
mensaje = input("Por favor introduzca el mensaje a enviar: ")

# Solicitamos el numero de dispositivos
n_original = int(input("Por favor introduzca la cantidad de dispositivos: "))

# Ajustamos n a la siguiente potencia de 2 para completar el arbol
if n_original & (n_original - 1) != 0:
    n = 1 << (n_original - 1).bit_length()
else:
    n = n_original

# Calculo del rango de dispositivos (hojas) en el arbol
inicio_dispositivo = n
fin_dispositivo = inicio_dispositivo + n_original - 1
print(f"Los dispositivos estan en el rango: {inicio_dispositivo} a {fin_dispositivo} (para {n_original} dispositivos)")

# Solicitamos los dispositivos comprometidos
while True:
    dispositivos_comprometidos = input(
        f"Por favor introduzca los dispositivos que desea comprometer (deje vacio si no hay dispositivos comprometidos, o ingrese dispositivos entre {inicio_dispositivo} y {fin_dispositivo}, separados por comas): "
    )

    # Si el usuario deja la entrada vacia, no hay dispositivos comprometidos
    if dispositivos_comprometidos.strip() == "":
        dispositivos_comprometidos = []
        break

    # Convertimos la entrada en una lista de enteros
    dispositivos_comprometidos = [int(n) for n in dispositivos_comprometidos.split(",")]

    # Verificamos que todos los dispositivos estan en el rango permitido
    if all(inicio_dispositivo <= nodo <= fin_dispositivo for nodo in dispositivos_comprometidos):
        break
    print(f"Uno o mas numeros ingresados no son validos. Por favor, ingrese numeros entre {inicio_dispositivo} y {fin_dispositivo}.")

print(f"Los dispositivos comprometidos son: {dispositivos_comprometidos if dispositivos_comprometidos else 'Ninguno'}")

# Generar claves aleatorias de 128 bits para cada nodo en el arbol
key_vault = {i: os.urandom(16) for i in range(1, 2 * n)}

def encrypt(key, mensaje):
    iv = os.urandom(16)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    ).encryptor()
    ciphertext = encryptor.update(mensaje) + encryptor.finalize()
    return iv, ciphertext

def decrypt(key, iv, ciphertext):
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    ).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Funcion para calcular el conjunto de cobertura de los dispositivos no comprometidos
def calculo_cobertura(n, dispositivos_comprometidos, fin_dispositivo):
    if not dispositivos_comprometidos:
        return [1]  

    Chequeo_nodo = {}
    total_nodos = 2 * n

    for i in range(1, total_nodos):
        Chequeo_nodo[i] = 'unknown'

    for nodo in dispositivos_comprometidos:
        Chequeo_nodo[nodo] = 'comprometido'

    for i in range(n, fin_dispositivo + 1):
        if Chequeo_nodo[i] != 'comprometido':
            Chequeo_nodo[i] = 'no_comprometido'

    for i in range(n - 1, 0, -1):
        hijo_izq = i * 2
        hijo_der = i * 2 + 1

        stat_izq = Chequeo_nodo.get(hijo_izq, 'unknown')
        stat_der = Chequeo_nodo.get(hijo_der, 'unknown')

        if stat_izq == 'no_comprometido' and stat_der == 'no_comprometido':
            Chequeo_nodo[i] = 'no_comprometido'
        elif stat_izq == 'comprometido' and stat_der == 'comprometido':
            Chequeo_nodo[i] = 'comprometido'
        else:
            Chequeo_nodo[i] = 'parcialmente_comprometido'

    coverage_set = []

    def collect_nodes(node):
        status = Chequeo_nodo.get(node, '')
        if status == 'no_comprometido' and node !=1:
            coverage_set.append(node)
        elif status == 'parcialmente_comprometido':
            collect_nodes(node * 2)
            collect_nodes(node * 2 + 1)

    collect_nodes(1)
    return coverage_set

def encrypt_with_coverage_non_compromised(mensaje, dispositivos_comprometidos, key_vault, n, fin_dispositivo):
    # Calculamos el conjunto de cobertura correcto despues de comprometer los indicados 
    cobertura_filtrada = calculo_cobertura(n, dispositivos_comprometidos, fin_dispositivo)
    print(f"\nCobertura para dispositivos no comprometidos: {sorted(cobertura_filtrada)}")

    plaintext = mensaje.encode()

    # Generamos una clave aleatoria K para cifrar el mensaje
    k = os.urandom(16)

    # Aplicamos padding al mensaje para que su longitud sea múltiplo de 16
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Ciframos el mensaje con la clave K
    iv_message, ciphertext = encrypt(k, padded_plaintext)

    # Generamos los tags
    tag = b"valido".ljust(16, b'\x00')
    tag2 = b"final".ljust(16, b'\x00')

    # Iniciamos el resultado con el IV del mensaje
    result = iv_message

    # Ciframos la clave K con las claves de los nodos en la cobertura filtrada
    encrypted_k_blocks = []

    for nodo in sorted(cobertura_filtrada):
        nodo_key = key_vault[nodo]
        tag_y_k = tag + k
        iv_key, encrypted_k_tag = encrypt(nodo_key, tag_y_k)
        encrypted_k_blocks.append(iv_key + encrypted_k_tag)

    # Agregamos los bloques cifrados de K al resultado
    for block in encrypted_k_blocks:
        result += block

    # Agregamos el tag final y el mensaje cifrado al resultado
    result += tag2 + ciphertext

    return result, cobertura_filtrada

def decrypt_with_coverage_non_compromised(encrypted_data, dispositivo, key_vault, cobertura):
    # Calculamos las claves que el dispositivo conoce
    claves_conocidas = []
    nodo_actual = dispositivo
    while nodo_actual >= 1:
        claves_conocidas.append(nodo_actual)
        nodo_actual = nodo_actual // 2

    print(f'\nLas claves que conoce el dispositivo {dispositivo} son {sorted(claves_conocidas)}')

    
    offset = 0
    iv_message = encrypted_data[offset:offset+16]
    offset += 16

    k = None
    final_tag = None

    # Intentamos descifrar K con las claves conocidas
    while offset < len(encrypted_data):
        potential_final_tag = encrypted_data[offset:offset+16]
        if potential_final_tag == b"final".ljust(16, b'\x00'):
            final_tag = potential_final_tag
            offset += 16
            break
        else:
            iv_key = encrypted_data[offset:offset+16]
            offset += 16
            encrypted_k_tag = encrypted_data[offset:offset+32]
            offset += 32

            if k is None:
                for nodo in claves_conocidas:
                    if nodo in cobertura:
                        nodo_key = key_vault[nodo]
                        try:
                            decrypted_k_tag = decrypt(nodo_key, iv_key, encrypted_k_tag)
                            tag = decrypted_k_tag[:16]
                            if tag == b"valido".ljust(16, b'\x00'):
                                k = decrypted_k_tag[16:]
                                print(f"Clave K descifrada con éxito usando el nodo {nodo}.")
                                break
                        except Exception:
                            continue

    if k is None:
        print("No se pudo descifrar la clave K con las claves disponibles.")
        return None

    if final_tag != b"final".ljust(16, b'\x00'):
        print("El tag final no es valido. Desencriptado fallido.")
        return None

    # El resto es el ciphertext
    ciphertext = encrypted_data[offset:]

    # Desciframos el mensaje final
    padded_plaintext = decrypt(k, iv_message, ciphertext)

    
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode()

# Llamada a la funcion de encriptado
encrypted_output, cobertura_filtrada = encrypt_with_coverage_non_compromised(
    mensaje, dispositivos_comprometidos, key_vault, n, fin_dispositivo
)

# Solicitamos el dispositivo que intentara desencriptar
dispositivo = int(input("\nPor favor indique el dispositivo que intentara desencriptar: "))

# Llamada a la funcion de desencriptado
mensaje_desencriptado = decrypt_with_coverage_non_compromised(
    encrypted_output, dispositivo, key_vault, cobertura_filtrada
)

if mensaje_desencriptado:
    print(f"\nEl mensaje desencriptado es: {mensaje_desencriptado}")
else:
    print("\nNo se pudo desencriptar el mensaje.")
