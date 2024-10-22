import random, time, paho.mqtt.client as mqtt

# Parámetros del servidor MQTT
MQTT_HOST = "18.100.158.114"
MQTT_PORT = 1883
MQTT_USER = "sinf"
MQTT_PASSWORD = "HkxNtvLB3GC5GQRUWfsA"
MQTT_TOPIC = 'Alice_'
chequeo = False

#Funcion para verificar la conexion al mqtt
def on_connect(client, data, flags, returnCode):
    if returnCode == 0:
        print('Bob is connected...')
    else:
        print(f'Connection error: {str(returnCode)}')
        
#Funcion para detectar si se recibio un mensaje 
def on_message(client, data, mensaje):
    global mensaje_, chequeo
    chequeo = True
    print(f'Alice envio: {mensaje.payload.decode('utf-8')}')
    mensaje_ = mensaje.payload
    
#Funcion para colocar en modo escucha 
def listen():
    global chequeo
    while not chequeo:
        client.loop_start()
        client.loop_stop()
        time.sleep(1)
    chequeo = False
    
#Funcion para convertir los dato recibidos a vector
def mensaje_a_vec(x, l):
    print(f"x = {x}")
    print(f"l = {l}")
    y = x.decode('utf-8')
    return [int(y[i]) for i in range(l)]

#Funcion para crear el generador pseudo aleatorio con input de la semilla
def g_de_s(s_recibido):
    s_ = int("".join(map(str,s_recibido)),2)
    random.seed(s_)
    Gs_bob = [random.randint(0,1) for i in range (0, 2*q)]
    return Gs_bob

# Separar Gs en grS y gnoRs según las posiciones de r
def separa_G_s(G_S_bob, r) -> tuple:
    grS = [G_S_bob[i] for i in range(len(G_S_bob)) if r[i] == 1]
    gnorS = [G_S_bob[i] for i in range(len(G_S_bob)) if r[i] == 0]
    return grS, gnorS

# Calcular e como el XOR entre gnoRs y c
def Calculo_e(grS, c_bob) -> list:
    return [g ^ cb for g, cb in zip(grS, c_bob)]

# Configuración del cliente MQTT para Bob
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT)
client.subscribe(MQTT_TOPIC)

#Escucha del primer mensaje de Alice
listen()
m = int(mensaje_, 10)

q = m + m + m

#Se genera el vector r y se le envia a Alice
r = [0] * q + [1] * q
random.shuffle(r)
print(f"r es:{r}")

#Conversion de r en string para enviar a Alice
r_enviar = ''.join(map(str,r))
client.publish('Bob_', r_enviar)

#Escucha del segundo mensaje de Alice
listen()
e_recibido = mensaje_a_vec(mensaje_, len(mensaje_))
print(f'El e recibido es:\n{e_recibido}')

#Escucha del tercer mensaje de Alice
listen()
s_recibido = mensaje_a_vec(mensaje_, len(mensaje_))
print(f'Semilla recibida:\n{s_recibido}')

#Escucha del cuarto mensaje de Alice
listen()
b_recibido = mensaje_a_vec(mensaje_, len(mensaje_))
print(f'b recibido:\n {b_recibido}')

#Escucha del quinto mensaje de Alice
listen()
gnorS_recibido = mensaje_a_vec(mensaje_, len(mensaje_))
print(f'GnorS recibido:\n {gnorS_recibido}')

#Asignacion de valores correspondientes a las variables segun enunciado o resultado de funciones
c_bob = b_recibido + b_recibido + b_recibido
print(f"c_bob es:\n {c_bob}")

G_S_bob = g_de_s(s_recibido)
print(f"G(s)_bob : \n {G_S_bob}")

grS, gnorS = separa_G_s(G_S_bob, r)
print(f"grS (elementos de G_s donde r es 1):\n, {grS}")
print(f"gnorS (elementos de G_s donde r es 0):\n{gnorS}")

e_bob = Calculo_e(grS, c_bob)
print(f"e_bob (resultado del XOR):{e_bob}")


# # Verificación del compromiso
if e_bob != e_recibido:
    print(f'El compromiso es corrupto, Alice es deshonesta')
    client.publish('Bob_', "El comprimiso es corrupto, Alice no es honesta")
else:
    print(f'El compromiso se cumple, Alice es honesta')
    client.publish('Bob_', "El Compromiso se cumple")
    if gnorS !=gnorS_recibido:
        print(f'La Semilla ha sido modificada, Alice hizo trampa')
        client.publish("Bob_","La Semilla ha sido modificada, Alice hizo trampa")
    else:
        print(f"La semilla coincide, Alice no hizo trampa")
        client.publish('Bob_',"La semilla coincide, Alice no hizo trampa")
        
        