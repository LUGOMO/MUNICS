# Fortificación de Arranque
## Securizacion del GRUB
- **Interrumpir el boot** 
	Presionar la c
- **Con esto podemos ver las contraseñas del root** 
	"set pager=1" y "cat /etc/shadow"
- **Convertirse en root mediante los parámetros del KERNEL**
	Entramos al kernel al presionar "e"
	**Agregar "init=/bin/bash"** en la linea que empieza con "linux /boot......."
	Presionar Ctrl + X
- **Crear claves cifradas**
	Comando **"grub-mkpasswd-pbkdf2"**
- **Para crear los usuarios, se accede a /etc/grub.d/40.custom**	(como root)
	Sintaxis:
	**Superusuarios**
	set superusers="superusuario1,superusuario2" 
	password_pbkdf2 El usuario La clave (paso anterior)
	password El usuario La clave en plano
	
	**Usuarios normales**
	set users="usuario1,usuario2" 
	password_pbkdf2 El usuario La clave (paso anterior)
	password El usuario La clave en plano

	**SE DEBE HACER update-grub y verificar el archivo grub.cfg en /boot/grub/grub.cfg**
	Si todo esta bien te pedirá la contraseña al iniciar el grub
- **Agregar nuevas entradas al GRUB**
	Se modifica nuevamente el /etc/grub.d/40.custom
	Se toma del grub.cfg una entrada existente como:
	Este es sin autenticacion
	**menuentry 'AlwaysAvailable' --class debian --class gnu-linux --class gnu --class os --unrestricted {**
    **load_video**
    **insmod gzio**
    **if [ x$grub_platform = xxen ]; then insmod xzio; insmod lzopio; fi**
    **insmod part_msdos**
    **insmod ext2**
    **set root='hd0,msdos1'**
    **if [ x$feature_platform_search_hint = xy ]; then**
        **search --no-floppy --fs-uuid --set=root \**
               **--hint-bios=hd0,msdos1 \**
               **--hint-efi=hd0,msdos1 \**
               **--hint-baremetal=hd0,msdos1 \**
               **c8f90164-6a53-4c62-849f-2f06ac8b9f9c**
    **else**
        **search --no-floppy --fs-uuid --set=root c8f90164-6a53-4c62-849f-2f06ac8b9f9c**
    **fi**
    **echo 'Loading Linux 6.1.0-30-amd64 ...'**
    **linux /boot/vmlinuz-6.1.0-30-amd64 root=UUID=c8f90164-6a53-4c62-849f-2f06ac8b9f9c ro quiet**
    **echo 'Loading initial ramdisk ...'**
    **initrd /boot/initrd.img-6.1.0-30-amd64**
	**}**
	- **Para que pida usuarios seria --users=usuario1,usuario2 {**
	- **Luego update-grub y verifica errores**
- **Si se necesita instalar otro Cargador, se instala por terminal y al reiniciar estará **
	Ejemplo en Lilo :
	se crean entradas en /etc/lilo.conf, aqui agregas lineas de password="clave" descomentar restricted

# Fortificación de Sistema de Archivos
- **Establecer Quotas para los usuarios**
	- En el fichero fstab dentro de /etc/ se debe agregar:
		En la linea # /home was on /dev/sda3 during installation UUID=ea229802-cc4d-450a-8a85-4864b28f767f /home           ext4    defaults        0       2
		**se modifica por (ver negritas):**
		  # /home was on /dev/sda3 during installation UUID=ea229802-cc4d-450a-8a85-4864b28f767f /home           ext4    defaults,**usrquota,grpquota**        0       2
		**Debe hacerse un "
		- **systemctl daemon-reload** 
		-  **mount -o remount /home/** (remontar el home para montar el sistema de ficheros)
		- **quotacheck -ugcm /home/**  (actualizar las cuotas)
		**y se comprueba con :** 
			- **ls /home/**
			(debe aparecer ahora aquota.group y aquota.user)
	- Aplicando 
		- **edquota -t o -g**: modificacion del tiempo de gracia para crear mas ficheros de los indicados, **t para user, g para grupos**.
		- **edquota -u** **Username**: se modifica el limite que el usuario puede alcanzar soft/hard, para hacer varios usuarios debemos hacer un bucle (gpt)
			- **repquota -a**: verificar 
	- Crear grupos:
		- **groupadd nombredelgrupo**: Creas un grupo
		- **usermod -aG nombre del grupo usuario**: asignar los usuarios al grupo
		- **gpasswd -d usuario grupo**: eliminar un usuario
			- **getent group grupo**: ver los usuarios de un grupo
		- **chgrp -R nombre del grupo /home/user**
		- **chmod g+s /home/user**: para que hereden los archivos creados por los usuarios
		- **quotaoff y quotaon /home**: reiniciar las quotas
	- Uso de ACLs:
		- **setfacl -m u:user:rw /path al que quieres permitir**: modificas permisos de usuario
		- **setfacl -m g:grupo:w /path:** modificar permisos de grupos
			- **getfacl /path**: te permite verificar que permisos tiene especifico por user
			- **ls-l**: te permite verificar que permisos tiene general
- **Creación de particiones**
		- **Fdisk /dev/disco**: Programa para gestionar las particiones
			- **n:** Crear partición
			- **p:** elegir primaria
			- **+nroG:** Estructura para agregar el tamaño deseado en Gb
			- **w:** Para guardar cambios
- **Creación de crypted file system**
		- **cryptsetup open /dev/partición especifica --type plain: esto crea el sistema de ficheros cifrado modo plain 
			- **mkfs.ext4 /dev/mapper/crypt1:** formatear el dispositivo de la ruta indicada con EXT4 para que pueda almacenar datos
				**mkdir /crypt1** debemos crear un directorio y montarlo con **mount /dev/mapper/crypt1 /crypt1**
		- **cryptsetup -y -v luksFormat --type luks /dev/partición especifica:** sistema de ficheros tipo luks
			- **cryptsetup open /dev/partición especifica encriptadoLUKS**
			-  **mkfs.ext4 /dev/mapper/encriptadoLUKS**
			- **mkdir /crypt2** , **mount /dev/mapper/encriptadoLUKS /crypt2**
			- **cryptsetup luksAddkey /dev/particion:** Permite agregar mas claves
- **Creación de volúmenes físicos:**
		- **pvcreate /dev/mapper/nombres existentes**
		- **vgcreate GrupoVolumenes /dev/mapper/cada uno de los vol**
			**vgdisplay**
- **Creación volúmenes lógicos:**
		- **lvcreate -L 3G GrupoVolumenes -n Grupo** : Crea un **volumen lógico (LV)** llamado `Grupo` de **3 GB** dentro del **grupo de volúmenes (VG)** llamado `GrupoVolumenes`.
			Se debe de verificar con **vgdisplay** y adicionalmente darle formato con **mkfs** y **montarlo en /mnt por ejemplo**
- **Creación de un  directorio encriptado**
		- encfs $HOME/ .crypted $HOME/CLEAR
		- fusermounb -u $HOME/CLEAR: se desmonta CLEAR
		- encfsctl paswwd .crypted: se cambia la contraseña al fichero

# Fortificación de Aplicaciones
- **Limitar consumo de aplicaciones**
	- **cpulimit --pid nro -l nro (porcentaje a limitar)**
		lo chequeas con **top** y puedes ver el pid tambien asi
- **Contenedores**
	- **ls -l /usr/share/lxc/templates:** revisar las plantillas disponibles
	- **lxc-create -t debian MyContainers:** aqui se crea el container de tipo Debian
	- **lxc-start -n My....:** se inicia el container
	- **lxc-stop -n My.....:** se pausa el container
	- **lxc-ls -f:** permite listar los container disponibles en el sistema
	- **lxc-attach -n My.... /bin/bash:** se monta el container
		- **passwd:** permite ponerle contraseña root al container
		- **nano /etc/network/interfaces**: Cambiar la ip del container
		- **nano /etc/ssh/sshd_config**: Cambiar el puerto ssh del container
				Despues de cualquier cambio hacer systemctl restar networking y ssh
		- nano /var/lib/lxc/container-name/config 
			- agregar lxc.start.auto = 1 ; iniciar automaticamente con la maquina
			- agregar lxc.start.delay = 3 ; esperar 3 seg despues del encendido
	- **Cgroups:**
		- **mkdir /sys/fs/cgroup/name del cgroup**
		- **echo PID >> /sys/fs/cgroup/namecgroup/cgroup.procs:** permite agregar un pid de un proceso al grupo 
		- /sys/fs/cgroup/namecgroup/..... permite ver varias cosas interesantes 
			- cgroup.freeze
			- cgroup.procs
			- memory.current
			- cpu.max
	- **Apparmor**
		- Ejemplo de copiar un programa del /bin/ls a /usr/bin/listar 
			cp /bin/ls /usr/bin/listar
		- /etc/apparmor.d 
			- debe crearse un archivo usr.bin.listar
				contenido:
						/usr/bin/listar {
							/       r,
							/**     r,
							deny /etc/      r,
							deny /etc/**    r,
							}
		- se debe configurar en modo enforce
			- aa-enforce /usr/bin/listar
# Fortificación de Cuentas de Usuario
- **Bloqueo de login de terminales y gráfico**
	- **nano /etc/pam.d/login** 
	 **auth       required pam_securetty.so** restringir login terminales no seguras
	- **nano /etc/pam.d/lightdm**
		**auth      requisite pam_securetty.so** restringir login gráfico
- **Restringir quien se hace root**
	- groupadd supass y sunopass
		- usermod -aG supass y nopass
	- **nano /etc/pamd.d/su**
		auth sufficient pam_wheel.so group=sunopass root_only trust
		auth requisite pam_wheel.so group=supass root_only 
- **nano /etc/pam.d/common-password** se puede cambiar el cifrado para el /etc/shadow 
- **nano /etc/security/pwquality.conf** cambiar los requisitos de las contraseñas 
- **nano /etc/passwd** se ven la configuracion de usuarios
		Se puede restringir lo que hacen los usuarios cambiando el /bin por /rbash
		- ln -s /bin/ls /home/user010/bin/ls
		- ln -s /bin/rm /home/user010/bin/rm 
		- - ln -s /bin/vi /home/user010/bin/vi
		- - ln -s /bin/wc /home/user010/bin/wc
		Son enlaces simbólicos de ls y rm real para que el user010 los tenga en su home restringido
- **nano /home/user/.bashrc**: permite  configurar el entorno de la terminal Bash.
			 PATH=/home/user010/bin se agrega al final de ese fichero
- **chown root .*** asigna al root la propiedad de todos los ficheros que inician con "."
- **nano /etc/sudoers** 
		Permite hacer alias de comandos, permitir que otros usuarios ejecuten comandos como otro user, etc
- **sudo -l -U** Permite ver que comandos puede ejecutar un usuario como sudo
- **nano /etc/pam/login y lightdm**
		auth    sufficient      pam_succeed_if.so user ingroup usuario:usuario
		Esto hara que no se le pida contraseña a usuario en login de terminal
		auth y en el login grafico
# Fortificacion de la RED
 - **nano /etc/network/interfaces** podemos modificar las ip de las tarjetas de red
- **ip a lista las interfaces** y sus ip
- **/usr/sbin/ftpd -D** activa el ftp
- nano /etc/hosts.allow y deny permiten configurar los tcpwrappers
		sintaxis:
		ftpd: ip, ip, ip 
		sshd: ip, ip, ip
- nano /etc/inetd.conf 
	  se agrego
	  telnet stream tcp nowait root /usr/sbin/tcp telnetd
	  telnet stream tcp nowait root /usr/sbin/telnetd telnetd
	 debe hacerse un systemctl restart inetutils-inetd.service al hacer cambios
- Configuracion para nftables
	- **nft add chain inet lxc DROPFTP**
	- **nft add chain inet lxc REJECTFTP**
		- **nft add rule inet lxc DROPFTP tcp dport 21 drop**, puede ser log reject drop dependiendo de lo que se quiera
	- **nft list ruleset** permite ver las nft rules
	- nft add rule inet lxc input ip saddr {ip/mascara, ip/mascara} jump DROPFTP
	- nft add chain CONTAINER WEB tcp dport 80 dnat to 10.0.3.100:80
	- nft add rule CONTAINER SSH ip daddr {ip/masc} tcp dport 22 dnat to 10.0.3.100:100
		  Con esa regla redirigimos el trafico ssh de la nic2 al container
# Mantenimiento



# Adicional
echo 'export PATH=$PATH:/sbin' >> ~/.bashrc
source ~/.bashrc