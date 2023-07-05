# Aplicación 
En esta carpeta podemos encontrar los archivos necesarios para el funcionamiento de la aplicación.
# Estructura de archivos de la aplicación
Para la estructura de la aplicación se ha utilizado el patrón de modelo-vista-controlador (MVC). 
El patrón MVC es un patrón arquitectónico que separa el sistema en tres partes, los datos, la lógica de la aplicación y la interfaz de usuario. El modelo es la capa de datos, la vista es la interfaz de usuario y el controlador, la lógica de la aplicación.

![alt text](https://github.com/fmv1001/F1RacePredictor/blob/main/docs/img/mvc.png)

En el servidor se ha aplicado este patrón de la siguiente manera:

  - `data`: Una primera carpeta de datos que contiene los datos necesarios para la aplciación: imágenes, modelos, codificadores, etc.
  - `logic`: Una carpeta llamada `logic` que contiene la lógica de negocio de la aplicación. Dentro de ella encontramos los archivos necesarios para el funcionamiento de la app.
  - `presentation`: Una última carpeta que implementa la capa de presentación (presentation). Dentro de ella encontramos el archivo `AppMain.py`, que implementa la interfaz de usuario.
