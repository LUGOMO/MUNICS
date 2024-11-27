import numpy as np

def signed_mod(a, q):
    """ Reducción módulo q para mantener los valores en el rango [-q/2, q/2-1]. """
    r = a % q
    return np.where(r > q // 2 - 1, r - q, r)

def generate_error(m, alpha, q):
    """ Genera errores a partir de una distribución Gaussiana con desviación estándar alpha*q. """
    desviacion = alpha * q
    samples = np.random.normal(loc=0, scale=desviacion, size=m)  # Distribución normal
    samples = np.round(samples)  # Redondear al entero más cercano
    return signed_mod(samples, q)  # Reducir módulo q y ajustar el rango

def main():
    n = 256
    q = 2**16
    delta = 2**10
    m1 = 10
    m2 = 8
    alpha_values = np.arange(5e-04, 5e-03, 5e-04)  # Valores de alpha

    for alpha in alpha_values:
        error_count = 0
        for _ in range(1000):
            s = np.random.choice([-1, 0, 1], size=n)  # Vector secreto aleatorio
            a1 = np.random.randint(-q // 2, q // 2, size=n)  # Vector aleatorio a1
            a2 = np.random.randint(-q // 2, q // 2, size=n)  # Vector aleatorio a2

            # Encriptar m1
            error1 = generate_error(1, alpha, q)[0]  # Generar error para m1
            b1 = signed_mod(np.dot(s, a1) + error1 + delta * m1, q)  # Calcular b1

            # Encriptar m2
            error2 = generate_error(1, alpha, q)[0]  # Generar error para m2
            b2 = signed_mod(np.dot(s, a2) + error2 + delta * m2, q)  # Calcular b2

            # Suma homomórfica de los cifrados
            a_sum = signed_mod(a1 + a2, q)  # Suma de los vectores a1 y a2
            b_sum = signed_mod(b1 + b2, q)  # Suma de los vectores b1 y b2

            # Desencriptar el resultado de la suma
            r = signed_mod(b_sum - np.dot(s, a_sum), q)
            m_hat = np.round(r / delta)

            # Verificar si hay error en la descodificación
            if m_hat != (m1 + m2):
                error_count += 1

        # Imprimir el contador de errores para cada alpha
        print(f"Alpha: {alpha:.5f}, Errores en suma: {error_count}")

if __name__ == "__main__":
    main()
