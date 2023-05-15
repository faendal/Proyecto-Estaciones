# Proyecto-Estaciones

Proyecto de contenedores para mostrar el estado de las estaciones de nivel de agua del SIATA.

Dentro del proyecto se encuentran:

 1.**Archivos Dockerfile :** Se encuentran dos archivos Dockerfile para construir las dos imágenes necesarias para correr el contenedor que contendrá la api con toda la información de las estaciones y el contenedor con la aplicación web que mostrará esta información gráficamente
 2. **Scripts .py:** Estos contienen el código utilizado para que las aplicaciones funcionen correctamente
 3. **Archivos requirements.txt.** Se encuentran dos archivos de requerimientos que indican que librerías se deben instalar en cada contenedor para permitir la ejecución del código
 4. **Base de datos:** Una pequeña base de datos .csv que contiene los usuarios y las contraseñas permitidas para ingresar a la página principal. Es utilizada como volumen en el contenedor web.
 5. **Archivo bash:** El proyecto contiene un archivo bash script que ejecuta todas las instrucciones necesarias para que el proyecto corra. Sin embargo, como docker requiere que los volúmenes sean creados con rutas absolutas, antes de correr este bash script, es necesario que la persona haga los cambios de rutas correspondientes a su propio equipo

Si se modifica el archivo "despliegue.sh" de manera que las rutas absolutas para el volumen funcione, para correr el proyecto, basta con hacer:

    bash despliegue.sh
   
   De lo contrario y si se quiere hacer este despliegue a mano, los pasos recomendados a seguir son los siguientes:
   

 1. Construir las imágenes: 
	 1.1. `sudo docker build . -f DockerfileApi -t api:01`
	 1.2. `sudo docker build . -f DockerfileFront -t front:01`
 2. Correr el contenedor que captura la api: Este tendrá conexión con el servidor dueño de la api a través del puerto 8089 y se ejecutará a través del puerto 5000. El código de ejecución es el siguiente: 
 `sudo docker run -d -p 5000:5000 -p 8089:8089 api:01`
 3. Correr el contenedor con la aplicación web: Este se ejecuta a través del puerto 80. Interiormente, a través del código, este se conecta a través del puerto 5000 con el contenedor de la api para capturar los datos que este tiene. Además, en este se crea el volumen para poder leer la base de datos que contiene los pares de usuario y contraseña válidos para la autenticación (véase el archivo contenido en el directorio dB/ para probar el funcionamiento). Para ejecutarlo se hace, teniendo nuevamente la salvedad que para el volumen es necesaria una ruta absoluta que cambiará entre diferentes equipos y por lo tanto es posible que deba modificarse:
  `sudo docker run -d -v /home/ubuntu/ATIVA/dB:/front/db -p 80:80 front:01`