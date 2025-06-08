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

## 2025-06-08

### [Feat] Añadir sidebar collapsible y eliminar íconos superiores en desktop

- Modificados:
  - crunevo/templates/base.html
  - crunevo/templates/navbar.html
  - crunevo/static/js/main.js
  - crunevo/static/css/style.css
  - crunevo/templates/components/sidebar_icons.html (nuevo)

- Detalles:
  - Se ocultan los íconos del navbar en escritorio y se muestran en un sidebar colapsable.
  - El contenedor principal se desplaza con `ms-lg-6`.
  - Toggle manejado con JS y estilos añadidos.

- Pruebas:
  ✅ `pip install -r requirements.txt`
  ✅ `PYTHONPATH=. pytest -q crunevo/tests`

### [Refactor] Cambiar sidebar de íconos a burbuja flotante inferior derecha

- Modificados:
  - crunevo/templates/components/sidebar_icons.html
  - crunevo/templates/base.html
  - crunevo/static/js/main.js
  - crunevo/static/css/style.css

- Detalles:
  - Se reemplazó el sidebar lateral izquierdo por un menú flotante en la esquina inferior derecha para escritorio.
  - Se eliminó el ícono de “Salir” y se agregó un botón flotante con toggle.
  - Se aplicaron estilos y transiciones CSS para una mejor experiencia.

- Pruebas:
  ✅ `pip install -r requirements.txt`
  ✅ `PYTHONPATH=. pytest -q`
