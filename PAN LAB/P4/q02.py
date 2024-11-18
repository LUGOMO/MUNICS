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
    m = 10
    alpha_values = np.arange(5e-04, 5e-03, 5e-04)  # Valores de alpha
    
    
    for alpha in alpha_values:
        error_count = 0
        for _ in range(1000):
            s = np.random.choice([-1, 0, 1], size=n)  # Vector secreto aleatorio
            a = np.random.randint(-q // 2, q // 2, size=n)  # Vector aleatorio a

            # Encriptar
            error = generate_error(1, alpha, q)[0]  # Generar error
            b = signed_mod(np.dot(s, a) + error + delta * m, q)  # Calcular b

            # Desencriptar
            r = signed_mod(b - np.dot(s, a), q)
            m_hat = np.round(r / delta)

            # Verificar si hay error en la descodificación
            if m_hat != m:
                error_count += 1

        # Imprimir el contador de errores para cada alpha
        print(f"Alpha: {alpha:.5f}, Errores: {error_count}")

if __name__ == "__main__":
    main()
