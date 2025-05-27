# Introducción a Análisis Forense

## Definición
Análisis forense informático, consiste en identificar, preservar, analizar y presentar las evidencias de una forma legal y aceptables aplicando técnicas científicas y analíticas especializadas a infraestructura tecnológicas.
## Principio de Locard
Siempre que dos objetos entran en contacto transfieren parte del material que incorporan al otro objeto
## Ámbitos de Actuación
- Recopilación y preservación de pruebas digitales
- Análisis de pruebas digitales
- Recuperación de datos
- Investigación de incidentes de seguridad
- Análisis de redes y Comunicaciones
- Creación de informes y testimonio en tribunales
- Asesoría y capacitación
- Investigación y desarrollo
## Normas AENOR aplicables al análisis forense
AENOR (Asociación Española de Normalización y Certificación)
- Familia UNE 71505:2013
	- -1 Vocabulario
	- -2 Buenas Practicas
	- -3 Formatos y Mecanismos
- UNE 71506:2013
	- Metodología para el análisis forense de evidencias electrónicas
- UNE 197010:2015
	- Criterios generales para elaboración de informes y dictámenes sobre las TIC
- ISO/IEC 27037:2012
	- Guía para adquisición, recolección, identificación y preservación de evidencia
- ISO/IEC 27042:2015
	- Guía para análisis e interpretación de la evidencia
- RFC 3227
	- Recolección y manejo de evidencias
- RFC 4810
	- Preservación de la información a largo plazo
- RFC 4998 (ERS)
	- Método para asegurar la integridad y autenticidad de los datos a lo largo del tiempo
- RFC 6283 (XMLERS)
	- Adaptación de la ERS pero usando XML
## Proceso de Investigación Forense
- Preparación del Caso
- Identificación
- Adquisición
- Preservación
- Análisis
- Presentación
### Preparación del caso
- Debe realizarse una preparación previa para poder adquirir las evidencias correctamente y que todo el proceso sea correcto a nivel legal
	- Permisos
	- Autorizaciones por escrito
	- Contrato
	- Etc
- Asegurar la escena
	- Proteger la escena para evitar la modificación o destrucción de la evidencia
### Identificación
- Detectar y localizar posibles fuentes de evidencia
- Determinar la fuente de los datos, ubicación y relación con el incidente
- Evaluación preliminar de los dispositivos y medios de almacenamiento
- Revisar el entorno legal que protege el bien:
	- Analizar normativas y regulaciones aplicables a la evidencia, asegurando que se realice de manera legal y admisibles en un proceso judicial la adquisición y análisis de datos.
- Inicio de la Cadena de Custodia:
	- Procedimiento que garantiza la autenticidad de la prueba digital desde la obtención hasta que se aporta como hecho probatorio a un procedimiento judicial.
		- Donde, cuando y quien descubrió y recolecto la evidencia.
		- Donde, cuando y quien manejo la evidencia
		- Quien ha custodiado la evidencia, durante cuanto tiempo y como se almaceno.
		- Cambio de custodia, debe ser indicado, como y cuando se realizo incluyendo detalles relevantes del proceso/caso.
### Adquisición
- Consiste en recopilar pruebas digitales de dispositivos electrónicos
- Puede incluir copias forenses bit a bit, extracciones lógica de datos o incluso capturas en vivo de memoria volátil.
- Debe documentarse completamente para garantizar la cadena de custodia.
La informacion debe recopilarse en el orden de tiempo que permanece accesible.
Debe recolectarse primero aquella que es mas volatil:
- Registros y Caché
- Tabla de enrutamiento, caché ARP, tablas de procesos etc....
- Sistemas de archivos temporales
- Disco
- Datos de Registro y monitoreo remoto relevantes
- Configuracion fisica y topologia de red
- Medios de almacenamiento de respaldo
#### Modos de Adquisicion
- Live, obtencion de datos volatiles, debe realizarse con sumo cuidado ya que puede invalidar pruebas si se usan ciertos comandos.
- Dead, se apagan los equipos cortando suministro electrico, y realizar copias bit a bit.

#### Clonado
Es una copia exacta bit a bit de un disco, incluyendo errores o sectores defectuosos, permite realizar una copia sobre la cual ejecutar el análisis, esta copia se aconseja realizarla  ante fedatorio publico, la copia original se la quedan ellos.

Hay clonado por software y por hardware.

### Integridad
Asegurar que los datos son copia exacta de los originales, usar funciones hash sobre original y copia.

MD5 y SHA-1 no son seguros, son susceptibles a ataques de colision.

Usar SHA-2 o SHA-3.
### Preservacion
Es el adecuado tratamiento y documentacion de las evidencias, garantizando la cadena de custodia.
### Analisis
Examinacion de los datos recopilados, para identificar patrones, rastrear actividades delictivas y descubrir informacion relevante para el caso.
- Recuperacion de ficheros eliminados
- Recuperacion e identificacion de correos 
- Busqueda de acciones especificas del usuario de la maquina
- Busqueda de archivos y contenido especifico
- Recuperacion de ultimos ficheros visitados, sitios web, etc.

#### Herramientas
- Autopsy, Brian Carrier, Open Source, colaborativo.
- Volatility, Open Source, escrita en Python
- SIFT (SANS), Compañia privada 1989 Allan Paller.
- Distribuciones
	- CAINE, bloqueo automático de escriturad para dispositivos conectados.
	- Paladin,
	- Parrot Security OS, basada en Debian con enfoque en seguridad informática
	- Cellebrite, Israelí, dispositivos móviles
	- MOBILedit
	- EnCase
### Presentación de Resultados
Recopilar y documentar toda la información que se obtuvo en el análisis.

Si es necesario se emite un informe forense, que debe comunicar de manera efectiva y clara información técnica y compleja para personas no técnicas, jueces y jurados.

# Figura del Perito
Decretado el 17 de Agosto de 1901 en el decreto de Romanones.

Se exige titulación oficial según la LEC en art. 340.1.

#### Peritos
- Perito Informático, experto en tecnologías de la información y sistemas informáticos
- Perito Forense, experto en ciencias forenses.
- Perito Informático Forense, experto en informática forense especializado en la identificación, preservación, análisis y presentación de evidencia digital en investigaciones y casos legales.
- Perito Judicial, profesional dotado de conocimientos especializados y reconocidos, que suministra información u opinión fundada a los tribunales de justicia sobre los puntos litigiosos que son materia de su dictamen.
#### Peritos Judiciales según designación
- Perito de oficio, elegido por un juez o tribunal
- Perito de Parte, elegido por una de las partes, y aceptado por el juez o fiscal.
## Código Deontológico
Conjunto de obligaciones morales del profesional y hace referencia a la ética.

***Obrar según ciencia y conciencia.***

El perito esta obligado a guardar el secreto profesional, ha de ser consecuente con la información encontrada en sus actuaciones, si hay un delito se debe informar a las autoridades competentes.
### Ordenes Judiciales
El perito puede intervenir en 3 de las cinco ordenes jurisdiccionales
- Civil
- Penal
- Contencioso administrativo
- Social
- ~~Militar~~
### Responsabilidades 
- Civil, obligado a reparar el daño a un particular
- Penal, obligado a reparar el daño a la sociedad
- Disciplinaria, no comparecer en juicio o vista cuando sea requerido judicialmente para ello
- Profesional, no cumplir el código penal deontológico o el procedimiento disciplinario Colegial.
### Cuerpo Oficial de Peritos (COP)
Conjunto de peritos colegiados para una profesión dada, es tarea de los colegios profesionales la creación y gestión del COP

## Normativa en España
#### LOPDGDD
Ley de protección de datos personales y garantía de los derechos digitales.

Garantiza los derechos digitales de los ciudadanos, establece requisitos estrictos en relación con la recopilación, almacenamiento, uso y divulgación de datos personales.
#### Código Penal
Contiene disposiciones especificas relacionadas con delitos informáticos, básicamente define que se considera delito informático.
#### LEC (Ley de Enjuiciamiento Civil)
Regula los procedimientos y procesos en casos civiles en España
#### LECr (Ley de Enjuiciamiento Criminal)
Establece reglas y procedimientos para la investigación y enjuiciamiento de delitos en España.
#### LSSI (Ley de Servicios de la Sociedad de la Información y de Comercio Electrónico)
Regula aspectos del comercio electrónico y servicios en linea
Investigadores forenses pueden verse afectados al investigar casos que involucren la transmisión y almacenamiento de datos en linea.
#### LOPSC (Ley Orgánica de Protección de la Seguridad Ciudadana)
Vigilancia e intercepción de comunicaciones en contexto de la seguridad nacional y lucha contra el terrorismo
#### LCD (Ley de la Conservación de Datos)
Establece las obligaciones de los proveedores de servicios de comunicaciones electrónicas y las redes publicas de comunicacion en relación con la conservación de datos durante 12 meses para fines de investigación y enjuiciamiento de delitos graves.
# Análisis Forense en Windows
Implica la identificación y extracción de datos relevantes de diversas fuentes para poder reconstruir las actividades realizada en el sistema y determinar posibles evidencias.
## Artefactos
Se refiere a cualquier objeto, dato o elemento almacenado en un sistema informático que pueda proporcionar información valiosa para una investigación
- Ficheros
- Cadenas de Registro
- Rutas de Acceso
- Configuraciones
- Metadatos
- Elementos que puedan ayudar a reconstruir o proporcionar evidencia.
Se dividen generalmente en, artefactos de aplicación y artefactos del OS.
## Logs
Proporcionan información sobre eventos específicos, aplicaciones y servicios.

En Windows encontramos:
- Event Logs (Registro de Eventos)
- Registro de Aplicaciones
- Registros varios sobre la instalación.
## Papelera de Reciclaje
Disponible por primera vez en Windows 95.

Contiene archivos borrados, información de la fecha y hora en la que se eliminaron y la ubicación donde estaban originalmente.
## Windows Registry
Proporciona información sobre:
- Frecuencia y tiempo de uso de las aplicaciones, información codificada, y deben usarse herramientas especializadas para decodificar.
- Dispositivos USB conectados, identificador de dispositivo, numero de serie, timestamps, etc.
- Asociaciones de tipos de archivos y programas predeterminados, identificador o clase de archivo que nos interesa.
### HKEYS (Handle To Registry Key)
- HKEY_CURRENT_USER, almacena configuraciones y preferencias especificas del usuario que ha iniciado sesión actualmente.
- HKEY_CURRENT_CONFIG, Contiene información sobre el perfil de hardware activo.
### Hives
El registro se agrupa en secciones lógicas conocidas como hives, so un grupo de claves, subclaves y valores relacionados con una parte especifica del OS o con las configuraciones de usuario. Ademas cada Hive se respalda en **Hive files** que contienen copias de seguridad de sus datos.

#### Hives importantes
- HKEY_LOCAL_MACHINE\SAM
- HKEY_LOCAL_MACHINE\Security
- HKEY_LOCAL_MACHINE\Software
- HKEY_LOCAL_MACHINE\System
- HKEY_CURRENT_CONFIG
- HKEY_USERS\DEFAULT
## Listas MRU (Most Recently Used)
Listas que almacenan información sobre los elementos utilizados mas recientes en un OS.

Podemos encontrar estas listas en el registro de Windows.

- OpensavePidlMRU, proporciona información sobre los archivos abiertos o guardados mas recientemente
- RunMRU, indica los comandos ejecutados en el cuadro de dialogo Ejecutar (Win+R)
## Shellbags
Lugares donde el OS almacena información relacionada con las preferencias de visualización de contenidos de Windows Explorer.

Pueden proporcionar información sobre las capetas a las que el usuarios ha accedido aun cuando estas ya no existan, incluyen timestamps.

### Bags
Contiene la información de las shellbags
### BagMRU
Contiene información sobre el historial de carpetas visitadas por un usuario en el Windows Explorer.
## Herramientas
- MiTec WRR, permite leer archivos de registro de Windows.
- ShellBags Explorer (SBE)
- RegRipper

## Prefetch
Mejora el rendimiento y la eficiencia de la carga de aplicaciones.

Para el analista permite descubrir trazas de uso y eliminacion de aplicaciones, permite tambien reconstruir la linea temporal.
## Superfetch
Monitorizacion de forma continua el uso de los programas, y optimizacion de la asignacion de memoria, precargando en RAM aquellos elementos que se utilizan con mayor frecuencia segun el patron de uso del usuario, este trabaja continuamente en tiempo real.

## Organizacion de almacenamiento de datos
### Jerarquia de almacenamiento
- Bit
	- Byte
		- Sector
			- Cluster
### Tamaño y Asignacion
- El tamaño de los sectores y clusters se define en el encabezado del sistema de archivos
- Los sistemas de archivos asignan espacio en disco a los archivos en clusters completos
### Organizacion del sistema de archivos
- FAT
- NTFS
### Organizacion del almacenamiento de datos
- Particiones y Volumenes
	- Particion
		- Define areas especificas del disco per no incluye sistema de archivos
		- Una particion es una division logica del disco
	- Volumen
		- Es un area de almacenamiento formateada con un sistema de archivos lista para guardar datos.
		-
## Sistemas de Archivos FAT
### Componentes Clave
### Sector de Arranque
- Ubicado al inicio del volumen
- Contiene información esencial sobre el sistema de archivos (tipo, tamaño, diseño).
- Incluye BPB, proporciona los detalles necesarios para acceder correctamente al volumen
### Tabla de Asignación de Archivos (FAT)
Actúa como mapa del dispositivo de almacenamiento
- Libre (Unallocated)
- Asignados (Allocated)
- Fin de un archivo (EOF)
- Defectuoso
### Comportamiento de eliminación de archivos
- Al eliminar un archivo en FAT, el primer caracter de su entrada en el directorio se reemplaza por (0xE5), marcándolo como eliminado.
- Los cluster de datos reales no se modifican hasta que son sobrescritos por nuevos datos.
### Restos de Fragmentación
- Datos de un archivo que se dispersan en cluster no contiguos.
- Al eliminar un archivo, los punteros que enlazan sus clusters se cambian a cero, complicando la recuperación y análisis de los datos.
### Espacio Residual
Archivos pequeños o el ultimo cluster de un archivo pueden no ocupar completamente el espacio asignado, dejando sectores residuales conocidos como **Slack Space**.
### Artefactos de Timestamps
- FAT registra las fechas de creación, modificación y acceso con precisión limitada, lo que puede dificultar el análisis cronológico preciso.
- Los timestamps, se almacenan en hora local y no incluyen información de zona horaria.
## Sistema de Archivos NTFS
Optimizado para discos duros, soporta volúmenes y archivos de mayor tamaño que FAT.
### Sector de Arranque
- Ubicado al inicio de un volumen NTFS y almacenado en el registro $Boot.
- Esencial para iniciar al OS y detalles sobre el sistema de archivos
### Area de Datos
- Región del volumen donde se almacenan los archivos de usuario y los directorios.
- Se gestiona en clústeres, y sus estado de asignación se controla mediante el archivo $Bitmap.
### Componentes Clave
- MFT (Master File Table)
	- Actúa como la base de datos central de NTFS
	- El archivo $MFTMirr contiene un respaldo de los primeros cuatro registros de la MFT, necesaria en caso de daño de la MFT
- Tamaño de Sector
	- Estándar es de 512 bytes
- Tamaño de Cluster
	- Varia según el tamaño del volumen
	- Oscila entre 512 bytes y 64 KB
La zona MFT evita la fragmentación, es un área especifica que crece para evitarla.
### Forense NTFS
- Al eliminar un archivo la entrada MFT se marca como no usada, pero permanece intacta
- Slack Space, pueden quedar archivos residuales si el archivo nuevo no llena el cluster en su totalidad.
- Análisis del Volumen Shadow Copy (VSC), crea copias instantáneas de archivos o volúmenes incluso en uso, permite recuperar varias versiones anteriores de archivos, incluyendo datos eliminados o modificados.
- 