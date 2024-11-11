import pandas as pd
import numpy as np

def conteo_bits(base_datos):
    items_conteo_bits = ["SB1", "SB2"]
    conteo_bits = []
    for i in range(0, 2):
        conteo_bits.append(np.count_nonzero(base_datos[items_conteo_bits[i]]))

    return conteo_bits

def histograma(base_datos):
    hist = np.zeros(126)
    for i in base_datos.Edad:
        hist[i] += 1

    return hist

def base_datos_aleatoria(n):
    nombres_aleatorios = ["David", "Luis", "Michel", "Andres", "Irina", "Alexander", "Paulina", "Mariana", "Elizabeth", "Bianca"]

    nombres_bd = np.random.choice(nombres_aleatorios, n).tolist()
    edades_bd = np.random.choice(range(0, 126), n).tolist()
    sb1_bd = np.random.choice(range(0, 2), n).tolist()
    sb2_bd = np.random.choice(range(0, 2), n).tolist()

    base_datos = pd.DataFrame({"Nombre": nombres_bd, "Edad": edades_bd, "SB1": sb1_bd, "SB2": sb2_bd})
    return base_datos

# Construyendo una base de datos aleatoria
n = 50

def q1(base_datos: pd.DataFrame, epsilon):
    sensibilidad = 125 / base_datos.shape[0]
    media_con_ruido = np.mean(base_datos.Edad) + np.random.laplace(0, sensibilidad / epsilon)
    if media_con_ruido > 125:
        media_con_ruido = 125
    if media_con_ruido < 0:
        media_con_ruido = 0
    return media_con_ruido

def q2(base_datos, epsilon):
    sensibilidad = 125
    mediana_con_ruido = np.round(np.median(base_datos.Edad) + np.random.laplace(0, sensibilidad / epsilon))
    if mediana_con_ruido > 125:
        mediana_con_ruido = 125
    if mediana_con_ruido < 0:
        mediana_con_ruido = 0
    return mediana_con_ruido

# Aquí conseguimos el número de bits seguros con privacidad diferencial (DP)
def q3(base_datos, epsilon):
    sensibilidad = 2

    conteo_de_bits = conteo_bits(base_datos)

    conteo_bits_con_ruido = []
    for i in range(0, len(conteo_de_bits)):
        conteo_bits_con_ruido.append(np.round(conteo_de_bits[i] + np.random.laplace(0, sensibilidad / epsilon)))

    return conteo_bits_con_ruido

# Aquí conseguimos el histograma seguro con privacidad diferencial (DP)
def q4(base_datos, epsilon):
    sensibilidad = 2

    hist = histograma(base_datos)

    hist_con_ruido = []

    for i in range(0, len(hist)):
        hist_con_ruido_e = np.round(hist[i] + np.random.laplace(0, sensibilidad / epsilon))
        if hist_con_ruido_e < 0:
            hist_con_ruido_e = 0
        hist_con_ruido.append(hist_con_ruido_e)

    return np.array(hist_con_ruido)

def nrmsd(lista_errores, valor_real):
    '''
    Función que calcula el NRMSD dados 2 vectores: lista_errores, que está formada por los errores; y valor_real, que está formado por los valores reales.
    '''
    lista_errores_cuadrados = []
    for i in lista_errores:
        lista_errores_cuadrados.append(pow(i, 2))

    denominador = np.mean(valor_real)
    if denominador == 0:
        denominador = 1
    return (np.sqrt(np.mean(lista_errores_cuadrados))) / denominador

def media_desde_histograma(histograma, n):
    return sum(histograma * range(0, 126)) / n
