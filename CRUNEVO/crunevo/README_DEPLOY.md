# Proyecto Apuntes Cantuta - Instrucciones de Despliegue

Este archivo contiene instrucciones básicas para desplegar la aplicación Flask "Apuntes Cantuta" en tu propio servidor.

## Estructura del Proyecto (dentro de `deployment_cantuta_app`):

-   `src/`: Contiene el código fuente principal de la aplicación Flask.
    -   `main.py`: Punto de entrada de la aplicación, configuración de Flask, SQLAlchemy, etc.
    -   `models/`: Define los modelos de la base de datos (User, Note, Product).
    -   `routes/`: Define las rutas y la lógica de las vistas de la aplicación.
    -   `static/`: Contiene los archivos estáticos.
        -   `css/`: Hojas de estilo CSS, incluyendo `bootstrap.min.css` (local) y `style.css` (personalizado).
        -   `images/`: Imágenes utilizadas por la aplicación (ej. `default_avatar.png`).
        -   `js/`: Archivos JavaScript (si los hubiera).
    -   `templates/`: Plantillas HTML de Jinja2.
    -   `instance/`: Este directorio se creará automáticamente al ejecutar la aplicación y contendrá la base de datos SQLite (`plataforma_apuntes.db`). Asegúrate de que el servidor tenga permisos para escribir en esta ubicación dentro de `src/`.
-   `requirements.txt`: Lista todas las dependencias de Python necesarias para el proyecto.
-   `venv/`: Entorno virtual de Python (generalmente no se sube al servidor, se recrea allí).
-   `.env`: Archivo para variables de entorno (ej. `SECRET_KEY`, `DATABASE_URI`, `DATABASE_DIR`). **Importante:** este archivo contiene información sensible y debe configurarse adecuadamente en el servidor. Puedes definir `DATABASE_DIR` para indicar un directorio con permisos de escritura donde se creará la base de datos SQLite. Si no se define, la aplicación intentará crearla dentro del proyecto y, si ese lugar es de solo lectura, utilizará `/tmp` de forma automática.

## Pasos Generales para el Despliegue:

1.  **Requisitos del Servidor:**
    *   Python 3.x
    *   `pip` (manejador de paquetes de Python)
    *   Un servidor WSGI como Gunicorn o uWSGI (recomendado para producción en lugar del servidor de desarrollo de Flask).
    *   Un servidor web como Nginx o Apache (opcional, pero recomendado para servir archivos estáticos y como proxy inverso).

2.  **Subir los Archivos:**
    *   Sube el contenido de la carpeta `deployment_cantuta_app` (o el ZIP que te proporcionaré) a tu servidor, excluyendo idealmente la carpeta `venv` (se recreará).

3.  **Crear y Activar un Entorno Virtual:**
    ```bash
    cd ruta/a/deployment_cantuta_app
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar Variables de Entorno:**
    *   Crea o edita el archivo `.env` en la raíz de `deployment_cantuta_app`.
    *   Asegúrate de que `SECRET_KEY` sea una clave fuerte y única.
    *   Verifica que `DATABASE_URI` (o `DATABASE_DIR`) apunte a una ubicación con permisos de escritura para la base de datos. Si usas SQLite, puedes establecer `DATABASE_DIR` con el directorio deseado y la aplicación generará allí el archivo `crunevo.sqlite3`.

6.  **Inicializar la Base de Datos (si es la primera vez):**
    *   La aplicación está configurada para crear las tablas y el directorio `instance/` automáticamente al iniciarse si no existen. No obstante, verifica que esto ocurra o ejecuta un script de inicialización si es necesario.

7.  **Ejecutar con un Servidor WSGI (Ejemplo con Gunicorn):**
    *   Instala Gunicorn: `pip install gunicorn`
    *   Ejecuta la aplicación (desde el directorio `deployment_cantuta_app` donde está `src/`):
        ```bash
        gunicorn --workers 4 --bind 0.0.0.0:PUERTO_DESEADO src.main:app
        ```
        Reemplaza `PUERTO_DESEADO` por el puerto en el que quieres que corra la aplicación (ej. 8000).
        El `src.main:app` le dice a Gunicorn que busque el objeto `app` de Flask dentro del archivo `main.py` que está en el paquete `src`.

8.  **Configurar un Servidor Web (Nginx/Apache - Opcional pero Recomendado):**
    *   Configura Nginx o Apache para que actúe como proxy inverso hacia Gunicorn y para servir los archivos estáticos directamente (desde `src/static/`). Esto mejora el rendimiento y la seguridad.

## Consideraciones Adicionales:

*   **Modo Debug:** Asegúrate de que `debug=False` en `src/main.py` para producción.
*   **Archivos Estáticos:** Verifica que las rutas a los archivos estáticos (CSS, JS, imágenes) sean correctas y que el servidor web (o Flask en desarrollo) los esté sirviendo adecuadamente.
*   **Permisos:** Asegúrate de que el usuario con el que corre la aplicación tenga los permisos necesarios para leer los archivos del proyecto y escribir en el directorio `instance/` (para la base de datos SQLite).
*   **Seguridad:** Revisa las configuraciones de seguridad de Flask y de tu servidor.

¡Mucha suerte con el despliegue!
