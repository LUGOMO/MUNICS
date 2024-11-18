import numpy as np
import matplotlib.pyplot as plt

def generate_error(m, alpha, q):
    # Muestreamos de una distribución Gaussiana con desviación estándar alpha * q
    gaussian_samples = np.random.normal(0, alpha * q, m)
    # Redondeamos al entero más cercano
    rounded_samples = np.round(gaussian_samples)
    # Reducimos módulo q al rango [-q/2, q/2-1]
    error_samples = np.mod(rounded_samples + q // 2, q) - q // 2
    return error_samples

# Parámetros
q = 100
m = 10000

# Generar los errores para diferentes valores de alpha
alphas = [0.01, 0.1, 1]

# Graficar los histogramas para cada alpha
plt.figure(figsize=(15, 5))
for i, alpha in enumerate(alphas):
    errors = generate_error(m, alpha, q)
    plt.subplot(1, 3, i + 1)
    plt.hist(errors, bins=np.arange(-q // 2, q // 2), edgecolor='black')
    plt.title(f"Histograma de errores para α = {alpha}")
    plt.xlabel("Valor del error")
    plt.ylabel("Frecuencia")
plt.tight_layout()
plt.show()
