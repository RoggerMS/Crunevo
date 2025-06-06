# Proyecto Apuntes Cantuta - Instrucciones de Despliegue

Este archivo contiene instrucciones básicas para desplegar la aplicación Flask "Apuntes Cantuta" en tu propio servidor.

## Estructura del Proyecto (dentro de `deployment_cantuta_app`):

-   `crunevo/`: Contiene el código fuente principal de la aplicación Flask.
    -   `app.py`: Define la función `create_app()` y registra los blueprints.
    -   `models/`: Define los modelos de la base de datos (User, Note, Product).
    -   `routes/`: Define las rutas y la lógica de las vistas de la aplicación.
    -   `static/`: Contiene los archivos estáticos.
        -   `css/`: Hojas de estilo CSS, incluyendo `bootstrap.min.css` (local) y `style.css` (personalizado).
        -   `images/`: Imágenes utilizadas por la aplicación (ej. `default_avatar.png`).
        -   `js/`: Archivos JavaScript (si los hubiera).
    -   `templates/`: Plantillas HTML de Jinja2.
    -   `instance/`: Este directorio se creará automáticamente al ejecutar la aplicación y contendrá la base de datos SQLite (`plataforma_apuntes.db`). Asegúrate de que el servidor tenga permisos para escribir en esta ubicación dentro de `crunevo/`.
-   `run.py`: Script de arranque que crea la aplicación con `create_app()`.
-   `requirements.txt`: Lista todas las dependencias de Python necesarias para el proyecto.
-   `venv/`: Entorno virtual de Python (generalmente no se sube al servidor, se recrea allí).
-   `.env`: Archivo para variables de entorno (ej. `SECRET_KEY`, `DATABASE_URI`). **Importante:** Este archivo contiene información sensible y debe configurarse adecuadamente en el servidor. La `DATABASE_URI` actual apunta a un archivo SQLite local dentro de `crunevo/instance/`. Si usas una base de datos diferente en producción, deberás actualizar esta URI.

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
    *   Verifica que `DATABASE_URI` apunte a la ubicación correcta de tu base de datos. Si usas SQLite, la ruta actual (`sqlite:////ruta/completa/a/deployment_cantuta_app/crunevo/instance/plataforma_apuntes.db`) debe ser correcta y el directorio `crunevo/instance` debe tener permisos de escritura.

6.  **Inicializar la Base de Datos (si es la primera vez):**
    *   La aplicación está configurada para crear las tablas y el directorio `instance/` automáticamente al iniciarse si no existen. No obstante, verifica que esto ocurra o ejecuta un script de inicialización si es necesario.

7.  **Ejecutar con un Servidor WSGI (Ejemplo con Gunicorn):**
    *   Instala Gunicorn: `pip install gunicorn`
    *   Ejecuta la aplicación (desde el directorio `deployment_cantuta_app` donde están `run.py` y la carpeta `crunevo/`):
        ```bash
        gunicorn --workers 4 --bind 0.0.0.0:PORTA_DESEJADA 'crunevo.app:create_app()'
        ```
        Reemplaza `PORTA_DESEJADA` por el puerto en el que quieres que corra la aplicación (ej. 8000).
        El comando anterior indica a Gunicorn que ejecute la función `create_app()` definida en `crunevo/app.py` para obtener la aplicación de Flask.

8.  **Configurar un Servidor Web (Nginx/Apache - Opcional pero Recomendado):**
    *   Configura Nginx o Apache para que actúe como proxy inverso hacia Gunicorn y para servir los archivos estáticos directamente (desde `crunevo/static/`). Esto mejora el rendimiento y la seguridad.

## Consideraciones Adicionales:

*   **Modo Debug:** Asegúrate de que `debug=False` en `run.py` (o en la configuración) para producción.
*   **Archivos Estáticos:** Verifica que las rutas a los archivos estáticos (CSS, JS, imágenes) sean correctas y que el servidor web (o Flask en desarrollo) los esté sirviendo adecuadamente.
*   **Permisos:** Asegúrate de que el usuario con el que corre la aplicación tenga los permisos necesarios para leer los archivos del proyecto y escribir en el directorio `instance/` (para la base de datos SQLite).
*   **Seguridad:** Revisa las configuraciones de seguridad de Flask y de tu servidor.

¡Mucha suerte con el despliegue!
