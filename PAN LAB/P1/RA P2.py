import numpy as np

# Solicitamos al usuario el Valor n y p 
n = int(input("Por favor introduzca el numero de estudiantes que hicieron el examen (n): ")) # Cantidad de estudiantes
p = float(input("Por favor introduzca la probabilidad de que el estudiante no sea honesto(p): ")) #Probabilidad de que no sean honestos
gamma_Teorico = 0.75

# Generacion del vector de 1's y 0's

X = np.random.choice([0,1], size=n,p=[1-p, p])

# Respuesta Aleatorizada
Primer_lanzamiento_moneda = np.random.choice([0,1], size=n, p=[0.5, 0.5]) # Cruz = 0 , Cara = 1""
Segundo_lanzamiento_moneda = np.random.choice([0,1], size=n, p=[0.5, 0.5]) # Cruz = 0 , Cara = 1""
Y = np.where(Primer_lanzamiento_moneda == 1, X, np.where(Segundo_lanzamiento_moneda == 1, 1, 0))

gamma_simulacion = np.mean(Y == X)
# Imprimir las respuestas generadas

##
print("Resultado de las Simulaciones:",Y[:20]) #Muestra la respuesta de las 2 primeras simulaciones
print(f"Valor de gamma empírico: {gamma_simulacion}")
print(f"Valor esperado de gamma: {gamma_Teorico}")
 

