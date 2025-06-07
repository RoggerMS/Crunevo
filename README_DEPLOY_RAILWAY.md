# Despliegue de Crunevo en Railway

## 1. Requisitos
- Python 3.x
- Gunicorn
- `requirements.txt` en la raíz

## 2. Configuración en Railway

### Volumen
- Añadir un volumen persistente
- Mount path sugerido: `/mnt/data`

### Variables de entorno
- `RAILWAY_VOLUME_MOUNT_PATH=/mnt/data`
  *(o alternativamente `DATABASE_DIR=/mnt/data`)*

### Comando de inicio
```bash
gunicorn -b 0.0.0.0:$PORT CRUNEVO.run:app
```

## 3. Notas
La base de datos SQLite se almacenará dentro del volumen.

Sin volumen, los datos se perderán al reiniciar.

