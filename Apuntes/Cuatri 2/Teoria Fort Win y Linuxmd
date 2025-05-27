# Arquitectura de Seguridad de Win11
## Seguridad Basada en Hardware
### TPM 2.0 (Trusted Platform Module)
Este modulo es un chip dedicado, gestiona claves criptograficas y protege datos sensibles, asegura el arranque del sistema, cifra los datos y proporciona  una base para la autenticacion segura
### Secure Boot
Garantiza que el sistema arranque solo con software firmado y verificado digitalmente. Previene la integridad del sistema desde el inicio.

### Virtualizacion de Seguridad
Utiliza tecnologias de virtualizacion de hardware para crear un entorno aislado que protege las operaciones criticas del sistema como administracion de credenciales y proteccion de memoria.

## Seguridad en el Nucleo del sistema


### Proteccion de Codigo Basada en Virtualizacion (HVCI)
Uyiliza la virtualizacion para proteger la memoria del sistema operativo contra ataques malware y explotacion

### Proteccion de la Integridad de la Memoria
Asegura que los procesos criticos del sistema operativo se ejecuten en un entorno seguro y aislado, reduciendo el riesgo que malware afecte memoria y su integridad.

## Seguridad en el Sistema de Archivos

### Bitlocker
Proporciona un cifrado de disco completo para proteger los datos almacenados en el dispositivo

### Proteccion de Archivos EFS
El sistema de archivos cifrados EFS permite cifrar archivos individuales en el sistema de archivos NTFS, proporciona una capa adicional de seguridad sin necesidad de cifrar todo el disco.

## Seguridad en la Red

### Firewall de Windows
Controla el trafico de red entrante y saliente, aplica reglas para permitir o bloquear conexiones segun la configuracion de seguridad del usuario y la organizacion

### Proteccion contra Amenazas de Red
W11 incluye caracteristicas para proteger contra ataques de red como filtrado de contenido, proteccion contra intrusiones y control de aplicacciones.

## Gestion de Identidad y Acceso

### Windows Hello
Proporciona opciones de autenticacion biometrica, reconocimiento facial, huellas PINs para autenticar usuarios de forma mas segura que contraseñas comunes

### Autenticacion Multifactor
Ofrece una capa adicional de seguridad, se solicitan multiples formas de verificacion antes de permitir el acceso.

## Actualizaciones y Parcheo de Seguridad

### Actualizaciones automaticas
W11 esta diseñado para gestionar automaticamente las actualizaciones del sistema operativo, parches de seguridad y mejoras.

### Windows Update fors Business
Permite a las organizaciones gestionar y controlar el despliegue de actualizaciones en entornos corporativos.

## Proteccion de la Privacidad

### Controles de Privacidad Mejorados
W11 ofrece herramientas y configuraciones avanzadas para gestionar el acceso de las aplicaciones a datos personales y funcionalidades del sistema. Permite a los usuarios tener un mayor control sobre que aplicaciones pueden acceder a su información.

### Transparencia en el Manejo de Datos
W11 proporciona informes y herramientas para que los usuarios puedan ver y controlar como se recopilan y utilizan sus datos


## Características de Seguridad Incorporadas en el Diseño de W11
### Hardware:
- TMP 2.0.
- Secure Boot.
### Identidad y acceso:
- Windows Hello.
- MFA.
### Datos y cifrado:
-  BitLocker.
-  Protección de Datos de la Empresa: Protección cifrada de datos corporativos al cifrarlos y asegurando que solo se acceda con autorización.
### Malware y amenazas:
- Microsoft Defender Antivirus: Protección en tiempo real contra malware, spyware y otras amenazas. Incluye capacidades avanzadas de detección y respuesta, aprovechando IA.
- Control de aplicaciones de Windows Defender (WDAC): Control de ejecución de aplicaciones en los equipos de una organización.
### Seguridad en la Red:
-        Firewall.
-    Protección contra vulnerabilidades de red.
### Integridad del  Sistema y Virtualización:
- Virtualización de Seguridad: Utiliza las capacidades de virtualización del hardware para crear un entorno aislado y seguridad
- HVCI.
### Actualizaciones y gestión:
 - Actualizaciones automáticas: Gestiona automáticamente las actualizaciones del sistema operativo, asegurando recibir los últimos parches de seguridad.
- Windows Update for Business: Permite gestionar el despliegue de actualizaciones en los entornos empresariales sin interrupciones significativas.
### Privacidad y control de acceso:
- Controles de privacidad: Opciones avanzadas de gestión de permisos de las aplicaciones y acceso a datos personales.
 - Gestión de acceso a datos: Herramientas para controlar qué aplicaciones pueden acceder a datos sensibles.
### Seguridad y Monitoreo:
- Centro de seguridad de Windows: Panel centralizado para gestionar el estado de la seguridad del sistema.
- Visor de Eventos y Registro de Seguridad: Permite a los administradores monitorear y registrar eventos de seguridad en el sistema, facilitando detección y respuesta.
## Importancia de Mantener el OS Actualizado
Se repite la misma información anterior

# Configuración y Administración de Cuentas de Usuario
## Creación y Gestion de Cuentas de Usuario

# H1 Hardening Boot
## Boot Steps ?

## Securing the Grub Bootloader
### Usuarios y Superusuarios

Se pueden definir usuarios y superusuarios e indicar que acceso tendrán estos a las entradas del menu del grub

*No necesariamente el nombre corresponde con usuarios del sistema*
Cuando definimos los "Menuentry" es cuando establecemos que usuario puede usarlo o no

- Si queremos que un menuentry sea accesible solo por superuser o user1 sera:
	menuentry --users user1 set root=(hd0,2)
- Si queremos que cualquiera pueda usar esta entrada:
	menuentry --unrestricted {set root=(hd0,2)
	
#### **Cualquier entrada que no tenga especificado "--unrestricted o --user" solo puede ser accedida por superusers (root)**

### Grub Passwords

Se utiliza el comando grub-mkpasswd_pbkdf2 para cifrar las contraseñas de usuarios para que en el archivo de configuración no estén en claro.

Los usuarios y contraseñas no deben ser definidos en grub.cfg esto debido a que cada que se reinicie el sistema sera sobrescrito, por esta razon debe realizarse en alguno de los ficheros dentro de /etc/grub.d.

Tanto users superusers y contraseñas durante practica lo definimos en 40_custom dentro de /etc/grub.d

# H2 Hardening Filesystems

En UNIX la seguridad depende de gran manera en "**el acceso a los archivos**", todo lo que contiene un sistema es un archivo

Cada archivo es propiedad de solo un usuario y un solo grupo, el usuario que posee el archivo puede pertenecer a varios grupos, pero el archivo solo pertenece a un grupo.
## Permisos
Cada archivo tiene 3 conjuntos de permisos, se le suele llamar "modo del archivo"

Hay tres tipos de letras que indican el tipo de permisos **rwx**, en caso de ausencia de permiso se representa con **"-"** un guion
	- r: permiso de lectura
	- w: permiso de escritura
	- x: permiso de ejecución
Ejemplo:
	-rw-r----- 1 antonio audio 4656065 Sep 13 13:06 audiofile.mp3
	 El primer "-" indica que es un fichero regular 
	 El archivo pertenece a Antonio y el grupo audio (rw-)
	 El archivo puede ser leído por cualquier usuario perteneciente al grupo audio (r--)
	 El archivo esta restringido para el resto de usuarios del sistema (---)
Para saber en numero los permisos de un archivo debemos tener en cuenta:
	r (read) → 4
	w (write) → 2
	x (execute) → 1
	- (sin permiso) → 0
Para calcular el total se suman los totales de cada uno de los 3 grupos
#### Permisos especiales
- Sticky bit (-------t), solo el propietario del archivo o del directorio puede borrar o renombrar archivos dentro, aun si otros usuarios tienen permisos de escritura
- setgid (-----s---), cuando un usuario lo ejecuta el proceso corre con los permisos del grupo propietario en lugar del usuario que lo ejecuta
- setuid(--s------), El proceso se ejecuta con los permisos del propietario del archivo en lugar de los permisos del usuario que lo ejecuta.
## Creación de Particiones

- Se crean con el comando **mkfs -t type [fs-options] device**
- Para acceder a un filesystem debe de estar montado en algún directorio del sistema
- Linux entiende diferentes tipos de filesystem, ext2, ext3, ext4, jfs, vfat, ntfs, etc.
- La sintaxis para montar sistemas de ficheros es:
- mount -t filesystemtype -o comma-separated-options device directory
Los sistemas que se montan automáticamente en el inicio se especifica en el fichero /etc/fstab, este fichero es modificable y podemos definir donde y como montar las particiones y dispositivos en el sistema de archivos.
## Particiones y Volúmenes Lógicos

Se puede tomar dos acercamientos
- Creamos sistemas de archivos como discos y particiones y lo montamos en directorios
- Combinamos diferentes dispositivos, creamos volúmenes lógicos y luego creamos el sistema de archivos sobre el Volumen lógico, esto permite agregar espacio al volumen a futuro.
## Posibles Amenazas
- Acceso no autorizado a información dentro del sistema de ficheros
	- Solución
		- Los directorios "home" permisos 700
		- Daemons deben ser world-readable
		- Restringir los permisos de ejecución innecesarios
		- Los directorios deben ser solo writeable por el admin
		- El directorio /tmp debe ser world-writeable pero con sticky bit
		- Se puede encriptar el sistema de ficheros para prevenir acceso no autorizado
- Agotando el almacenamiento, previniendo a usuarios escribir sobre el sistema de ficheros
	- Solución 
		- Establecer quotas
- Corromper el sistema haciéndolo inutilizable, ganando acceso a ejecutables maliciosos
	- Solución
		- Usar sistemas de ficheros probados y seguros, no probar opciones experimentales
		- Mantener el kernel actualizado y parchado
		- Revisar cuidadosamente permisos de ficheros
		- Mantener un ambiente estable
		- Proteger físicamente el equipo
	
## ACLs

Nos permite definir a los ficheros permisos específicos a usuarios o grupos 

Para definir permisos de usuarios y grupos se realiza con el comando:

	setfacl .m "u:user:permissions" <file/dir>
	setfacl .m "g:group:permissions" <file/dir>
Los ficheros que tienen ACLs su estructura de permisos tiene un indicador al final 
(----------+), donde el + indica que tiene una ACL aplicada

Para verificar las acl se usa el comando getfacl \<fichero>
## Quotas

Permite restringir el espacio que un usuario o grupo puede usar del sistema de archivos
Las cuotas residen en lo ficheros aquota.user o aquota.group en el directorio root

#### Tipos de limites
- Soft limit: establece una advertencia de la cantidad maxima de ficheros que puede escribir el usuario o grupo, si alcanza esto se le permitira por x tiempo sobrepasarlo pero al cumplirse el tiempo se bloqueara y el soft limit pasa a ser el hard limit
- Hard limit: es un valor fijo en el cual si el usuario o grupo llega se bloquea el permiso y no podra exceder este valor

#### Comandos utiles
- quotacheck
- quotaon, quotaoff
- edquota
- repquota, quota
## Crypting

Se utiliza cryptsetup y hay dos maneras de usarlo
- Plain type: es un enlace (link) entre crypted y el plain device, consiste en crear un mapeo entre el disco encriptado y el nombre del dispositivo
- LUKS type:  crea una cabecera en el dispositivo con las opciones de cifrado y la masterkey usando la passphrase (puede cambiarse si se tiene root access al volumen)

# H3 Hardening Applications

Todas las aplicaciones pueden clasificarse en dos categorías, las que sabemos son inseguras y las que aun no conocemos sus vulnerabilidades aun.

Es necesario deshacerse de toda aquella aplicación que no sea necesaria, minimizamos la superficie de ataque.
## Limitando recursos de las aplicaciones

Se pueden establecer limites en /etc/security/limits.conf que afectan la sesion del usuario, podemos controlar procesos, memoria, sesiones, uso de CPU etc.

Es necesario que configuremos el modulo "**pam_limits**"  para que sea efectivo.

Estos limites afectan la sesion pero no la aplicacion individualmente.

Hay hard limits los cuales se definen y no pueden ser modificados, y soft limits donde el usuario puede modificar el valor limite entre los extremos entre soft y hard limit
## Cgroups
Es una característica en el kernel linux que nos permite limitar el uso de recursos.
Los Cgroup permiten:
- Limitación de recursos
- Priorizacion de grupos para utilizar recursos
- Accounting, se puede medir y monitorear el uso de recursos de un grupo.
- Control, se puede paralizar, congelar y reiniciar grupos de procesos
Los cgroups son gerarquicos, se pueden crear cgroups dentro de otros
Los procesos que se crean por procesos pertenecientes a un cgroup pertenence a ese mismo cgroup, aunque igualmente se puede modificar la pertenencia.
Para configurar un cgroup se crea una carpeta dentro de /sys/fs/cgroups y se añade el PID y los limites a configurar

## Ejecución en jaulas chroot
Por diseño, los procesos en Linux solo conocen el directorio actual y el root
El comando chdir permite modificar el directorio sobre el cual se esta trabajando, y chroot permite cambial el directorio raíz de trabajo.
Un programa chrooted no puede acceder a ficheros fuera de su chroot ya que no tiene como nombrarlos, pero es posible configurar entornos chrooted, para esto en linux debemos de montar los diferentes directorios que necesitemos como proc sys o dev para permitir que el programa acceda a ellos dentro de su nueva raíz.

Los entornos chroot se utilizan usualmente para:
- Probar software
- Algunos servidores
- Para rescatar sistemas


## Entornos virtualizados

Esto es ideal para aislar el OS de potenciales fallos de aplicaciones, un VE es diferente de una VM, requiere de muchos menos recursos.

Usualmente se le llama a los VE contained based virtualization, los contenedores suele ofrecer menos aislamiento que un VM porque comparten parte del kernel e instancias del OS host.

La configuración de los container usualmente se realiza en /var/lib/lxc/container_nameconfig, aqui decidimos el tipo de conexion de red, si queremos que se inicie con el arranque o con delay o tambien si queremos que el contenedor lo pueda ejecutar un usuario comun.

## D.AC y M.A.C

D.A.C (Discretionary Access Control) el dueño decide que o quien puede hacer cambios sobre los ficheros y directorios, la mayoria de sistemas aplican esto.
M.A.C (Mandatory Access Control) el OS establece la politica de quien accede independientemente de los permisos que tengan los usuarios.

MAC usa la politica de minimo privilegio, se comprueba primero DAC y luego MAC, siempre denegando el acceso siempre que uno de los dos deniegue.

Las soluciones en Linux de MAC son SELinux y Apparmor

### AppArmor

Impone restricciones a rutas, puertos, sockets y varios mecanismos de entrada y salida. 

Para verificar si esta habilitado por defecto se realiza cat /sys/module/apparmor/parameters/enabled y con aa-status se listan todos los perfiles cargados, ademas con la opcion -Z del comando ps pdoemos ver sl status de confinamiento de un proceso.
Por cada aplicación bajo el control de apparmor se tiene un perfil en /etc/apparmor.d

Comandos de interes:
- apparmor_parser -r, un perfil de aplicacion (-r sirve para reemplazar si ya hay uno)
- aa-disable, deshabilitamos un perfil de aplicación
- aa-enforce y aa-complain, para colocar en enforce o complain
- aa-easyprof, sirve para crear un perfil de aplicación vacío
### SELinux

Son una serie de parches para el kernel de Linux que permiten utilizar M.A.C, en este cada aplicación, fichero.... esta marcado (labeled) y el acceso a estos solo se permite siempre y cuando haya una regla especifica en la política que así lo indique, en caso de no haber una regla especifica este denegara por defecto.

Una política son un conjunto de reglas, y cada regla describe una interacción entre proceso y fichero.

SELinux se puede aplicar de dos maneras:
- Enforcing, la política se aplica activamente, denegando el acceso cuando sea necesario (solo hay un registro en el log, la primera vez que se deniega)
- Permissive, la política no restringe activamente, cada vez que un acceso debe ser denegado se aplica (se genera un log cada ves que hay una entrada)
Los comandos **getenforce** y **setenforce** permite ver y configurar el modo actual
Para poder habilitar SELinux en Debian debemos tener instalado algún sistema de ficheros del tipo ext o jfs, ademas para adquirir la política por defecto se deben instalar ciertos paquetes y por ultimo ejecutar selinux-activate para configurar el Grub y que se re-etiquete en el siguiente reinicio.

Al tener SELinux corriendo, cada fichero/proceso es etiquetado con lo que se llama selinux context

Selinux context consiste de 4 etiquetas selinux_user:selinux_role:selinux_type:selinux_level

Con los comandos **chcon, restorecon, secon y runcon** podemos modificar el acceso o modificar el contexto de ficheros y procesos.

# H4 Protección de cuentas de usuario

### Usuarios

Un usuario es una entidad del sistema que puede poseer ficheros, directorios, dispositivos etc, crear y ejecutar procesos. Estos usuarios se identifican con un numero UID, los permisos de un archivo especifican lo que un usuario puede hacer con un archivo en especifico, siempre hay un usuario especial (uid=0 root) que puede acceder todos los archivos, señalar todos los procesos y hacer todas las llamadas que desee del sistema

Todo archivo del sistema tiene una unica propiedad, y las credenciales de los procesos indican que usuario esta detras de la ejecucion de dicho proceso.

Hay unos usuarios espeificos, denominados pseudousers los cuales solo existen para ejecutar servicios especificos y poseer los ficheros asociados a estos.

### Grupos

Es un conjunto de usuarios agrupados para una razon en especifica, estos sonidentificados por un GID, 

## Ficheros de definicion de usuarios y grupos

La informacion de usuarios es definida de manera local y almacenada en las dos siguientes rutas:

- /etc/passwd, este fichero define las cuentas de usuario en el sistema
- /etc/shadow, este fichero contiene las contraseñas de dichos usuarios, esto solo se encuentra en sistemas nuevos.
La informacion de definicion de grupos:
- /etc/group, este fichero define los grupos 
- /etc/gshadow, este fichero define las contraseñas de los grupos, tambien se encuentra el administrador de los grupos existentes (usuario que puede cambiar la contraseña del grupo o modificar los miembros de este)
## Módulos PAM

PAM (Plugabble Authentication Modules), permite  modificar los mecanismos de autenticacion sin alterar las aplicaciones.

Es una API generalizada para servicios asociados a autenticacion, permite a un administrador agregar nuevos métodos de autenticacion a traves de la instalación de nuevos módulos PAM
Permite a un administrador modificar políticas de autenticación a traves de la modificación de archivos de configuración

Si borras el archivo PAM  de configuración te deja fuera del sistema.

PAM se puede implementar de diferentes maneras al igual que su configuración que se puede evidenciar en:
- Ubicación y formato del archivo de configuración
- La ubicación de la librería PAM
- Lista de los módulos disponibles

Los módulos PAM pueden gestionar:
- Autenticacion
- Manejo de cuentas (horarios de acceso desde ciertos equipos)
- Manejo de sesión
- Manejo de contraseñas
Un modulo PAM es un pedazo de código auto contenido que implementa primitivas en una o varias instancias de mecanismos específicos.
- sufficient, si este modulo indica acceso, se permite y no se verifica mas 
- requisite, si este modulo deniega el acceso, se deniega y no se verifica mas.
- required, Es necesario que este modulo otorgue acceso, y se evalúa el resto
- optional, Este modulo se evalúa si el resultado del resto de módulos no es deterministico.
- \[new syntax]
#### Configuracion de los modulos PAM \[new syntax]
\[value1=action1 value2=action2........ valueN=actionN]
###### Value
Puede tomar los siguientes valores:
- success
- open_err
- symbol_err
- service_err
	\.
	\.
	\.
	\.
- default
donde default indica que todos los valores que no se indican explicitamente en el listado
##### action
Puede tomar las siguientes acciones:
- ignore: El estado del módulo no contribuye al código de retorno de la aplicación.
- bad: Debe considerarse como retorno negativo.
- die: Termina inmediatamente la pila y el módulo PAM y vuelve a la aplicación.
- ok: Debe considerarse como código de retorno positivo.
- done: Igual que OK pero termina la pila y el módulo.
- reset: Limpia la memoria del stack y empieza con el siguiente módulo.
Los módulos suelen estar localizados en lib/security y su configuración se lleva a cabo en /etc/pam.d o en el pam.conf.

En el pam.conf la sintaxis viene precedida del servicio.

## Modulos PAM comunes

-  pam_deny: Bloquea autenticaciones.
- pam_getenv: Recupera variables de entorno definidas en PAM.
- pam_rhosts: Autenticación basada en archivos .rhosts.
- pam_unix: Autenticación mediante passwd y shadow.
- pam_winbind: Autenticación de AD a través de Samba/Winbind
- pam_permit: Permite acceso.
- pam_access: Control de acceso basado en reglas definidas en security/access.conf.
- pam_cracklib: Reglas de seguridad para contraseñas.
- pam_env: Carga variables de entorno.
- pam_debug: Registro de depuración detallado.
- pam_echo: Mensajes por pantalla.
- pam_exec: Ejecuta programas o scripts.
- pam_ftp: Autenticación anónima.
- pam_localuser: Autenticación con usuarios locales.

## Fortificacion de la autenticacion

Autenticacion es el metodo a traves el cual una entidad acredita su identidad contra el sistema, las mas comunes son dispositivos fisicios, mediciones biometricas, certificados digitales y contraseñas.

### Refuerzo de contraseñas

Debemos de restringir el acceso al fichero /etc/shadow, se guarda un bloque de texto cifrado no la contraseña en si, usar un salt para producir diferentes cifrados a partir de una misma contraseña, usar algoritmos de cifrado lentos y complejos, y por ultimo definimos una política de composición de contraseñas

La mayoria de esta configuracion se realiza en los pam modules especificamente:
- /etc/pam.d/login
- /etc/pam.d/common-auth
- /etc/pam.d/common-password
Para el login grafico se ajusta en:
- /etc/pam.d/lightdm
- /etc/pam.d/slim
- /etc/pam.d/gdm

#### Principales Modulos PAM para refuerzo:
- pam_unix 
- pam_pwquality
- pam_pwhistory
- pam_securetty
- pam_faildelay
- pam_google_authenticator
### Autenticacion en dos pasos

Se utilizan dos metodos de en vez de uno para autenticar, por convencion el primer metodo es la contraseña y el segundo pueden ser varias opciones como google auth

### Limitando privilegios: Shells restringidas

Consiste en asignar a uno o varios usuarios shells limitadas, donde no pueden realizar ciertos comandos o acciones.

Una restricted shell tiene las siguientes caracteristicas:
- No puede ejecutarse cd, asi el usuario esta confinado al directorio actual
- No puede ejecutarse nada relacionado con /, asi solo se le permite ejecutar al usuario lo que este en su PATH
- No se permite modificar variables de entorno, como el PATH
- No se permite redirigir inputs estandar, salidas o errores usando operadores de redireccion
- No se permite salir del modo restringido, ni directamente ni a traves del uso de scripts.

Para asignar una shell restringida debemos establecer la shell restringida como la shell de login del usuario, crear un directorio /bin en el home de dicho usuario, creamos enlaces simbólicos a los programas que queremos permitirle utilizar en su $HOME/bin, creamos los archivos de configuración de su shell y los hacemos pertenecientes al root y sin permiso de escritura, en esos mismos ficheros de configuración definimos el PATH que sera su $HOME/bin, le damos permisos de pertenencia adecuados de manera que pueda escribir pero no borrar ficheros de configuración de la shell

## Convertirse en Root

Hay tres maneras de convertirse en Root
- Inicio de sesión directo como root
- Comando su
- Comando sudo
Loggearse como root debería estar siempre desactivado, se puede adivinar, y no queda registro en el sistema de quien se hizo root, para desactivar el login directo como root se puede usar el modulo securetty en /etc/securetty y listar el modulo pam_securetty en /etc/pam.d/login y /etc/pam.d/login_grafico_utilizado

El acceso mediante comando debe configurarse, solo los usuarios definidos en configuración puedan hacerse root, esto puede realizarse mediante el modulo pam.wheel

### Sudo y sudoers

El comando sudo permite a cualquier usuario permitido ejecutar comandos en nombre de root, si te hace root tienes todos los privilegios de esta cuenta

En el fichero /etc/sudoers.d se puede configurar permisos específicos para usuarios, siempre se recomienda editar dicho fichero con **visudo**

Se puede definir alias tanto para usuarios como para comandos, un ejemplo completo definiendo alias para ambos y por ultimo indicando que pueden ejecutar dicha accion como sudo seria:

User_alias DOWNDOERS = pepe, pepa, user2
Cmnd_alias POWERDOWN = /sbin/shutdown, /sbin/halt, /sbin/reboot, /sbin/restart

DOWNDOERS rutercillo=(root) POWEDOWN

donde rutercillo es el hostname de la maquina 

# H5 Hardening the Network

## Configuracion de red en Debian based systems

### Configuracion basica de red


Una interfaz de red tiene que tener como requerimientos mínimos:
- Direccion ip
- Mascara de red
- Dirección de broadcast

Hay dos tipos de formas de configurarla, manualmente o mediante DHCP, para revisar dichas configuraciones hay dos comandos claves, **ip** e **ifconfig** suelen estar ubicados en /sbin

La configuración del DNS reside en el fichero /etc/resolv.conf, este fichero permite introducir el nameserver (hasta 3) para la dirección y el domain para el dominio local

El fichero /etc/hosts, permite definir las ip definidas localmente y adjuntar un hostname correspondiente a estos.

El fichero /etc/nsswitch.conf define la fuente de donde se obtienen la información de name-service de distintas categorías, como hosts, users, mail aliases etc.., ademas de el orden en que debe hacerse la solicitud de esta información.

### Configuracion de las NIC

Antiguamente se definían por el orden de detección del sistema, ahora se asignan nombres a las interfaces la primera vez que se detectan y se guarda en las reglas udev, el nuevo esquema asigna los nombres dependiendo de donde y como se conectan al sistema lo que facilita la sustitución de NICs.

Comandos para configurar:
- dhclient interface_name, configura usando dhcp
- ifconfig interface_name...... configura la NIC con ip, mascara y broadcast
- ip addr add........., configura la NIC con la ip addr

Rutas importantes:
- /etc/init.d/networking or systemctl. si queremos configurar la NIC automáticamente en arranque
- /etc/network/interfaces, Para configurar manualmente la NIC, Debian y derivados revisan este fichero al configurar
- /etc/hostname, Contiene el nombre del sistema, nombre de dominio o el nombre del nodo

### Network Manager

Es un paquete instalado en la mayoría de Linux, es un demonio que en segundo plano gestiona todas las NIC no declaradas en los ficheros de configuracion, su configuracion esta en /etc/NetworkManager/NetworkManager.conf, se compueba con el comando **nmcli dev status**

Para evitar que NM controle las NIC, deben de configurarse en interfaces las NIC, y el fichero de NW debe tener los plugins=ifupdown y managed=false

### Interface Aliasing

Consiste en asignar mas de una ip a una NIC, se usa el comando **ip* addr** o mediante ajuste de la configuracion del fichero **/etc/network/interfaces**


### Inetd

Tambien conocido como el "internet superserver", es el encargado de los servicios de internet y gestionar las conexiones, permitiendo que los server programs solo se ejecuten cuando es necesario.

Dos ficheros controlan la configuración de inetd, /etc/services y /etc/inetd.conf

Este fichero tiene un mapa donde establece la relación entre el numero de puerto y el protocolo asociado al servicio


## Access Control TCP Wrappers

Es una capa adicional de seguridad que se situa entre el servicio inetd y los server programs para realizar control de acceso basado en hostnames, direcciones ip o solicitudes de identidad.

tcpd es llamado por inetd y recibe la peticion, este verifica sus archivos de configuracion y determina si se permite o deniega el acceso, si se permite tcpd inicia el server program proporcionado como parametro.

La configuracion de tcpd se realiza en /etc/host.allow y /etc/host.deny, aplica por orden, si no se permite, por defecto se denegara el acceso

## Access Control Packet Filtering

Consiste en verificar la cabecera de cada uno de los paquetes de red que recibe, despues de analizar se decide una accion que puede ser:
- Aceptar
- Rechazar
- Drop
En Linux se utiliza Netfilter para esto, importante que tras reiniciar se pierde la configuracion, por esta razon debe incluirse en los scripts de inicio.

Netfilter posee distintas tablas para las diferentes funciones que soporta, siendo **filter** la tabla para el filtrado de paquetes

La tabla **filter** trabaaja con cadenas, cada cadena tiene una serie de reglas que operan a los paquetes pertenecientes a dicha cadena.

Las reglas se verifican en orde, cuando un paquete hace match con una regla se ejecuta no mas reglas se verifican con dicho paquete.

En caso de no hacer match con ninguna regla la accion por defecto de la cadena es la que se aplica.

Tipos de cadena

- Input, paquetes que estan destinados a procesos de nuestro sistema
- Output, paquetes que se originan en el sistema y tienen destino exterior
- Forward, paquetes que llegan a nuestro sistema pero tienen un destino diferente.
### IPtables

Este programa es con el que se modifica la tabla **filter** de **Netfilter**
- Permite, crear borrar y modificar la politica por defecto de cadenas
- Listar las reglas en una cadena
- Borrar todas las reglas en una cadena
### Conformación de las reglas
- Selección de paquetes
- Acción a tomar
#### Selección de paquetes

Para definir una regla debemos primero seleccionar el paquete, esto se hace:
- protocolo
- puerto de origen
- puerto de destino
- interfaz de entrada
- interfaz de salida
#### Acciones a tomar
- Drop, se tira (no response)
- Reject, se rechaza (connection refused)
- Accept, se acepta 
- Log, se genera un log para este paquete, esta accion no hace que termine el chequeo de reglas de este paquete
Podemos guardar la configuracion actual de la table filter de Netfilter con el comando iptables-save

### Nftables
Es el framework de clasificación de paquetes moderno en el Kernel Linux, los conjuntos de reglas se disponen en forma de arbol para reducir los tiempos de inspección, para acceder a ellos se usa el comando **nft**, siempre podemos utilizar las viejas iptables para acceder al filtrado de paquetes en el kernel.

**Diferencias con iptables**: La sintaxis es distinta, no tiene tablas o cadenas por defecto, múltiples acciones por regla en forma de expresiones, soporte a nuevos protocolos y existe un comando de traducción de iptables a nftables.

Si queremos tener configuración persistente se pueden incluir las reglas en nftables.conf y se cargaran al arrancar el sistema. Para listar las reglas se usa nft list ruleset.

Cada tabla se aplica sobre una familia de direcciones: ip, ip6, inet, bridge y arp. Las tablas se crean con nft add table familia nombre y se listan con nft list tables.

Para crear una cadena se utiliza nft add chain familia nombreTabla nombreCadena.

Hay dos tipos de cadenas:
- Cadenas normales: Se usan como objetivo de saltos.
- Cadenas base: Se registra en uno de los Hooks de netfilter, en su creación se debe indicar el tipo (filter, route, nat), el hook (prerouting, input, forward, output, postrouting), la prioridad (numérico) y la política (accept o drop). La policy se establece por defecto si no cumple ninguna regla.

Para añadir una regla se usa nft add rule family nombreTabla nombreCadena matches statements. Los matches nos permiten seleccionar los paquetes y los statements las acciones. Con insert podemos añadirla en la posición que queramos handle X.

Los matches pueden ser el protocolo, direcciones origen y destino, puerto origen y destino, tipo de icmp, estado de conexión, etc.

Los statements pueden ser:

- Accept
- Drop
- Queue: Pone en cola en el espacio de usuario y detiene la evaluación.
- Continue
- Return
- Jump chain: Permite indicar a que cadena debe saltar para su evaluación y vuelve.
- Goto chain: Igual pero no vuelve.
- Log 
- Reject: Para conexiones ICMP.
- Limit rate.
- Dnat, Snat, Masquerade, Redirect: Para acciones específicas de red.

# H6 Mantenimiento

La seguridad no es una meta es una labor constante, el mantenimiento de un sistema se basa en el proceso de aplicacion de parches, actualizacion de informacion de vulnerabilidades y monitorizacion de la actividad del sistema de manera recurrente.

La principal fuente de informacion es el subsistema de logs, todo lo que ocurre puede configurarse para que genere una entrada en los logs. Los logs de autenticacion y sistemas criticos ademas de registrarse en local se sugiere enviar a otras maquinas.

### Logs, logfiles y syslog

Systemd toma control sobre la mayoria por no decir todos los servicios de una maquina, systemd almacena los logs en formato binario dentro de **systemd-journald**, y pueden consultarse mediante el programa **journalctl**.

Aun teniendo systemd se pueden instalar programas tradicionales como syslog o rsyslog, que permiten configurar y revisar de manera mas cómoda, como también su mantenimiento.

#### Log
Es una descripción de un evento que ocurrió durante la ejecución de un proceso en el sistema, aun cuando los programas pueden llevar sus propios logs, suele haber un demonio tipicamente syslogd  que aglutina de manera centralizada los logs de diferentes programas, la mayoria de sistemas Linux almacenan estos en **/var/log** o alguno de sus subdirectorios.

### Configuracion de los logs

Para gestionar que se hace con los logs debe especificarse en el archivo de configuracion, este fichero se suele encontrar en **/etc/syslog.conf o /etc/rsyslog.conf**

Los logs se clasifican en función de que servicio ha generado el log(facilities) , y en funcion de la severidad de este (severity).

Usual facilities en syslog: auth, authpriv, cron, daemon, ftp, kernel, lpr, mail,news, syslog, user, uucp
Usual severities en syslog: emerg, alert, crit, err, warning, notice, info, debug.

El formato de la configuracion de logs consiste en:

selector \<tab> action
El Selector elige los logs basados en "facility" y "severity" con la estructura facility.severity, algunos sistemas permiten definir listas , como hay otros que permiten el uso del wildcard \* para facility y/o severity.

facility1,facility2.severity
o
facility1.severity1; facility2.severity2

La accion determina que debe hacerse con el log seleccionado por el selector
- Escribir el log en un fichero
- Notificar a los usuarios

### Extensiones

Es necesario indicar a syslog cuando queremos recibir logs enviados de otra maquina a la nuestra, normalmente este parámetro se define en **/etc/default/syslog** 

### Rotación de logs

Los logs crecen con el tiempo y terminan ocupando mucho espacio, por esta razon es necesario rotarlos creando nuevos ficheros cuando se alcanza cierto tamaño y/o antigüedad.

Logrotate es un proframa estandar en Linux que permite realizar este proceso, permite rotar, comprimir, remover..... los ficheros de log en sistemas Linux, se suel correr a diario usando cron.

Su configuracion se ajusta en /etc/logrotate.conf permitiendo especificar opciones segun cada fichero a rotar.

### Lynis

Es una herramienta que permite realizar una auditoria del sistema, esta se encarga de escanear la configuracion del sistema y se ejecuta desde la linea de comandos, su salida es un resumen de lo que se ha comprobado y lo que se ha encontrado.


