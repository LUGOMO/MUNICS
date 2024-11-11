import lab02_utilitis, numpy, pandas
import matplotlib.pyplot as plt

# Bases de datos:
databases_sizes = [101, 1001, 10001]

# Realizamos el proceso de cálculo para cada tamaño de base de datos
for n in databases_sizes:
    # Variables iniciales que iremos empleando
    mean_list = []
    median_list = []
    bitcount_list = []
    histogram_list = []

    # Lista de errores:
    q1_error = []
    q2_error = []
    q3_error = []
    q4_error = []

    # Generamos 100 bases de datos y realizamos los cálculos
    for i in range(0, 100):
        # Creación de base de datos aleatoria
        db = lab02_utilitis.base_datos_aleatoria(n)
        epsilon = 1

        # Cálculo de valores reales
        mean_list.append(numpy.mean(db.Edad))  
        median_list.append(numpy.median(db.Edad))
        bitcount_list.append(lab02_utilitis.conteo_bits(db))
        histogram_list.append(lab02_utilitis.histograma(db))
        
        # Cálculo de errores para cada función que aplica epsilon-DP
        # Q1: Media
        q1_error.append(lab02_utilitis.q1(db, epsilon) - mean_list[i])

        # Q2: Mediana
        q2_error.append(lab02_utilitis.q2(db, epsilon) - median_list[i])

        # Q3: Conteo de bits
        bitcount_with_noise = lab02_utilitis.q3(db, epsilon)
        bit_error = [bitcount_with_noise[x] - bitcount_list[i][x] for x in range(0, len(bitcount_with_noise))]
        q3_error.append(bit_error)

        # Q4: Histograma
        hist_with_noise = lab02_utilitis.q4(db, epsilon)
        hist_error = [hist_with_noise[x] - histogram_list[i][x] for x in range(0, len(hist_with_noise))]
        q4_error.append(hist_error)

    # Cálculo de NRMSD
    q3_error = pandas.DataFrame(q3_error)
    q4_error = pandas.DataFrame(q4_error)

    bitcount_df = pandas.DataFrame(bitcount_list)
    histogram_df = pandas.DataFrame(histogram_list)

    # Definimos las listas para errores y valores reales
    list_of_errors = [q1_error, q2_error, q3_error, q4_error]
    list_of_real_values = [mean_list, median_list, bitcount_df, histogram_df]

    # Diccionario para almacenar NRMSD
    list_of_nrmsd = {}

    # Cálculo de NRMSD para cada consulta (Q1, Q2, Q3, Q4)
    for x in range(0, len(list_of_errors)):
        if isinstance(list_of_errors[x], pandas.DataFrame):  # Si es un DataFrame (Q3 y Q4)
            temp_list = [lab02_utilitis.nrmsd(list_of_errors[x][i], list_of_real_values[x][i]) for i in list_of_errors[x].columns]
            list_of_nrmsd["q" + str(x + 1)] = temp_list
        else:  # Si es un float (Q1 y Q2)
            list_of_nrmsd["q" + str(x + 1)] = lab02_utilitis.nrmsd(list_of_errors[x], list_of_real_values[x])

    # Gráfico del histograma (Q4) en modo de barra
    plt.bar(range(0, 126), list_of_nrmsd["q4"])
    plt.title("Valores histogramas para n = " + str(n))
    plt.xlabel("Edad")
    plt.ylabel("NRMSD")
    plt.savefig('n' + str(n) + 'hist.png')
    plt.close()

    # Resultados de NRMSD para las demás funciones (Q1, Q2, Q3) en una tabla
    print("Para bases de datos con n =", n)
    print("\tNRMSD_q1 respecto a la media real es", list_of_nrmsd["q1"])
    print("\tNRMSD_q2 respecto a la mediana real es", list_of_nrmsd["q2"])
    print("\tNRMSD_q3 respecto al bitcount real es {", list_of_nrmsd["q3"][0], "[SB1] y ", list_of_nrmsd["q3"][1], "[SB2] }")
    print("\tNRMSD_q4 disponible en n" + str(n) + "hist.png")
