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

### [Fix] Reposicionar men\u00fa flotante a esquina inferior derecha correctamente (2025-06-08)

- Se movi\u00f3 el men\u00fa de navegaci\u00f3n colapsable de lateral izquierdo a burbuja flotante.
- El bot\u00f3n abre/cierra los \u00edconos en pantallas grandes.
- Se elimin\u00f3 el \u00edcono de cierre de sesi\u00f3n.
- Archivos modificados:
  - `crunevo/templates/components/sidebar_icons.html`
  - `crunevo/templates/base.html`
  - `crunevo/static/js/main.js`
  - `crunevo/static/css/style.css`

### [Refactor] Rediseñar feed de apuntes para móviles con estilo moderno (2025-06-08)
- Modificados:
  - `crunevo/templates/feed.html`
  - `crunevo/static/css/custom_feed.css`
- Detalles:
  - Se reorganizó el HTML usando `article.note-card` y un contenedor `.feed-container` para un aspecto de app.
  - Se añadió diseño responsive con `border-radius`, `box-shadow` e íconos centrados.
  - Las miniaturas ahora ocupan todo el ancho superior y el botón principal se centra.
- Pruebas:
  ✅ `pip install -r requirements.txt`
  ✅ `PYTHONPATH=. pytest -q crunevo/tests`

### [Enhancement] Mejoras visuales en el feed móvil (2025-06-08)
- Modificados:
  - `crunevo/templates/feed.html`
  - `crunevo/static/css/custom_feed.css`
- Detalles:
  - Se añadió animación de aparición a las tarjetas con `.animate-fade` y `@keyframes fadeUp`.
  - Se agregó subtítulo informativo, nuevo placeholder y mejoras de accesibilidad con `aria-label`.
  - Botón de subir con mayor padding en móviles.
- Pruebas:
  ✅ `pip install -r requirements.txt`
  ✅ `PYTHONPATH=. pytest -q crunevo/tests`

### [Refactor] Mejorar feed móvil para experiencia inmersiva tipo app (2025-06-08)

- Rediseñado el feed móvil eliminando espacios y ampliando visuales.
- Inspirado en el diseño del feed de Facebook Mobile.
- Archivos modificados:
  - crunevo/templates/feed.html
  - crunevo/static/css/custom_feed.css

### [Feat] Feed móvil inmersivo estilo app (2025-06-08)

- Modificados:
  - `crunevo/templates/base.html`
  - `crunevo/static/css/style.css`
  - `crunevo/templates/feed.html`
  - `crunevo/static/css/custom_feed.css`
  - `crunevo/static/js/main.js`
- Detalles:
  - `.container` y `.feed-container` sin márgenes laterales en móviles.
  - Tarjetas a ancho completo con bordes mínimos y sombra intensa.
  - Barra inferior de acciones con íconos grandes y color activo.
  - Títulos de 1.4rem y descripciones justificadas.
- Pruebas:
  ✅ `pip install -r requirements.txt`
  ✅ `PYTHONPATH=. pytest -q`

### [Fix] Eliminar espacio gris lateral en móviles (2025-06-08)

- Modificados:
  - `crunevo/templates/base.html`
  - `crunevo/static/css/style.css`
- Detalles:
  - Se reemplazó el contenedor principal por `.container-fluid p-0` para quitar padding.
  - Se añadieron reglas globales que eliminan márgenes y padding en móviles para `.container`, `.container-fluid` y `.feed-container`.
- Pruebas:
  ✅ `pip install -r requirements.txt`
  ✅ `PYTHONPATH=. pytest -q crunevo/tests`

### [Fix] Eliminar sombras y bordes de tarjetas en móviles (2025-06-08)

- Modificados:
  - `crunevo/static/css/custom_feed.css`
  - `crunevo/static/css/style.css`
- Detalles:
  - Se eliminaron `border-radius` y `box-shadow` de `.note-card` y `.create-note.card` en móviles.
  - Regla global para `.card` en pantallas pequeñas evita sombras y bordes.
- Pruebas:
  ✅ `black .`
  ❌ `PYTHONPATH=. pytest -q` (faltan dependencias)

### [Enhancement] Acciones interactivas y tarjetas de sugerencia (2025-06-08)

- Modificados:
  - `crunevo/templates/feed.html`
  - `crunevo/static/js/main.js`
  - `crunevo/static/css/custom_feed.css`
- Detalles:
  - Botones de acciones con `data-action` que se activan al tocarlos.
  - Después de cada 3 notas se muestra una tarjeta de recomendación.
  - Se agregó escala en `.btn-primary:active` y sombra en `.note-card`.
- Pruebas:
  ✅ `black .`
  ❌ `pytest -q` (faltan dependencias)

### [Feat] Crear modelo Post y habilitar feed social (2025-06-08)

- Nuevos archivos:
  - `crunevo/models/post.py`
  - `crunevo/tests/test_social_posts.py`
  - `migrations/` con versión inicial `b547bec8a90a_create_post_model.py`
- Modificados:
  - `crunevo/__init__.py` ahora usa Flask-Migrate.
  - `crunevo/routes/main_routes.py`, `feed.html`, `main.js`, `custom_feed.css`.
- Detalles:
  - Los usuarios pueden alternar entre subir apuntes y publicaciones sociales.
  - Se añadió el modelo `Post` con relación a `User` y ruta `/crear_post`.
  - Integrado Flask-Migrate y primer migración automática.
- Pruebas:
  ✅ `black .`
  ✅ `PYTHONPATH=. pytest -q crunevo/tests`
