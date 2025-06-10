# Despliegue de Crunevo en Railway

## 1. Requisitos
- Python 3.x
- Gunicorn
- `requirements/requirements-core.txt` para instalar solo lo esencial

## 2. Configuración en Railway

### Base de datos
- Activa el plugin PostgreSQL de Railway.
- Obtén la URL de conexión y configúrala en `SQLALCHEMY_DATABASE_URI`.

### Comando de inicio
```bash
gunicorn -b 0.0.0.0:$PORT run:app
```

## 3. Notas
Railway gestionará la base de datos PostgreSQL de forma automática.

Instala las dependencias con:

```bash
pip install -r requirements/requirements-core.txt
```

