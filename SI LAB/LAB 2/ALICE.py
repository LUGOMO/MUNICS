import random, time, paho.mqtt.client as mqtt


# Parámetros del servidor MQTT
MQTT_HOST = "18.100.158.114"
MQTT_PORT = 1883
MQTT_USER = "sinf"
MQTT_PASSWORD = "HkxNtvLB3GC5GQRUWfsA"
MQTT_TOPIC = 'Bob_'
chequeo = False

#Funcion para verificar la conexion al mqtt
def on_connect(client, data, flags, returnCode):
    if returnCode == 0:
        print('Alice is connected...')
    else:
        print(f'Connection error: {str(returnCode)}')
        
#Funcion para detectar si se recibio un mensaje 
def on_message(client, data, mensaje):
    global mensaje_, chequeo
    chequeo = True
    print(f'Bob envio: {mensaje.payload.decode('utf-8')}')
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
    # print(f"x = {x}")
    # print(f"l = {l}")
    y = x.decode('utf-8')  # Decodificar directamente los bytes a una cadena
    return [int(y[i]) for i in range(l)]


# Configuración del cliente MQTT para Alice
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message

# Conectar y suscribirse al topic `
client.connect(MQTT_HOST, MQTT_PORT)
client.subscribe(MQTT_TOPIC)

# Se solicita el tamaño de m 
m = int(input('Define el tamaño de m \n')) #Alice decide el tamano de m
print(f"m es:\n {m}")

#Se envia a Alice el length de m
client.publish('Alice_', m)

#Escucha del primer mensaje de Bob
listen()
q = m + m + m #Al definir m, le asigna el tamaño a q ya que q=m+m+m 
print(f"q es:\n {q}")
#Definimos la longitud de r
r = [0] * (2*q) 
r_recibido = mensaje_a_vec(mensaje_, len(mensaje_))
print(f"r es:\n {r_recibido}")

#Generamos el vector b de forma aleatoria 
b = [random.randint(0,1) for i in range (0,m)] 
print(f"b es:\n {b}")

c = b + b + b
print(f"c es:\n {c}")

#Generamos la semilla de forma aleatoria
s=[random.randint(0,1) for i in range (0,10)]
print(f"La semilla s es:\n{s}")

# Generar el vector Gs usando la semilla s
def g_de_s(s):
    s_ = int("".join(map(str,s)),2)
    random.seed(s_)
    Gs = [random.randint(0, 1) for i in range(0, 2*q)]
    return Gs

G_s = g_de_s(s)
print(f"G(s) es :\n {G_s}")

# Separar Gs en grS y gnoRs según las posiciones de r
def separa_G_s(G_s, r_recibido) -> tuple:
    grS = [G_s[i] for i in range(len(G_s)) if r_recibido[i] == 1]
    gnorS = [G_s[i] for i in range(len(G_s)) if r_recibido[i] == 0]
    return grS, gnorS

grS, gnorS = separa_G_s(G_s, r_recibido)
print(f"grS (elementos de G_s donde r es 1):\n{grS}")
print(f"gnorS (elementos de G_s donde r es 0):\n{gnorS}")

# Calcular e como el XOR entre gnoRs y c
def Calculo_e(grS, c) -> list:
    return [g ^ cb for g, cb in zip(grS, c)]

e = Calculo_e(grS, c)
print(f"e (resultado del XOR):{e}")

#transformamos en bits y publicamos en el mqtt 
envio_e = ''.join(map(str,e))
print(f"e a enviar:{envio_e}")
client.publish('Alice_', envio_e)
time.sleep(2)

#Se solicita por pantalla si Alice desea modificar la semilla que envia a Bob
trampa = int(input('Desea modificar la semilla?  No (0) Si (1)\n'))
if trampa != 0:
    s[0] = s[0] ^ 1
    print(f"S modificado es:{s}")
#Envio de la semilla modificada o real, segun eleccion de alice
s_enviar = ''.join(map(str,s))
client.publish('Alice_', s_enviar)
time.sleep(3)

#Se solicita por pantalla si Alice desea modificar el bit commit que envia a Bob
trampa_ = int(input('Desea modificar b?  No (0) Si (1)\n'))
if trampa_ != 0:
    b[0] = b[0] ^ 1
    print(f"b modificado es:{b}")
#Envio del bit commit modificado o real, segun eleccion de alice    
b_enviar = ''.join(map(str,b))
client.publish('Alice_', b_enviar)

#Envio del gnoRs a Bob
gnorS_enviar = ''.join(map(str,gnorS))
client.publish('Alice_', gnorS_enviar)

#Escucha del segundo mensaje de Bob, para saber que concluye de la informacion enviada
listen()
listen()


