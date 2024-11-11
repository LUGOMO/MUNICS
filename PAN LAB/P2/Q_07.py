import lab02_utilitis, numpy, pandas
import matplotlib.pyplot as plt

# Bases de datos:
databases_sizes = [101, 1001, 10001]

# Realizaremos el proceso de cálculo para cada tamaño de base de datos
for n in databases_sizes:
    # Variables iniciales que iremos empleando
    # Lista de valores reales:
    mean_list = []
    median_list = []
    bitcount_list = []
    histogram_list = []

    # Lista de errores:
    q1_error = []
    q2_error = []
    q3_error = []
    q4_error = []

    # En primer lugar, deben crearse 100 bases de datos
    # Luego, se calculan la media, mediana, bitcount e histograma junto con los errores obtenidos al aplicar laplace
    for i in range(0, 100):
        # Creación de base de datos
        db = lab02_utilitis.base_datos_aleatoria(n)
        # epsilon
        epsilon = 1

        # Cálculo de valores reales
        mean_list.append(numpy.mean(db.Edad))  
        median_list.append(numpy.median(db.Edad)) 
        bitcount_list.append(lab02_utilitis.conteo_bits(db)) 
        histogram_list.append(lab02_utilitis.histograma(db))
        
        # Cálculo de errores para cada función que aplica epsilon-DP
        # q1
        q1_error.append(lab02_utilitis.q1(db, epsilon) - mean_list[i])
        # q2
        q2_error.append(lab02_utilitis.q2(db, epsilon) - median_list[i])
        # q3
        bitcount_with_noise = lab02_utilitis.q3(db, epsilon)
        bit_error = []
        for x in range(0, len(bitcount_with_noise)):
            bit_error.append(bitcount_with_noise[x] - bitcount_list[i][x])
        q3_error.append(bit_error)
        # q4
        hist_with_noise = lab02_utilitis.q4(db, epsilon)
        hist_error = []
        for x in range(0, len(hist_with_noise)):
            hist_error.append(hist_with_noise[x] - histogram_list[i][x])
        q4_error.append(hist_error)
    
    # Una vez calculados los valores para cada base de datos (valor real y error) se procede al calculo de NRMSD

    # Se almacenan los resultados de forma que sea más simple su uso
    q3_error = pandas.DataFrame(q3_error)
    q4_error = pandas.DataFrame(q4_error)

    bitcount_df = pandas.DataFrame(bitcount_list)
    histogram_df = pandas.DataFrame(histogram_list)

    # Se establecen 2 listas: una con los errores y otra con los valores reales
    list_of_errors = [q1_error, q2_error, q3_error, q4_error]
    list_of_real_values = [mean_list, median_list, bitcount_df, histogram_df]

    # Y se inicializa el diccionario donde se almacenarán los resultados
    list_of_nrmsd = {}

    # Para cada elemento de la lista de errores y de valores reales:
    for x in range(0, len(list_of_errors)):
        # Si es un dataframe (es decir, si son listas de errores/resultados reales)
        if isinstance(list_of_errors[x], pandas.DataFrame):
            # Se aplica un bucle sobre cada elemento, calculando así el NRMSD para cada uno de ellos
            temp_list = []
            for i in list_of_errors[x].columns:
                temp_list.append(lab02_utilitis.nrmsd(list_of_errors[x][i], list_of_real_values[x][i]))

            # El resultado de NRMSD en cada elemento se almacena en el diccionario
            list_of_nrmsd["q" + str(x + 1)] = temp_list

        # En el resto de casos, el valor proporcionado es un float
        else:
            # El resultado de NRMSD se almacena en el diccionario
            list_of_nrmsd["q" + str(x + 1)] = lab02_utilitis.nrmsd(list_of_errors[x], list_of_real_values[x])

    # Plot del histograma
    plt.plot(range(0, 126), list_of_nrmsd["q4"])
    plt.title("Valores histogramas para n = " + str(n))
    plt.savefig('n' + str(n) + 'hist.png')
    plt.close()
    
    print("Para bases de datos con n =", n)
    print("\tNRMSD_q1 respecto a la media real es", list_of_nrmsd["q1"])
    print("\tNRMSD_q2 respecto a la mediana real es", list_of_nrmsd["q2"])
    print("\tNRMSD_q3 respecto al bitcount real es {", list_of_nrmsd["q3"][0], "[SB1] y ", list_of_nrmsd["q3"][1], "[SB2] }")
    print("\tNRMSD_q4 disponible en n" + str(n) + "hist.png")
