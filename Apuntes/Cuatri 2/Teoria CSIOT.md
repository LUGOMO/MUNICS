# Introducción a la Ciberseguridad Industrial
## Conceptos Básicos
### Ciberseguridad Industrial
Rama de la ciberseguridad que aglomera un conjunto de acciones para proteger de ataques a usuarios y entidades pertenecientes a un entorno industrial.
### Infraestructura Critica
Infraestructura indispensable para el correcto funcionamiento de la industria, su destrucción o perturbación conlleva un grave impacto en los servicios esenciales.
### Servicio Esencial
Es aquel necesario para garantizar el mantenimiento de las funciones sociales básicas, de salud, seguridad bienestar social y económicas de los ciudadanos y el eficaz y correcto funcionamiento de las instituciones de un  estado o administraciones publicas.
### Infraestructura estratégica
Son las instalaciones, redes, sistemas , equipos físicos y tecnologías de la información y comunicacion sobre las cuales funcionan los servicios esenciales.
### Políticas de Seguridad Industrial
Son el conjunto de actividades destinadas a asegurar la funcionalidad, continuidad e integridad de las infraestructuras, con el fin de minimizar, preveer y mitigar el daño causado por un ataque deliberado contra dichas infraestructuras.

Tambien tienen que garantizar la integracion de las acciones llevadas a cabo por otras personas/entidades responsables de los problemas de seguridad que se abordaran.
## Ley PIC (Proteccion de Infraestructuras Criticas)
Define el conjunto de infraestructuras que prestan servicios esenciales en España.

Diseña un planteamiento que contiene medidas de prevención y protección eficaces contra las posibles amenazas de dichas infraestructuras, tanto en el plano físico como la seguridad de las TIC.

### Contribuciones Ley PIC
- Sistema Nacional de Protección de Infraestructuras Criticas.
- Marco Normativo del Sistema de Planificación PIC.
- Catalogo Nacional de Infraestructuras Criticas.
- CERT (Computer Emergency Response Team).
### Catalogo PIC
Recopilación completa, actualizada y contrastada sobre la totalidad de las infraestructuras estratégicas del territorio nacional.
3500 instalaciones de todas las areas y contiene:
- Descripción.
- Contacto.
- Tipo.
- Datos Geográficos.
- Localización.
- Información de Seguridad.
- Riesgos Evaluados.
- Etc.

### Infraestructuras Criticas
- España
	- Estrecho de Gibraltar.
	- Instituto Grifols (Fabrica de inmunoglobulina intravenosa).
	- Gaseoducto entre Algeria y Europa.
- Galicia
	- Puerto.
	- Refinería y Oleoducto de A Coruña.
	- Regasificadora de Mugardos (Muy importante).
- Otros países:
	- Farmacéuticas.
	- Minas.
	- Infraestructuras TIC.
	- Puertos.
	- Ubicaciones Estratégicas.
## Implicaciones de Ciberataques en Entornos Industriales
### Principales impactos
- Cambio en un sistema, OS o una configuración de una aplicación
	- Introducción de canales de control
	- Supresion de sistemas de alarma para ocultar actividad maliciosa
	- Alteración del comportamiento esperado para producir resultados inesperados/impredecibles
- Cambio de la lógica de controladores industriales
	- Daños en equipos o instalaciones
	- Mal funcionamiento de procesos
	- Deshabilitación del control sobre un proceso
- Envió de información errónea a operarios
	- Provocar acciones que indiquen respuestas erróneas, conllevando a reprogramación lógica de un controlador
	- Ocultar actividades maliciosas, incluido el incidente en si o inyección de código
- Alteración de los sistemas de seguridad tradicional u otros controles
	- Interrumpe las operaciones esperadas, backups u otras medidas típicas de seguridad, pudiendo ocasionar daños
- Infección de software malicioso
	- Suele impactar las operaciones comunes del dispositivo, ocasionando una detención de su funcionamiento para analizar, reemplazar o limpiar.
	- Facilita el acceso a otros dispositivos industriales para el ataque
- Robo de Información
	- Extracción de secretos industriales
- Alteracion de informacion
	- Moficiacion de cierta informacion para perjudicar la produccion de un producto

## Ataques a Infraestructura Industrial
- Año 2000 
	- Utilizan un radio transmisor para abrir una estación de aguas residuales en Australia, se virtió el contenido en ríos adyacentes.
- Año 2007
	- Proyecto Aurora demuestra que podían controlar y estropear un generador diesel usado para producción de energía
- Año 2008
	- Un gusano "agent.bz" inicia el proceso de infección de maquinaria militar de EEUU.
		- Usaron un Pendrive dejado en un Parking
		- Mayor ataque en la historia de EEUU cibernético
		- El malware abría una backdoor
		- El pentagono prohibio uso de USB y deshabilitó el autorun en Windows
		- 2005 Sony Rootkit usa autorun para instalar desde CDs software antipirateria.
	- Año 2009
		- Operacion Aurora contra Google y otras empresas
			- Introducía Payload para extraer ideas de negocio, diseños industriales y propiedad intelectual secreta
	- Año 2010 
		- Stuxnet, 4 exploits Zero day (Iran Nuclear Plant)
			- Buscaba servicios de PLCs Siemens
			- Credenciales por defecto en cuentas SQL del PLC
			- Inyectaba Rootkit a través de Profibus
			- Controlaban así la velocidad de un motor
			- Destruyo 1/5 de las centrifugadoras, fallaba el motor y no dejaba de dar vueltas sin control
	- Año 2011
		- McAfee descubre Night Dragon
			- Oculto desde 2009
			- Atacaba empresas petroleras, energéticas y petroquímicas
			- Extraía información sensible
			- Accede a servidores coorp a través de SQL injection para entrar a la intranet
	- Año 2012
		- Shamoon
			- Objetivo Aramco y RasGas (Petroleras Saudi y Qatar)
			- Malware para Win NT, infiltrado por phishing
			- 15 agosto en Ramadan exploto una bomba lógica sobrescribiendo 30000 disco duros de computadoras de Aramco
	- Año 2019
		- Ataque contra red eléctrica inteligente de EEUU
	- Año 2021
		- Ataque a Oleoducto en EEUU
	- Año 2024
		- Ataque Salt Typhoon
		- Operando desde 2022
		- Accede a ordenadores de empresas de Telecom
		- Lee datos de llamadas, audios de llamadas SMS e ip de destino

# Introducción a Sistemas Ciberfísicos e IoT
Los sistemas ciberfísicos son sistemas controlados y monitorizados mediante algoritmos computacionales, generalmente abarca subsistemas los cuales interconecta usuarios a través de Internet.

IIoT, es la IoT en contexto industrial, conecta hardware industrial buscando mejorar la eficiencia y la automatización.

Los CoBots, son robots colaborativos.
## Hardware y Firmware
### Sensórica
Son sistemas de adquisición de datos mediante interfaces, sensores y multiplexores
#### Tipos de Sensores:
- Naturales, responden a señales electro-químicas basándose en el transporte de iones. (Ojo humano)
- Artificiales, se basan en el transporte de señales eléctricas o fotonicas. (Creados por el ser humano)
#### Conceptos Básicos
- Estimulo, propiedad física que es detectada y convertida en señal eléctrica o fotónica.
- Formato de salida de un sensor, puede ser un voltaje, corriente o carga, también puede indicar amplitud frecuencia, fase o código digital de salida.
- Sensor Vs transductor, el transductor convierte un tipo de energía en cualquier salida, el sensor SIEMPRE convierte a energía eléctrica.
- Actuador, cualquier elemento que actúe en respuesta a una señal captada por sensores
### Sensores y Actuadores comunes
- Sensores de Movimiento, detectan y miden aceleración y rotación en los tres ejes.
	- Acelerometro MEMS, sensor basado en sistemas microelectromecanico, detecta cambios en la velocidad usando micro-sensores y un microprocesador (usado en vehiculos).
	- Giroscopio, se usa cuando no hay campo geomagnetico y permite detectar la orientacion actual o sus cambios a partir de la velocidad angular.
	- Magnetometro, sensor sensible al campo electromagnetico de la tierra, tambien denominado compas, mide en Teslas \[T]
- Sensores de Posición, permiten obtener la ubicación física del dispositivo.
	- Sensores de Proximidad, miden el calor emitido por humanos y ciertos animales, detectan presencia, y permiten activar de forma automatica sistemas o alertas.
- Sensores Ambientales, miden parámetros como temperatura, presión, iluminación y humedad.
- Sensores Fisiológicos, miden parametros corporales, presion sanguinea, pulsaciones, ECG, EMG, glucosa, oxigeno en sangre, etc.

### Cloud
Los datos industriales son enviados a servidores con servicios de automatización industrial en la nube.

### Seguridad de CPS y Sistemas IoT/IIoT
La problemática principal es que los equipos IoT tradicionales tienen poco poder computacional, ademas de soler depender de baterías y pilas, ademas suelen ser muy inseguros (reciben pocas actualizaciones y falta de cifrado) es un blanco fácil para ataques cibernéticos. 

### Soluciones Típicas
- Firewall
- VPNs
- Optimizacion de Software
- Uso de Cripto-Chips
- Uso de nuevas Arquitecturas IoT-IIoT
# Ciberseguridad de Sistemas de Control y Comunicacion Industrial
## ICS (Industrial Control System)
Es un sistema formado por equipos interconectados que controlan, monitorizan y administran grandes sistemas de produccion industria, suelen controlar infraestructura critica, como plantas de produccion electrica, sistemas de transporte, plantas quimicas, etc.

### Sinónimos incorrectos y Áreas a ICS:
- PCS (Sistema de Control de Procesos) o PLC (Controlador Lógico Programable)
	Es una unidad de procesamiento.
- DCS (Sistema de Control Distribuido)
	Es una locacion.
- SCADA (Supervisory Control and Data Acquisition)
	Área extensa geográfica.
En general ICS engloba a PCS, DCS y SCADA y la estructura respeta ese orden.
## PLC
Permite a los operarios tomar decisiones de control sobre elementos hardware, creados en 1968 por GM (General Motors) para reemplazar los circuitos lógicos basados en relés.

Un PLC, es fácil de programar, mantener y reparar o sustituir, son pequeños, mas baratos que los relé y capaces de comunicarse con dispositivos

Evolucionaron para que tengan mayor potencia de procesamiento, soporte para I/O digital y analógico, como distintas variantes de soporte para nuevos protocolos de comunicacion como también implementar variantes de lazos de control

### Estructura de PLC:
- Input Module
- Procesor Unit
	- CPU
	- ALU
	- Memory
- Power Supply
- Output Module
## SCADA
Es una capa de Software por encima de los PLC que se encarga de realizar tareas de supervisión/monitorización sobre estos.

No lleva a cabo tareas de control sobre los PLC, solo supervisión, sin embargo muchos sistemas SCADA también permiten enviar comandos de alto nivel para realizar acciones de control.

Permiten, adquirir datos, presentarlos a través de interfaces personalizadas(HMI Human-Machine-Interface), y realizar control de sistemas distribuidos de manera dispersa geográficamente.
#### RTU (Remote Terminal Unit)
Hardware de control que se comunica con un sistema SCADA a través de un nodo maestro (MTU) Master Terminal Unit, estos RTU suelen ser un tipo de PLC, suelen mostrar solo cambios de estado y no un flujo continuo.
## DCS
Son similares a un SCADA recoge datos de hardware y los presenta en HMI pero este muestra los datos en tiempo real, se debe a que se sitúa en locaciones con alta conectividad.

Suele decirse que los SCADA son event driven, mientras que los DCS process driven.
## Protocolos de Comunicación
Amplia diversidad de protocolos muy específicos, son protocolos optimizados para ser fiables, donde la mayoría permiten operaciones en tiempo real de manera muy precisa.

Estos son diseñados para ser eficientes a la hora de cumplir con requisitos económicos y de operación de sistemas de control altamente distribuidos.

No suelen ofrecer autenticacion y cifrado, suelen llamarse de manera general Protocolos SCADA o Protocolos Fieldbus.
- Protocolos SCADA, para comunicacion de sistemas de supervision.
- Protocolos Fieldbus, para comunicacion de sistemas de control.

### ModBus (Modicon Communication Bus)
Es el protocolo mas antiguo y utilizado (1979) es el estándar en la industria, es protocolo abierto y gratuito, transmite los datos en plano, trabaja a nivel de aplicación y sigue un modelo request/reply, en general es muy sencillo y con muchas variantes.

#### Problemas de Seguridad
- Carece de Autenticación
	- Solo requiere de una dirección y un código de función valido, que pueden ser fácilmente adivinados o copiados
- Ausencia de Cifrado
	- Todos los datos se transmiten en claro, pueden ser capturados y alterados con facilidad.
- No hay verificación de la Integridad
	- No hay checksums de mensajes por lo que se facilita su alteración.
- Uso de Puerto serial
	- No posee mecanismos de supresión de broadcast, por lo que todos los dispositivos conectados reciben todos los mensajes, por lo que facilita ataques DoS.
- Peligro de reprogramacion
	- Permite inyectar lógica de control maliciosa.
Se recomienda su uso solamente en entornos controlados, hacer uso de IDSs o IPSs y SCADA para monitorizar los comandos ejecutados, en áreas mas criticas se sugiere Firewalls, filtros específicos de protocolos industriales, y sistemas de monitorización a nivel de aplicación para validar sesiones y prevenir Hijacking de sesiones ModBus.

### OPC (Object Linking and Embedding for Process Control)
Es un framework para comunicar sistemas basados en Windows que usan el protocolo OLE de Microsoft.

Es un conjunto de protocolos que permite comunicar a sistemas que controlan procesos usando funcionalidades de red de Windows usualmente TCP/IP

Al utilizar la API DCOM (Distribuited Componen Object Model) de Microsoft elimina la necesidad de usar drivers especificos para cada dispositivo.

Fundamentalmente es como SCADA, y actualmente se implementa la arquitectura OPC-UA (Unified Architecture).

#### Problemas de Seguridad
- Al usar DCOM y RPC es sumamente vulnerable a ataques
- Al depender de Windows es vulnerable a exploits del OS o típicas vulnerabilidades de Host Windows
- Son muy difíciles de parchear.

### Diferencias con Redes de Comunicación Comerciales
Los sistemas ICS están diseñados para controlar equipos físicos en entornos industriales exigentes, con alta fiabilidad, bajo tiempo de respuesta y protocolos especializados. En cambio, las redes comerciales se centran en la transferencia de datos en entornos comunes, con menor exigencia de fiabilidad, mayor tolerancia a fallos y protocolos unificados.
#### Seguridad
El impacto de los fallos de seguridad de los ICS son usualmente mayores que en otros sistemas, debido a que conllevan consecuencias físicas, los errores suelen ser difíciles de diagnosticar y reparar porque se manifiestan como fallos de mantenimiento o parones.

Es complicado administrar ICSs debido al desfase de software, no hay entornos amigables de pruebas y los dispositivos pueden estar muy dispersos físicamente y normalmente no se pueden usar Firewall o antivirus porque entorpecen el funcionamiento regular.

Los vectores de ataque suelen ser  específicos debido al uso de protocolos de red no típicos o comandos no "bloqueables" por cuestiones de seguridad.
# Ciberseguridad de Tecnologías de la industria 4.0/5.0
## Tecnologías de la industria 4.0
Industria 4.0 representa la evolución de las fabricas tradicionales a fabricas inteligentes, buscan mas eficiencia en administración de recursos y tener alta flexibilidad para adaptarse al constante cambio en los requerimientos de producción, este concepto se definió oficialmente en 2011 por el gobierno Alemán.

### Pilares principales
- Robots Autónomos, automatizar con robots tareas sistemáticas de industrias (Cobots)
- Big Data, 
- Realidad Aumentada
- Manufactura Aditiva
- Computación en la Nube
- Ciberseguridad
- IoT
- Integración de Sistemas
- Simulación
## Tecnologías de la industria 5.0
Busca personalizar productos a escala masiva, se basa en la cooperación entre humano y maquina, utiliza computación cognitiva esto intenta a través de IA y procesamiento de señales imitar como los humanos tomamos decisiones.

# Ciberseguridad dispositivos IoT/IIoT Hardware, Firmware y Middleware

## IoTSF
Proporciona una guía de buenas practicas.

#### Clasificacion de dispositivos IoT
- Sensores
- Actuadores
- Gateways
### Clasificación  de los Datos
Un esquema de clasificación de datos define un numero de clases o niveles de sensibilidad para los datos y es esencial para su protección
### Seguridad Física
Define las medidas a tomar para asegurar que los dispositivos no sean vulnerados y cumplan con todas las medidas necesarias de seguridad, donde en casos específicos donde se necesiten funcionalidades físicas como puertos , la circuitería etc, estén debidamente protegidos y aislados de individuos malintencionados.
### Arranque seguro
La integridad de un dispositivo depende críticamente que su arranque lógico cumpla con el arranque de confianza.
### OS seguro
Debemos de minimizar el riesgo que amenazas se infiltren en el OS, manteniendo actualizado y protegido el sistema operativo.
### Seguridad de las Aplicaciones
Las aplicaciones propias y de terceros deben seguir los principios de diseño de implementacion segura, debe de documentarse el diseño, deben ser operadas a nivel de privilegio mas bajo, asegurarnos que cumplan con las regulaciones etc.
### Gestión de Credenciales
Las credenciales son la evidencia de las identidades de las personas o de otras entidades, los dispositivos deben ser identificables de manera única, deben usarse buenas practicas de políticas de contraseñas, usar hashes, usar autenticacion de dos factores etc.
### Cifrado
Debemos aplicar el nivel apropiado de cifrado en función a los datos que se transmiten, ademas se aconsejas utilizar suites de cifrado estándar en las industrias y configurar conexiones seguras al igual que implementar protocolos seguros.
### Conexiones de Red
Seguir protocolos de seguridad, como solo utilizar aquellas interfaces necesarias, ejecutar servicios exclusivamente necesarios, uso de protocolos seguros, autenticacion en cada conexión como también autenticar el destino antes de enviar datos sensibles.
### Securización de las Actualizaciones de OS
Las actualizaciones permiten parchar fallos en funciones o vulnerabilidades de los dispositivos, por esta razón se aconseja mantener los equipos con actualizaciones al día, cifrar los paquetes de actualizaciones para evitar ingeniería inversa.
### Registro (Logs)
Se deben mantener actualizados los logs de eventos ya que ayudan a la gestión de fallos de seguridad, se deben rotar los logs y mantener en sitios seguros, adicionalmente se aconseja definir niveles de registro para procesar con mejor facilidad las alertas.
### Política de Actualización de OS
A veces los dispositivos están limitados por recursos, debemos de realizar un proceso de gestión de todos los equipos conectados a lo largo de su ciclo de vida, llevando registro de cada uno de ellos, mantener actualizado, llevar registro de versiones como gestionar aquellos reemplazos cuando es necesario, ademas debemos tener mecanismos de actualización debidamente definidos dentro de la arquitectura del software.
### Evaluar el Proceso de Arranque Seguro
El arranque seguro no puede ser evitado, por esta razón todo software que se cargue en el arranque seguro debe ser verificado, justo después que fue cargado en RAM.
### Imágenes y Firmas de las Actualizaciones de Software
Es critico verificar que todo software instalado en un dispositivo provenga de una fuente de confianza, se debe de usar criptografía para firmar el paquete de software.
### Ataques de Canal Lateral
Un ataque de canal lateral es una característica no intencionada/anticipada, para observar cambios de estado de un sistema, estos ataques no deben ignorarse porque buscan recopilar información de como se comporta el sistema para posterior realizar ataques dirigidos.

## PSA (Platform Security Model)
Es un marco diseñado para mejorar la seguridad de los dispositivos y servicios, más enfocado a circuitos integrados a diferencia de IoTSF.

Contempla que los dispositivos:
- Son identificables de forma única.
- Admiten un ciclo de vida de seguridad.
- Son verificables de forma segura.
- Garantizan que solo se pueda ejecutar el software autorizado.
- Admiten actualizaciones seguras.
- Impiden la instalación de actualizaciones antiguas.
- Admiten el aislamiento.
- Admiten la interacción a través de los límites de aislamiento.
- Admiten la vinculación única de datos confidenciales a un dispositivo.
- Admiten un conjunto mínimo de servicios confiables y operaciones criptográficas necesarias para que el dispositivo admita los demás objetivos

Modelo de Seguridad:
- Especificaciones de Seguridad Y Cumplimiento de Certificaciones
	- Diseño y Manufactura y Deployment
		- Reporte de Manufactura
			- Manejo del Dispositivo
		- Enrolment
			- Verificación de Dispositivos
				- Validación de Entidad
				- Attestation
		- Provisionamiento y actualizaciones
			- Manejo del Dispositivo
		- Protocolo Attestation
			- Verificación de Dispositivos
				- Validación de Entidad
				- Attestation
## Modelado de Amenazas
Consiste en comprender un sistema, identificar las amenazas al sistema, clarificarlas según impacto y probabilidad de ocurrencia

Si no se realiza un modelado de amenazas pueden destinarse fondos a herramientas que no cubrirán las preocupaciones mas serias.
### Proceso de modelado de Amenazas (Microsoft)
- Identificar los assets
- Describir la arquitectura
- Descomponer la aplicación
- Identificar las amenazas
- Documentar las amenazas
- Clasificar las amenazas
### Arboles de ataque
Un ataque habitualmente es sistemático, un ataque suele ser una parte de una campaña de subataques al sistema. Los arboles de ataque sirven para modelar las características de ataques en dispositivos y sistemas

Es un diagrama conceptual de como un objetivo podría ser atacado, permitiendo a los usuarios analizar escenarios de ataque y defensa.
# Bluetooth LE 
