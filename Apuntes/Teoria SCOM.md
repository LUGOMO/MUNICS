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
- RSA (No presente en TLS v1.3), es el mas simple usa un premaster secret aleatorio, encripta con la llave publica del servidor y la envia en el ClientKeyExchange. (No proporciona forward secrecy)
- DHECDE, Puede derivar una llave secreta sobre un canal inseguro, ambos lados deben estar autenticados para evitar ataques MITM    