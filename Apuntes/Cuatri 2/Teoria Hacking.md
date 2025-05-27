# Fundamentos

## Test de Penetración
### Definición y Alcance
Consiste en realizar pruebas ofensivas contra los mecanismos de defensa existentes en el entorno que se analiza.

Consiste desde análisis de dispositivos físicos y digitales, como el factor humano mediante ingeniería social.

El objetivo es verificar bajo situaciones extremas cual es el comportamiento de los mecanismos de defensa, buscamos vulnerabilidades en los mismos, falta de controles y brechas que puedan existir entre la informacion critica y los controles existentes.

Un Pentest recrea las acciones ofensicas de un atacante para identificar posibles vulnerabilidades.

Con los resultados se realiza una documentación con los detalles que se obtuvieron en la auditoria, a partir de este documento se pueden/deben tomar acciones usándolo como guía

### Hackers
- White hat, especialistas de seguridad que intentan encontrar agujeros en la seguridad
- Black hat, buscan remuneriacion principalmente, pueden participar en espionaje, protestas o adictos al delito cibernetico
- Gray hat, Mezcla entre White y Black, buscan vulnerabilidades sin permiso de propietarios, y al encontrar pediran retribucion, en caso de no ser recompensado puede filtren dicha informacion y/o publiquen la vulnerabilidad para que el mundo la conozca.

### Hackers Vs Crackers
- Script Kiddies, hackers que utilizan programas escritos por otros para penetrar, tienen poco conocimiento de lo que hace a bajo medio o alto nivel en el codigo.
- Newbie, principiante inofensivo en busca de conocimientos de hacking
- Lammer, se cree hacker y no tiene los conocimientos ni la logica para comprender que es lo que realmente sucede cuando utiliza porgramas de otros para hackear o vulnerar

### Certificaciones 
- CEH (Certified Ethical Hacker)
- eJPTv2 (eLearn Security Junior Penetration Tester)
- OSCP (Offensive Security Certified Professional)
### Vulnerabilidades
Se considera una debilidad que podria conllevar a un fallo de seguridad
Clasificación:
- Tecnologica, fallos propios de las tecnologias utilizadas
- Configuracion, fallo conmumente humanos relativo a la configuracion de aplicativos y servicios disponibles
- Politica, por falta de esta o no bien definida
### Colecciones y Catálogos de Vulnerabilidades
- CWE (Common Weakness Enumeration)
- NVD (National Vulnerability Database)
- OWASP (Open Web Application Security Project)
### Ataques
La explotación de cualquier vulnerabilidad permitirá realizar un ataque 

Clasificación:
- Interrupción, impedimos el flujo normal de información
- Intercepción, capturamos información confidencial
- Modificación, modificamos información sensible afectando la integridad de los datos de la empresa
- Fabricación, agredimos la integridad añadiendo información falsa, por lo tanto afectando la autenticidad de la información.

### Amenazas
La finalidad de un test de penetración sera identificar las diferentes amenazas que están afectando a una determinada estructura empresarial

Clasificacion:
- Externas, ejecutadas desde fuera de la empresa
- Internas, provienen desde dentro de la empresa
- Estructuradas, planificadas con antelación
- No Estructuradas, no planificadas
### Vector de Ataque
Los vectores de ataque son las rutas o los medios utilizados para realizar dichos ataques

Un vector permite al atacante explotar o tomar ventaja de alguna vulnerabilidad o debilidad existente

Algunos Vectores:
- Redes Sociales, email, dispositivos móviles
- Software sin parches de seguridad
- Malware y Botnets
- Aplicaciones mal configuradas
- Complejidad de la infraestructura de red
- Políticas de seguridad inadecuadas

### Modalidades

Las auditorias se pueden clasificar según la información previa que proporciona la organización

- White Box, nos proporcionan información previa de forma detallada.
- Grey Box, nos proporcionan de información parcial de la organización
- Black Box, no tenemos ningún tipo de información proporcionada por la empresa.
### Fases
#### Reconocimiento
Es la etapa que mas tiempo suele demandar, se definen objetivos, se recopila toda la información posible que se utilizara en el resto de fases.

La información abarca:
- Nombres
- Direcciones de correo de empleados
- Topología de red
- Direcciones ip
- Etc
Hay dos tipos de reconocimiento
- Footprinting, es todo aquella recaudación que se realiza en medios o fuentes de acceso publico (shodan NameCHK Google/Bin Hacking)
- Fingerprinting, información que no es de dominio publico, información de la topología, direcciones y nombres a diferentes niveles, estado de puertos, versiones y estado de actualización de software y parches de SO, listado de vulnerabilidades, etc.........
#### Enumeración
Utilizando la información obtenida en el reconocimiento se buscan posibles vectores de ataque, esta etapa involucra escaneo de puertos y servicios y por ultimo se realiza el escaneo de vulnerabilidades que permitirá definir los vectores de ataque.
#### Análisis de Vulnerabilidades
Proceso donde evaluamos de que manera es posible realizar la explotación de las vulnerabilidades listadas, investigación de versiones debilidades etc
#### Acceso 
En esta etapa se realiza el acceso al sistema, explotando las vulnerabilidades detectadas y aprovechadas por el auditor para comprometer el sistema.
#### Persistencia o Mantenimiento de Acceso
Una vez obtenido acceso al sistema se busca preservar el sistema comprometido, a disposicion del atacante, se busca obtener un acceso perdurable en el tiempo

#### Borrado de rastro
El auditor de ser necesario elimina rastros de haber realizado acciones sobre el sistema para vulnerarlo.

### Blue Team Vs Red Team
- Blue Team, bloquea, detecta y previene ataques informaticos, se enfoca en la defensa
- Red Team, escanea detecta y explota vulnerabilidades, se enfoca en el ataque
- Purple Team, equipos altamente especializados con integrantes de ambos bandos red y blue team en conjunto, suele definirse como un Red team que entrena un Blue team.
### Conceptos 
#### Ingeniería Social
Obtención de información a traves de la manipulación de las personas, aprovechando que es el eslabón débil de la organización
### Wardriving
Obtención de una red de forma inalámbrica, ejecutado usualmente desde fuera de la sede de la organización con un portátil y un amplificador de señal WiFi.

### Equipo Robado
Comprobaciones de la información contenida en dispositivos portátiles y la problemática de la perdida o robo de alguno de ellos.


## Alcance de un Test de Penetración
- Prueba de intrusión de servicios externos
- Prueba de intrusión de servicios internos
- Prueba de intrusión mediante ingeniería social
- Prueba de intrusión de aplicaciones Web
- Prueba de intrusión de aplicaciones móviles
- Prueba de intrusión de integridad física
- Prueba avanzada de ataque persistente
- Arquitectura en la nube y análisis de la configuración de seguridad
- Análisis de la configuración de seguridad de equipos móviles
- Análisis de la seguridad de servidores de bases de datos
- Análisis de la seguridad de la infraestructura de redes
- Análisis de seguridad de la infraestructura de virtualización
- Prueba de intrusión de redes Wi-Fi
- Prueba de denegación de servicio
- Prueba de fugas de datos
- Identificación de datos confidenciales
- Revisión de código
- Ciberestafa
- Respuesta ante incidentes
- Informática forense

# Reconocimiento y Enumeración
### Footprinting
Lo principal es obtener una instantánea de los elementos observables de una red local
- Ip Activas
- Protocolos Usados
- Topología 
- Detección de IDS, IPS o Firewalls
### Fingerprinting
Una vez se identifican las maquinas disponibles debemos escanearlas para obtener información especifica referente a:
- Sistemas Operativos y Versiones
- Servicios activos y versiones
- Versiones de IDS o Firewalls
## Reconocimiento
### Activo: Consiste en la interacción directa con el objetivo
- Se tiene interacción activa o directa con la organización/victima
- Este proceso implica mas riesgo de detección que el reconocimiento pasivo, también conocido como rattling the doorknobs
Ejemplos:
- Barridos de ping
- Conexión a un puerto de alguna aplicación
### Pasivo: No tenemos interacción directa con el objetivo
- Obtenemos información mediante google, la pagina web, IP y/o numero de puertos abiertos.
- Sniffing es otro medio de reconocimiento pasivo, y puede proporcionar información util como rangos de direcciones ip, convención de nombres, servidores o redes ocultas, y otros servicios disponibles en el sistema o red.
### Capa de Enlace (Capa 2)
- El descubrimiento de esta capa suele hacerse mediante ARP, buscando descubrir servicios sin levantar sospechas.
	- Herramientas:
		- ARPing
		- Netdiscover
		- NMAP (+ NSE)
		- Metasploit
	- ARP traduce dirección de red en direcciones MAC
		- ARP se usa en direcciones IPv4
		- NDP (Neighbor Discovery Potocol), para direcciones IPv6
	- ARPing
		- Envía trama ARP en la capa de enlace como Ping hace en la capa de red.
		- Util en Maquinas con "Ping" deshabilitado (filtrado de paquetes ICMP)
		- Se utiliza para evitar detección por Firewalls básicos.
			Utilización: 
				- arping 192.168.56.6 -c 1 
	- NetDiscover (alternativa a ARPing)
		Podemos realizar búsquedas usando:
		- Interfaces: netdiscover -i eth0
		- Ficheros de entrada, netdiscover -l listaIP.txt
		- Rangos de IPs, netdiscover -r 192.168.56.0/24
		- Modo Pasivo, netdiscover -p (Tarda en exceso)
	- Nmap
		Permite evitar el envió de ping
		- Utilizando sondeo de lista (-sL)
		- Deshabilitando el ping (-Pn)
		- Enviando combinaciones arbitrarias de sondas TCP, SYN/ACK, UDP e ICMP a multiples puertos de la red remota
**Importante, ARP no atraviesa Routers, solo detectan sistemas dentro de la misma subred**
### Capa de Red (Capa 3)
- El descubrimiento en capa 3 esta basado principalmente en ICMP
	- fping
		Version optimizada de "ping" que permite escaneos simultáneos, en lugar de solo enviar a un objetivo hasta que venza el tiempo, enviara paquetes ping con un modelo round-robin
		- -a, muestra los sistemas en funcionamiento o "vivos"
		- -g, genera una lista desde la mascara de red IP proporcionada o un IP de inicio y finalización. Si se define mascara de red, las direcciones de red y broadcast serán excluidas del resultado.
	- hping3
		- Ademas de ICMP permite enviar TCP, UDP y RAW-IP (permite modificar cabeceras de paquetes IP)
		- Permite trazar rutas de conexión y evadir reglas de Firewalls
			- hping3 www.usc.es -t 1 --traceroute
		- Permite ejecutar ataques DDOS
			- hping3 --rand-source 192.168.56.4
			- hping3 --rand-source --flood 192.168.56.4
	- Nmap 
		Permite realizar un escaneo de red mediante el parámetro -sn
		- Como sucedía en capa 2, si estamos fuera de la red local o sin privilegios de administración se hace una petición ICMP Echo Request
		- Para evitar uso de ARP, --disable-arp-ping
### Capa de Transporte (Capa 4)
- Aquí utilizamos TCP / UDP
- Debemos distinguir entre descubrimiento de maquinas (descubrimiento) y escaneo de puertos (enumeración)
- Debemos recordar que los puertos existen y proporcionan información valiosa, 
- Este tipo de descubrimiento se utilizan puertos conocidos para determinar si una maquina esta apagada o encendida.
	- hping3
		- Escaneo de puertos conocidos usando el flag SYN de TCP
			- hping3 --udp 192.168.56.4 -p 53
		- Escaneo de puertos conocidos por UDP
			- hping3 -S www.scanme.org -p 80
				 *Si nos devuelven un flag SA, entonces el puesto está abierto (SYN/ACK)*
				 *Si nos devuelve un flag RA, entonces el puesto cerrado o filtrado (RST/ACK)*
		- Averiguar el tiempo de operacion de la maquina (tiempo despierta)
			- hping3 -p 443 -S --tcp-timestamp www.scanme.org
				 *Con el flag --tcp-timestamp le estamos preguntado el “uptime”
	- Nmap
		- Podemos escanear puertos conocidos usando el flag SYN de TCP
			- nmap 192.168.56.5 -PA80 -sn
		- Escaneo de puertos conocidos por UDP
			- nmap www.scanme.org -PU53 -sn
			
			
### **Puertos Comunes** ![[Pasted image 20250519231957.png]]
### Registros Web
- Whois
	- Prohibido por la GDPR 
		Alternativa www.nic.es
	- Permite acceder a información sobre el objetivo
		- Detalles de registro
		- Dirección IP
		- Información de contacto que contiene la dirección
		- ID de correo electrónico
		- Numero de Teléfono
		- Propietario del dominio
		- Registrador de dominios
### Correos Electrónicos
- Theharvester
	Es una herramienta de recopilación de cuentas de correo electrónico, nombres de usuario, nombres de host / subdominio
## Enumeración


## Explotación
### Searchsploit 
Busqueda en EDB, funciona offline, permite desarrollar y ejecutar exploits 
### Metasploit
ofrece la shell meterpreter que permite interactuar con la maquina vulnerada en busca de elevar privilegios
- getsystem, funciona en Win y Linux
	- Concepto de Named Pipe en Windows, facilita comunicación entre procesos
### Linux
#### Linux Automático

- **LinPEAS** – Escanea automáticamente el sistema Linux en busca de vectores de escalada de privilegios conocidos.
- **LinEnum** – Recopila información detallada del sistema para identificar posibles rutas de escalada de privilegios.
- **linuxprivchecker.py** – Script en Python que busca configuraciones y permisos inseguros para sugerir posibles escaladas.
- **unix-privesc-check** – Verifica configuraciones del sistema Unix para detectar posibles vías de escalada de privilegios.
- **SUDO_KILLER** – Analiza configuraciones de sudo para detectar abusos potenciales y vectores de escalada.
#### Linux Manual
- **SUID** – Archivos con el bit SUID permiten ejecutar programas con privilegios del propietario (a menudo root).
- **Capabilities** – Permisos asignados a binarios que pueden permitir acciones privilegiadas sin ser SUID. ***IMPORTANTES CAP_SETUID CAP_SETGID
- **SUDO** – Verificación de comandos permitidos mediante sudo para encontrar rutas de escalada.
- **NOPASSWD** – Entradas sudo configuradas sin contraseña que pueden ser abusadas para obtener privilegios.
- **LD_PRELOAD & NOPASSWD** – Inyección de librerías con LD_PRELOAD combinada con sudo para ejecutar código como root.
- **Sudo_inject** – Técnica o herramienta que explota vulnerabilidades o configuraciones de sudo para inyección directa de comandos.
- **Wildcards** – Uso de caracteres comodín en comandos permitidos por sudo para ejecutar scripts maliciosos.
- **Kernels antiguos** – Explotación de vulnerabilidades conocidas en versiones antiguas del kernel Linux.
#### Busqueda de passwords en Linux
- Ficheros que contienen password
	- grep --color=auto -rnw '/' -ie "PASSWORD" --color=always 2> /dev/null
	- find . -type f -exec grep -i -I "PASSWORD" {} /dev/null \;
- Passwords antiguos en /etc/security/opasswd
- ficheros modificados en los ultimos x minutos
	- find / -mmin -10 2>/dev/null | grep -Ev "^/proc"
- Passwords en memoria
	- strings /dev/mem -n10 | grep -i PASS
### Windows
- - **Watson** – Enumera vulnerabilidades locales conocidas en Windows según la versión del sistema operativo.
- **Windows-Exploit-Suggester** – Sugiere exploits disponibles según parches faltantes en el sistema Windows.
- **JAWS (Just Another Windows (Enum) Script)** – Script en PowerShell para enumerar configuraciones inseguras en Windows.
- **WinPEAS** – Herramienta automatizada para escanear vectores de escalada de privilegios en Windows.
- **Seatbelt** – Herramienta de post-explotación para recolectar información sensible y de configuración en Windows.
- **SharpUP** – Busca formas de escalada de privilegios en entornos Windows desde un binario .NET.
- **PowerUP** – Módulo de PowerShell que identifica oportunidades de escalada de privilegios en Windows.
- **PowerLess** – Herramienta para evasión de AMSI y ejecución sin PowerShell directo, enfocada en sistemas restringidos.
- **Sherlock** – Escanea el sistema Windows en busca de vulnerabilidades de escalada de privilegios locales conocidas.

#### Buscando passwords en Windows
- **Mimikatz** – Herramienta poderosa que extrae contraseñas, hashes y tickets Kerberos directamente desde la memoria.
- **SessionGopher** – Script en PowerShell que extrae información de sesiones RDP, VNC y credenciales guardadas en Windows.
