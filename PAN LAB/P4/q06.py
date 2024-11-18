import numpy as np

def signed_mod(a, q):
    """ Reducción módulo q para mantener los valores en el rango [-q/2, q/2-1]. """
    r = a % q
    return np.where(r > q // 2 - 1, r - q, r)

def generate_error(m, alpha, q):
    """ Genera errores a partir de una distribución Gaussiana con desviación estándar alpha*q. """
    desviacion = alpha * q
    samples = np.random.normal(loc=0, scale=desviacion, size=m)
    samples = np.round(samples)
    return signed_mod(samples, q)

def gadget_decomposition(c, p):
    """ Realiza la descomposición gadget de c usando potencias de 2^p. """
    max_val = 2**p
    c_0 = c % max_val  # Resto de la división
    c_1 = c // max_val  # Cociente de la división
    return c_0, c_1

def encrypt(a, s, delta, m, q, alpha):
    """ Encripta un mensaje m generando (a, b). """
    error = generate_error(1, alpha, q)[0]
    b = signed_mod(np.dot(a, s) + error + delta * m, q)
    return a, b

def change_key(cipher, s_old, s_new, q, delta, p):
    """ Realiza el cambio de clave usando la descomposición gadget. """
    a, b = cipher
    c_0, c_1 = gadget_decomposition(np.max(np.abs(a)), p)

    # Generar nuevo ciphertext basado en descomposición gadget
    a_prime = signed_mod(c_0 * a + (c_1 * (2**p)) * a, q)
    b_prime = signed_mod(c_0 * b + (c_1 * (2**p)) * b, q)

    return a_prime, b_prime

def main_q6():
    n = 128
    q = 2**24
    delta = 2**22
    alpha = 5e-06
    m = 10
    repetitions = 1000
    p = 4

    error_count = 0

    for _ in range(repetitions):
        s_old = np.random.choice([-1, 0, 1], size=n)
        s_new = np.random.choice([-1, 0, 1], size=n)
        a = np.random.randint(-q // 2, q // 2, size=n)

        cipher = encrypt(a, s_old, delta, m, q, alpha)

        a_prime, b_prime = change_key(cipher, s_old, s_new, q, delta, p)

        r_new = signed_mod(b_prime - np.dot(a_prime, s_new), q)
        m_hat_new = np.round(r_new / delta)

        if m_hat_new != m:
            error_count += 1

    print(f"Alpha: {alpha}, Errores en cambio de clave: {error_count}")

if __name__ == "__main__":
    main_q6()


