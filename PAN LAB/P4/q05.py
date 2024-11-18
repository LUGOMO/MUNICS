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

def gadget_decomposition(c, p):
    """ Realiza la descomposición gadget de c usando el valor p. """
    # Encontrar c^(1) como el cociente de c dividido por 2^p
    c_1 = c // (2**p)
    # Encontrar c^(0) como el residuo de c módulo 2^p
    c_0 = c % (2**p)
    
    # Asegurar que c^(0) y c^(1) estén en el intervalo [-2^(p-1), 2^(p-1)-1]
    max_val = 2**(p-1)
    c_0 = signed_mod(c_0, 2**p)  # Asegurar que c_0 esté en [-2^(p-1), 2^(p-1)-1]
    c_1 = signed_mod(c_1, 2**p)  # Asegurar que c_1 esté en [-2^(p-1), 2^(p-1)-1]

    return c_0, c_1

def main():
    n = 256
    q = 2**16
    delta = 2**10
    m = 3
    p = 3
    alpha_values = np.arange(5e-04, 5e-03, 5e-04)  # Valores de alpha

    # Parte 1: Multiplicación directa con c = 10
    c_direct = 10
    print("Multiplicación directa:")
    for alpha in alpha_values:
        error_count_direct = 0
        for _ in range(1000):
            s = np.random.choice([-1, 0, 1], size=n)  # Vector secreto aleatorio
            a = np.random.randint(-q // 2, q // 2, size=n)  # Vector aleatorio a

            # Encriptar el mensaje m
            error = generate_error(1, alpha, q)[0]  # Generar error
            b = signed_mod(np.dot(s, a) + error + delta * m, q)  # Calcular b

            # Multiplicación homomórfica directa con constante c
            a_mult = signed_mod(c_direct * a, q)  # Multiplicar vector a por c
            b_mult = signed_mod(c_direct * b, q)  # Multiplicar b por c

            # Desencriptar el resultado de la multiplicación
            r = signed_mod(b_mult - np.dot(s, a_mult), q)
            m_hat = np.round(r / delta)

            # Verificar si hay error en la descodificación
            if m_hat != (c_direct * m):
                error_count_direct += 1

        print(f"Alpha: {alpha:.5f}, Errores en multiplicación directa: {error_count_direct}")

    # Parte 2: Multiplicación con descomposición gadget
    print("Multiplicación con descomposición gadget:")
    c_0, c_1 = gadget_decomposition(c_direct, p)  # Realizar la descomposición gadget de c

    for alpha in alpha_values:
        error_count_gadget = 0
        for _ in range(1000):
            s = np.random.choice([-1, 0, 1], size=n)  # Vector secreto aleatorio
            a = np.random.randint(-q // 2, q // 2, size=n)  # Vector aleatorio a

            # Encriptar el mensaje m
            error = generate_error(1, alpha, q)[0]  # Generar error
            b = signed_mod(np.dot(s, a) + error + delta * m, q)  # Calcular b

            # Multiplicación homomórfica utilizando la descomposición gadget
            a_gadget = signed_mod(c_0 * a + (c_1 * 2**p) * a, q)  # Suma ponderada de los componentes gadget
            b_gadget = signed_mod(c_0 * b + (c_1 * 2**p) * b, q)  # Suma ponderada de los componentes gadget

            # Desencriptar el resultado de la multiplicación gadget
            r = signed_mod(b_gadget - np.dot(s, a_gadget), q)
            m_hat = np.round(r / delta)

            # Verificar si hay error en la descodificación
            if m_hat != (c_direct * m):
                error_count_gadget += 1

        print(f"Alpha: {alpha:.5f}, Errores en multiplicación gadget: {error_count_gadget}")

if __name__ == "__main__":
    main()
