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
    c_1 = c // (2**p)  # Parte alta
    c_0 = c % (2**p)  # Parte baja
    
    # Ajustar rangos
    c_0 = signed_mod(c_0, 2**p)
    c_1 = signed_mod(c_1, 2**p)

    return [(c_0, 0), (c_1, p)]  # Devolver coeficientes con su escala

def main():
    n = 256
    q = 2**16
    delta = 2**10
    m = 3
    c = 10
    p = 3
    alpha_values = np.arange(5e-04, 5e-03, 5e-04)  # Valores de alpha

    # Parte 1: Multiplicación directa con c = 10
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
            a_mult = signed_mod(c * a, q)  # Multiplicar vector a por c
            b_mult = signed_mod(c * b, q)  # Multiplicar b por c

            # Desencriptar el resultado de la multiplicación
            r = signed_mod(b_mult - np.dot(s, a_mult), q)
            m_hat = np.round(r / delta)

            # Verificar si hay error en la descodificación
            if m_hat != (c * m):
                error_count_direct += 1

        print(f"Alpha: {alpha:.5f}, Errores en multiplicación directa: {error_count_direct}")

    # Parte 2: Multiplicación con descomposición gadget
    print("\nMultiplicación con descomposición gadget:")
    for alpha in alpha_values:
        error_count_gadget = 0
        for _ in range(1000):
            s = np.random.choice([-1, 0, 1], size=n)  # Vector secreto aleatorio

            # Descomposición gadget de c
            gadget_components = gadget_decomposition(c, p)

            # Inicializar acumuladores para las partes gadget
            a_gadget_total = np.zeros(n, dtype=int)
            b_gadget_total = 0

            for coeff, scale in gadget_components:
                # Generar dinámicamente un nuevo vector aleatorio a para este componente
                a_component = np.random.randint(-q // 2, q // 2, size=n)

                # Calcular el mensaje escalado dinámicamente
                m_scaled = m * (2**scale)

                # Generar error dinámico
                error_component = generate_error(1, alpha, q)[0]

                # Calcular b para este componente
                b_component = signed_mod(np.dot(s, a_component) + error_component + delta * m_scaled, q)

                # Acumular las partes gadget
                a_gadget_total = signed_mod(a_gadget_total + coeff * a_component, q)
                b_gadget_total = signed_mod(b_gadget_total + coeff * b_component, q)

            # Desencriptar el resultado combinado
            r = signed_mod(b_gadget_total - np.dot(s, a_gadget_total), q)
            m_hat = np.round(r / delta)

            # Verificar si hay error en la descodificación
            if m_hat != (c * m):
                error_count_gadget += 1

        print(f"Alpha: {alpha:.5f}, Errores en multiplicación gadget: {error_count_gadget}")

if __name__ == "__main__":
    main()
