import numpy as np
import matplotlib.pyplot as plt

# Solicitamos al usuario el Valor n y p 
n = int(input("Por favor introduzca el numero de estudiantes que hicieron el examen (n): "))  # Cantidad de estudiantes
p = float(input("Por favor introduzca la probabilidad de que el estudiante no sea honesto(p): "))  # Probabilidad de que no sean honestos
gamma_Teorico = 0.75  # Valor teórico de gamma

# Función para calcular el estimador de p
def calcular_estimador_p(q, gamma):
    return (q - (1 - gamma)) / (2 * gamma - 1)

# Número de simulaciones para demostrar que el estimador es insesgado
cantidad_sims = 50  # Solo 50 simulaciones para el gráfico
estimadores_p = []

for _ in range(cantidad_sims):
    # Generación del vector de 1's y 0's
    X = np.random.choice([0, 1], size=n, p=[1 - p, p])

    # Respuesta Aleatorizada
    Primer_lanzamiento_moneda = np.random.choice([0, 1], size=n, p=[0.5, 0.5])  # Cruz = 0 , Cara = 1
    Segundo_lanzamiento_moneda = np.random.choice([0, 1], size=n, p=[0.5, 0.5])  # Cruz = 0 , Cara = 1
    Y = np.where(Primer_lanzamiento_moneda == 1, X, np.where(Segundo_lanzamiento_moneda == 1, 1, 0))

    # Calcular el valor empírico de gamma
    gamma_simulacion = np.mean(Y == X)

    # Calcular q (proporción de respuestas observadas "hizo trampa")
    q = p*gamma_simulacion +(1-p)*(1-gamma_simulacion)

    # Calcular el estimador de p
    estimador_p = calcular_estimador_p(q, gamma_simulacion)
    estimadores_p.append(estimador_p)

# Calcular la diferencia entre el valor verdadero de p y el estimador p
diferencias = [p - estimador for estimador in estimadores_p]

# Calcular el promedio del estimador p
promedio_estimador_p = np.mean(estimadores_p)

# Imprimir los resultados
print("Resultado de las Simulaciones (Primeros 20 valores de Y):", Y[:20])  # Muestra las primeras 20 respuestas aleatorizadas
print(f"Valor de gamma empírico: {gamma_simulacion}")
print(f"Valor esperado de gamma: {gamma_Teorico}")
print(f"Promedio del estimador p después de {cantidad_sims} simulaciones: {promedio_estimador_p}")
print(f"Valor verdadero de p: {p}")

# Representar las diferencias en el gráfico
plt.plot(range(1, cantidad_sims + 1), diferencias, marker='o', linestyle='None', color='b')  # Mostrar en el eje x las simulaciones (de 1 a 50)
plt.axhline(0, color='r', linestyle='--', linewidth=2)
plt.xlabel('Simulación (número de experimento)')
plt.ylabel('Diferencia (p - p\')')
plt.title('Validación empírica del estimador p\'')
plt.show()