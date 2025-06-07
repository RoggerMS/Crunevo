# AGENTS.md – Guía para Agentes de Código (Codex, etc.)

## Estructura del Proyecto
- `crunevo/models/`: Modelos de SQLAlchemy
- `crunevo/routes/`: Blueprints de Flask organizados por módulo
- `crunevo/templates/`: Plantillas Jinja2 (HTML) por sección
- `crunevo/static/`: Archivos estáticos (CSS, JS, imágenes)
- `crunevo/tests/`: Tests con Pytest para rutas, modelos y seguridad

## Estándares de Código
- Formato: usa `black` con 88 caracteres por línea
- Control de acceso: usa `@login_required` para rutas protegidas
- Flash messages: `'success'`, `'danger'`, `'warning'`, `'info'`
- Validación: valida campos con `.strip()` y longitud mínima

## Comandos Clave
```bash
pip install -r requirements.txt
export FLASK_APP=crunevo/app.py
flask db upgrade
PYTHONPATH=. pytest -q crunevo/tests
```

### Migraciones
Se crean con:

```bash
flask db migrate -m "mensaje"
flask db upgrade
```

## Flujo de Pull Request
Título: [Feat], [Fix], [Refactor] según el caso

Cuerpo:

Resumen de cambios

Pruebas realizadas

Notas (migraciones nuevas, archivos añadidos, etc.)

## Antes de Hacer Commit
```bash
black .
pytest -q
```
