# TLS (Transpor Layer Security Protocol)
Es una evolución de SSL (Secure Socket Layer) para proporcionar comunicaciones seguras sobre infraestructura insegura.
Proporciona un canal seguro a un servicio de Internet arbitrario, garantiza autenticacion, confidencialidad e integridad.
## TLS dentro de la arquitectura de Internet.
### TLS Record Protocol
Es la capa mas baja del protocolo TLS, se encarga de fragmentar los datos de aplicación, cifrarlos y autenticarlos, encapsularlos en una estructura fija, y transmitirlos de forma segura sobre TCP.

En general es un contenedor seguro que divide la información en fragmentos, los cifra, acompaña con metadatos estructurados y los entrega a TCP para su envió.
### Fases del Protocolo 1.3

	Client                                     Server
	  | ---- ClientHello (DH, suites, ext) ----> |
	  | <---- ServerHello (DH, suite) -----------|
	  | <---- EncryptedExtensions, Certificate --|
	  | <---- CertificateVerify, Finished -------|
	  | ---- Finished --------------------------> |
--------A partir de aquí se empieza a usar cifrado de aplicación con las claves derivadas.----
	   | ===== Encrypted Application Data ======> |

- **Handshake**
	- Usa Diffie-Hellman Ephmeral (DHE/ECDHE), para generar una clave compartida con forward secrecy.
	- Elimina RSA key exchange
	- El Cliente envía:
		- ClientHello, lista de las suites soportadas, clave publica DH, extensiones como SNI (server name indication) ALPN(Application-Layer Protcol Negotiation), etc.
	- El servidor responde:
		- ServerHello, suite de cifrado elegida, clave publica DH propia, certificado
	- Derivan la shared secret y la usan para proteger el resto del handshake.
- **Key Derivation**
	- Se usa HKDF (HMAC-based Key Derivation Function) sobre la shared secret para derivar:
		- Traffic secrets
		- Application Keys
- Data Transfer
	- Toda la comunicación va cifrada con AEAD ciphers AES-GCM o ChaCha20-Poly1305
	- No hay mas renegociación de sesion 
## Concepto
Es un protocolo criptográfico que proporciona confidencialidad, integridad y autenticacion de las comunicacion entre aplicaciones que usan la red, típicamente sobre TCP

Opera entre la capa de transporte (TCP) y la capa de aplicación (HTTP,SMTP, etc).
## Objetivo
- Interoperabilidad, ya que no depende de ningún OS o lenguaje de programación
- Extensibilidad, independiente de primitivas criptográficas (garantiza confidencialidad basándose únicamente en que la función de cifrado es segura, sin importar cual se use)
- Eficiencia, minimiza el coste de rendimiento sobre la comunicacion.
## Linea Temporal
- 1994 SSL1, nunca vio la luz del día.
- 1994 SSL2, Utilizado en Netscape Navigator 1.1, se introduce uso de certificados de servidor.
- 1996 SSL3, Rediseño completo, soporte para PKI mediante certificados X.509.
- 1999 TLS 1.0, Estandariza SSL3, cambio de nombre para complacer a Microsoft, no interoperable.
- 2006 TLS 1.1, Ajustes de seguridad y extensiones TLS.
- 2008 TLS 1.2, Version mas comun y flexible.
- 2018 TLS 1.3, Mejoras de rendimiento y simplificación del protocolo.
## Competidores 
- SSH (Secure Shell)
	- Opera en capa de aplicacion TCP/IP
	- Puede usar contraseñas o utilizar criptografia de llave publica.
	- Se basa en sistema de confianza con hosts conocidos e intercambio de claves en vez de PKI.
	- Se suele utilizar para, acceso remoto, transferencia de archivos, y protocolos de tunelizacion.
- PGP (Pretty Good Privacy)
	- Opera en mensaje a mensaje (offline)
	- Decentralized Web of trust (Cada usuario es responsable de verificar las claves publicas de otros y firmarlas si confía en ellas) en vez de PKI jerárquico.
	- Se suele utilizar en, emails, archivos, verificación de paquetes de software.
## Protocolo TLS (v1.2 y v1.3)
### Record Protocol
Transporta y encripta (opcionalmente) cada mensaje TLS entre dos aplicaciones.

Un TLS Record, se compone de:
- Header
	- Type
	- Version
	- Length
- Data
Todo esto conforma el Record TLS, adicionalmente hay un contador de 64 bits que TLS usa internamente como nonce para cada registro cifrado que no se transmite en la red.

El record Protocol se encarga de:
- Transporte del mensaje, transfiere bloques de datos opacos proporcionados por capas superiores del protocolo (TLS no interpreta ni modifica el contenido, , solo lo protege la información proporcionada por las capas de aplicación y los envia por TCP)
- Encriptacion y validacion de integridad, los primeros mensajes son transferidos en claro, luego que el handshale termina (v1.2) lo encripta y valida de acuerdo a los parametros negociados.
- Compresion, esta tarea ya no se realiza debido a los ataques laterales de compresion.
- Extensibilidad, el protocolo solo se encarga del transporte y el encriptado.
### Handshake Protocol
Es el encargado de negociar los parametros de conexion y realiza el proceso de autenticacion
- Intercambia entre 6 y 10 mensajes dependiendo de las especificaciones que demanda el extremo
 #### Flujos comunes
 - Full handshake con el servidor de autenticacion
 - Abbreviated handshake, para restablecer una sesion previa
 - Full handshake con autenticacion mutua.
#### Full Handshake
- Intercambio de capacidades y parámetros de negociación
- Autenticación (valida los certificados presentados
- Acordar el master secret para proteger la sesió
- Verificar la integridad de los mensajes del saludo
Etapas:
- Cliente envía "Client Hello":
- Servidor responde con "Server Hello":
- Servidor envía su certificado digital:
- Servidor envía una clave pública:
- Servidor indica el final de la negociación.
- Cliente envía información adicional para generar el master secret.
- Cliente cambia a cifrado con la clave negociada.
- El cliente envía un MAC final con un hash de todos los mensajes.
- Servidor cambia a cifrado con la clave negociada.
- Servidor envía un MAC final con un hash de todos los mensajes.
En el Client Hello aparecen campos importantes:
- Random: Previene los ataques de repetición y asegura integridad.
- Session ID: Vacío en la primera conexión.
- Cipher Suites: Ordenadas por preferencia.
##### Client Hello
Lista de las suites soportadas, clave publica DH, extensiones como SNI (server name indication) ALPN(Application-Layer Protcol Negotiation), etc.
##### Server Hello
Suite de cifrado elegida, clave publica DH propia, certificado
##### Intercambio de Claves y Certificados
- Mensaje del certificado
	- El mensaje lleva el certificado X.509 del servidor, primero el principal y luego los intermedios.
	- No se debe  enviar nunca el certificado raiz.
	- El certificado depende de la cipher suite (los algoritmos de cifrado deben coincidir)
	- El servidor se puede configurar con varios certificados.
- Intercambio de clave
	- El contenido depende de la cipher suite establecida.
	- El ClientKeyMessage es obligatorio.
	- El ServerKeyExchange es opcional.
##### Protocolo Change Cipher (No esta presente en v1.3)
No esta presente en v1.3, solo contiene un mensaje "ChangeCipherSpec"
- Se envía durante el handshake para indicar:
	- El cliente o servidor tiene suficiente informacion para generar las claves de encriptado.
	- El resto de mensajes se encriptaran.
##### Cierre del handshake
- Mensaje "Finished"
	- Es el primer mensaje encriptado, permite verificar la integridad del handshake.
	- Tiene un campo, "verify_data" es un hash (criptográfico) de todos los mensajes del handshake mezclado con la master secret
#### Full Handshake Mutual
##### Petición del Certificado
- Necesita que el servidor este autenticado
- Puede limitar los algoritmos de firma, llave publica y autoridades certificadoras aceptables.
##### Verificación del certificado
Es una firma de un handshake previo para comprobar la posesión de la llave privada del certificado.

En general la diferencia con el Full Handshake es:
- El servidor solicita al cliente el certificado.
- El cliente envía el certificado.
- El cliente envía una firma de los mensajes anteriores en el handshake para verificar que posee la clave privada del certificado
### Handshake TLS v1.3
- Introduce mejoras en el proceso de handshake, eliminando redundancias y mejorando la seguridad.
	- Principales diferencias:
		- Menos mensajes en el handshake (pasa de 4 a 3 rondas), 5 mensajes (CH + Key_share, SH + KeyShare, SCert, Fin, Fin).
		- Elimina el uso de claves RSA estáticas, obligando a usar Diffie-Hellman Ephemeral (DHE) o Pre-Shared Keys (PSK) lo que mejora la seguridad.
#### Abbreviated Handshake (Resumen de Sesion)
TLS permite reestablecer una sesion si ya anteriormente hubo una sesion establecida previamente.

El Cliente envia un ID de sesion en el Client Hello, el servidor lo devuelve y se realiza un nuevo set de claves para reanudar el trafico.

Existe una alternativa, "tickets de sesion" que almacena toda la informacion del cliente.

Los servicios simetricos son mas pesados que los asimetricos.
### Intercambio de Claves
- RSA (No presente en TLS v1.3), es el mas simple usa un premaster secret aleatorio, encripta con la llave publica del servidor y la envia en el ClientKeyExchange. **(No proporciona forward secrecy)**
- DHECDE, Puede derivar una llave secreta sobre un canal inseguro, ambos lados deben estar autenticados para evitar ataques MITM   
	- Hay dos variaciones:
		- Statich (DH) (No se usa en v1.3), rara vez utilizado, el servidor reusa paramteros. por lo que la llave siempre es la misma, **(No proporciona Forward Secrecy)**
		- (EC) Ephemeral (DHE), los parametros cambian en cada conexion diferente, **(Proporciona Forward Secrecy)**
***Forward Secrecy o secreto a futuro establece que si se filtra o roba la clave privada de un servidor, los mensajes que tú y ese servidor intercambiaron en el pasado seguiran protegidos.***
### Autenticación
Usualmente se utiliza algun tipo de criptografia de llave publica, comunmente RSA aunque tambien se usa ECDSA (Eliptic Curve Digital Signature Algorithm).
- El cliente obtiene y valida el certificado del servidor
	 Dependiendo de que algoritmo se utilice
	- RSA, el cliente encripta la premaster secret con la llave publica del servidor. El servidor se autentica solo si el mensaje "**Finished**" que recibe del cliente es correcto
	- ECDSA, El servidor comunica los parametros firmados con su propia clave privada. Dichos parametros son concatenados con valores aleatorios para evitar ataques de repeticion.
### Encriptado
Pueden usarse varios cifrados, 3DES, AES. ARIA. CAMELIA, RC4 y SEED

#### Tipos de encriptado
###### Stream Encryption
Se genera un flujo de claves operadas con los datos usando XOR

La estructura consiste en:

Header | Ciphertext 
- Donde Ciphertext esta compuesto por Plaintext | MAC (Aqui ocurre el encriptado)
- Que a su vez MAC esta compuesto por Sequence Number | Header | Plaintext (Aqui ocurre la autenticacion)

**El Header esta incluido en la MAC para proteger la integridad del mensaje completo, el MAC (Message Authentication Code) detecta si alguien modifico el contenido o el contexto del mensaje, por lo que incluir el Header en el MAC garantiza que nadie pueda cambiar el tipo de mensaje, que la version TLS usada no se altera, y el receptor puede saber si el mensaje fue recortado o alargado*

**El Sequence Number, se usa como entrada para calcular el MAC, sin embargo este no se envia en el paquete, sirve para evitar ataques de reordenamiento o duplicacion de mensajes**
##### Block Encryption
Divide los datos en bloques de tamaño fijo y se realizan las operaciones de cifrado usando los bloques de entrada como entrada de los siguientes. Se utiliza CBC o EMAC.

La estructura consiste en:

Header | IV | Ciphertext
- Ciphertext: Plaintext | MAC | Padding (Aqui ocurre el encriptado)
- MAC: Sequence Number | Header | Plaintext (Aqui ocurre la autenticacion)

Este tipo utiliza CBC Mode (Cypher Block Chaining)
A partir de TLS 1.1, el IV es unico por cada registro, evitando ataques de prediccion del IV (TLS 1.0)
###### Authenticated Encryption With Associated Data (AEAD)
Realiza cifrado y autenticacion en una sola operacion criptografica.

La estructura consiste en:

Header | Nonce | Ciphertext

Utiliza los modos CBC-MAC (CCM) y Galois Counter Mode (GCM)
Es el preferido en la actualidad
Solo disponible en v1.3

### Cierre de conexión
TLS, utiliza el subprotocolo de alertas para cerrar la conexión de forma segura

Niveles:
- Fatal, la conexión se cierra de inmediato
- Warning, transporta una descripción, donde el receptor puede emitir una alerta "fatal" como respuesta. El mensaje "Close Notify" sirve para cerrar de manera correcta la conexión TLS, si este no se recibe puede haber un ataque de truncado.
### Operaciones Criptograficas
#### PRF (Pseudo Random Function)
Una funcion pseudoaleatoria genera cantidades arbitrarias de datos pseudoaleatorios. En TLS v1.2 se utiliza Hash-based MAC (HMAC) y en TLS v1.3 se utiliza HKDF
#### Master Secret
Se deriva del **premaster secret** mediante una PRF, se utilizan campos aleatorios para garantizar la aleatoriedad, tiene 48 bytes (384 bits) de longitud.

### Generacion de Claves

Para la generacion de claves se utiliza como parametros:
- Premaster Key
- Master Secret
- Client Random
- Server Random

Estos son los parametros de la PRF que produce la **Master Key**.

Luego la Master key se concatenacon:
- "key expansion"
- Client random
- Server Random

Cuya salida se vuelve a usar como parametros de otra PRF que produce el **Key Block** que esta conformado por:
- Encrypt Key 1
- Encrypt Key 2
- Mac Key 1
- Mac Key 2
- IV 1
- IV 2

En resumen
**Generación del Master Secret:**
Master Secret = PRF(Premaster Secret, "master secret", ClientRandom || ServerRandom)
**Generacion del Key Block:**
Key Block = PRF(Master Secret, "key expansion", ServerRandom || ClientRandom)
### Cipher Suites
Es una seleccion de primitivas criptograficas y parametros, en otras palabras es un conjunto de algoritmos que define como se protegera la conexion segura entre Cliente y Servidor.
# PKI (Public Key Infraestructure)
Su meta es permitir que personas que nunca se han conocido se comuniquen de manera segura.

Su objetivo es acceder a las claves publicas, obtener informacion acerca de la validez de esas claves (concepto de revocacion) y que sea escalable.

Internet PKI, se basa en el uso de entidades de terceros confiables o tambien conocidas como CA (Certification Authorities), estas generan certificados mediante el almacenamiento de claves publicas.
## X.509
Es un estandar internacional de llaves publicas (PKI) adaptado para el uso en Internet.
### Timeline
- PKIX (Public Key Infraestructure for X.509) se conformo para adaptar las ITU-T a X.509
- CA/Browser Forum (CAB Forum), coordina y estandariza la relacion entre navegadores CA y OS
- IETF Web PKI, describe el comportamiento de PKI en la web

## Campos del Certificado
- Version: 1.2 o 3 (Actualmente casi todos usan v3)
- Numero de serie: numero unico, no secuencial con al menos 20 bit aleatoriedad.
- Algoritmo de firma, el que se implento para firmar el certificado
- Emisor: DN del emisor del certificado
- Validez: fecha de inicio y final de la validez del certificado
- Subject: DN de la entidad propietaria de la llave publica certificada.
- Clave Publica: ID del algoritmo, parametros opcionales y la clave en si.
### Extensiones del certificado
- Nombre alternativo del Subject: Permite multiples identidades, especificadas por el nombre de DNS, direcciones IP o URL, reemplaza el campo "Subject".
- Limitaciones de nombre: Limita las identidades a las que la CA puede certificar.
- Limites Básicos: Limita la profundidad maxima en la cadena de confianza, indica cuantos niveles de CAs subordinadas se pueden emitir debajo.
- Uso de claves: define para que puede usarse la clave publica del certificado (lista de permisos).
- Uso de claves extendido:  refina aun mas los usos de manera mas especifica de la clave publica.
- Políticas de certificado: son enlaces que remiten a documentos o lineamientos que indican como se valido la identitada, garantias del certificado, para que se puede usar legal o contractualmente el certificado.
- Puntos de distribución CRL: Ubicación de la lista de revocación.
- Información de acceso de autoridad: Varias URIs, entre ellas la ubicación del OSCP responder.
- Clave de identificación del Subject: Usualmente es un hash, utilizado para identificar de manera única la llave publica.
- Clave de identificación de la autoridad: Hash de la clave que firmo el certificado.
### Ciclo de Vida de los Certificados

#### Solicitud de emisión del Certificado
- Subscriber: Genera una solicitud de firma de certificado que contiene su información y clave publica.
- Registration Authority: Recibe el CSR (Request Certificate Issuance) y realiza la validación de la entidad del solicitante.
- Certification Authority: Es la autoridad que emite el certificado
#### Validacion
- Validate Subscriber Identity: La RA o CA, verifican la identidad del solicitante según sus políticas
#### Emision
- Issue Certificate: Una vez se valido, la CA firma digitalmente el certificado con su clave privada.
#### Publicación del Certificado
Se publica en varios lugares:
- Web Server: Para autenticacion SSL o TLS
- CRL Server: Para la listas de revocación.
- OCSP Responder: Servicio de verificación de estado online.
#### Proceso de Verificación
- 1 Request Certificate: Solicita al servidor web el certificado
- 2 Verificación de firma: Valida que la firma de la CA es valida o no.
- 3 Verificación de revocación: Consulta CRL u OCSP para verificar si ha sido revocado o no.
- Relying Party: Confía si pasa todas las verificaciones.
## Internet PKI Infraestructure
### Solicitud de Firma del Certificado
Lleva la clave publica del solicitante, con la finalidad de demostrar la veracidad de la clave privada correspondiente
### Validación de la identidad del suscriptor
#### Estrategias de Validación
- Dominio, Prueba de control de un dominio determinado, envía un correo a una dirección desconocida o un registro de la zona de dominio.
- Organización, Requiere de validación de identidad y autenticidad, verifica inconsistencias en procedimientos o en codificación de la información.
- Ampliada, Requiere validación de identidad y autenticidad con requisitos muy estrictos.
### Revocación
Se realiza cuando hay sospecha que la clave privada ha sido comprometida, o el certificado ya no se necesita.

Se puede comprobar con las CRL o de manera online con OCSP, ambas permiten a las partes involucradas verificar el estado.
### Cadenas de certificados
Es el camino de confianza entre el certificado con una autoridad certificadora en la que confía el OS.

El Root CA va embebido en el SO o navegador, los certificados intermedios y finales son proporcionados por el servidor.
#### Justificación de las cadenas de certificados
- Seguridad de la clave raíz de la CA: Es critico, si se revoca todos los certificados deben ser emitidos nuevamente, esta clave debe mantenerse siempre offline.
- Certificación Cruzada: una nueva clave raíz es firmada por la antigua mientras se despliega en OS y navegadores.
- Compartimentar: Dividir una raíz entre múltiples CA subordinadas para reducir riesgos.
- Delegación: Una gran empresa puede querer emitir sus propios certificados, una CA puede emitir un certificado subordinado, pudiendo este certificado estar restringido.
### Partes de Confianza
Debe de confiarse en una colección de certificados CA raíces, OS, o navegadores.
- Apple y Microsoft, La CA debe pasar una auditoria anual.
- Mozilla, Usa un programa transparente de certificados raíz.
- Chrome, Usa el almacenamiento de certificados del OS, aplica listas blancas y negras.
## Problemas con la PKI actual infraestructura
### Control de la emisión de certificados por los propietarios de dominios
Cualquier CA puede emitir un certificado para un dominio sin permiso o notificación del propietario, esto puede ser negligencia o malicia.

Existen cientos de CA, por lo que una sola comprometida podría vulnerar la seguridad.

### Dificultad actualizando los almacenes de confianza
Se dice que la mayoría de CAs son muy "grandes" para fallar, eliminar una CA tiene consecuencias a gran escala por lo que usualmente no ocurre.

Las CAs raíz se confía o no, se puede prohibir certificados CA desde una fecha especifica, o remover privilegios EV.
### Revocación fallida
#### Razones
- Retardo en la propagación de información, la información en CRL y OSCP pueden mantenerse valido hasta 10 días.
- Los navegadores ignoran fallos en la comunicacion de CRL y OSCP.
- Los navegadores por defecto no verifican chequeos de revocación debido a muchos errores y alta latencia.

Como medida provisional la mayoría de navegadores utilizan mecanismos de listas negras de certificados e intermediarios revocados.
#### Otras debilidades
- Validación de dominio débil, implementado por emails inseguros o utilizando datos "whois" inseguros.
- Advertencias de certificado, Muchas aplicaciones se saltan la validación de certificados, y navegadores permiten el uso de certificados no verificados.
## Mejoras de la Infraestructura
### Notaries
Repositorios públicos de certificados conocidos, esto puede impedir ataques basados en intermediarios maliciosos.
### Fijación de claves publicas HPKP
Permite a los dueños restringir que CAs pueden emitir certificados para sus dominios.

Actualmente esta obsoleto.
### Transparencia de Certificados
Busca identificar rápidamente certificados fraudulentos, es un framework que permite verificar la emisión de certificados, bajo CT todas las CA participantes deben aplicar todos los certificados emitidos a un log publico.

Cualquiera puede monitorizar la emisión de certificados, las CA obtienen una prueba digital firmada como prueba de entrega.

# PBNAC (Port-Based Network Access Control)
## IEEE 802.1X
Es un estandar IEEE para el control de puertos basado en control de acceso, proporciona un mecanismo de autenticacion a dispositivos que quieren conectarse por LAN o WLAN.

Los puertos del SW por defecto estan bloqueados hasta que el dispositivo conectado se autentique, mientras tanto solo paquetes especificos son transmitidos para poder implementar la autenticacion, en WiFi su equivalente sera la asociacion inicial con el AP.

Se necesitan de 3 partes involucradas, el suplicante (dispositivo del cliente), un autenticador (SW o AP) y un servidor de autenticacion.
## EAP (Extensible Authentication Protocol)
Es un framework de autenticacion L2 (Capa 2 OSI Enlace de Datos), por lo que no es un un mecanismo de autenticacion especifico, este propociona funciones comunes de metodos negociacion de autenticacion llamado EAP Methods.

La autenticacion es realizada por el protocolo interno a EAP, no es realizada por EAP.

