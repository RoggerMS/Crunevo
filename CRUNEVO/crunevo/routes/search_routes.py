# src/routes/search_routes.py
from flask import Blueprint, request, jsonify, render_template # Added render_template
from sqlalchemy import or_

from src.models import db
from src.models.note import Note
from src.models.product import Product

search_bp = Blueprint("search", __name__)

@search_bp.route("/api/search", methods=["GET"])
def global_search_api(): # Renamed to avoid conflict
    query = request.args.get("q", "")
    limit = request.args.get("limit", default=5, type=int)

    results = {
        "apuntes": [],
        "tienda": [],
        "temas_sugeridos": []
    }

    if not query:
        return jsonify(results)

    apuntes_filters = [
        Note.title.ilike(f"%{query}%"),
        Note.description.ilike(f"%{query}%"),
        Note.course.ilike(f"%{query}%"),
        Note.faculty.ilike(f"%{query}%"),
        Note.tags.ilike(f"%{query}%")
    ]
    apuntes_query = Note.query.filter(or_(*apuntes_filters)).limit(limit).all()
    for apunte in apuntes_query:
        results["apuntes"].append({
            "id": apunte.id,
            "title": apunte.title,
            "description_snippet": (apunte.description[:100] + "..." if apunte.description and len(apunte.description) > 100 else apunte.description),
            "course": apunte.course,
            "faculty": apunte.faculty,
            "tags": apunte.tags,
            "file_type": apunte.file_type,
            "url": f"/notes/{apunte.id}"
        })

    productos_query = Product.query.filter(
        or_(
            Product.name.ilike(f"%{query}%"),
            Product.type.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%")
        )
    ).limit(limit).all()
    for producto in productos_query:
        results["tienda"].append({
            "id": producto.id,
            "name": producto.name,
            "price": producto.price,
            "image_url": producto.image_url,
            "type": producto.type,
            "url": f"/store/product/{producto.id}"
        })

    if query.lower() == "álgebra":
        results["temas_sugeridos"].extend([
            {"text": "Facultad de Ciencias", "type": "filter", "filter_type": "faculty"},
            {"text": "Resúmenes de Álgebra", "type": "filter", "filter_type": "note_type"}
        ])
    elif query.lower() == "derecho":
        results["temas_sugeridos"].extend([
            {"text": "Facultad de Derecho", "type": "filter", "filter_type": "faculty"},
            {"text": "Derecho Penal", "type": "filter", "filter_type": "course"}
        ])

    return jsonify(results)

@search_bp.route("/search_results", methods=["GET"])
def search_results_page():
    query = request.args.get("q", "")
    category = request.args.get("category", "all") # 'all', 'apuntes', 'tienda'
    page = request.args.get("page", 1, type=int)
    per_page = 10 # Number of items per page

    # For now, this is a placeholder page. 
    # A full implementation would fetch paginated results based on query and category.
    # We will simulate some data or just show the query term.
    
    # Simulate fetching more data based on the query for demonstration
    # In a real app, you'd query the database here with pagination
    simulated_apuntes = []
    simulated_productos = []

    if query: # Only simulate if there's a query
        if category == "apuntes" or category == "all":
            # Simulate more apuntes results
            for i in range(per_page):
                simulated_apuntes.append({
                    "id": 100 + i,
                    "title": f"Apunte de {query} - Resultado Completo {i+1}",
                    "description_snippet": "Descripción extendida del apunte de prueba para la página de resultados completos.",
                    "course": "Curso Ejemplo",
                    "faculty": "Facultad Ejemplo",
                    "file_type": "pdf",
                    "url": f"/notes/{100+i}"
                })
        
        if category == "tienda" or category == "all":
            # Simulate more tienda results
            for i in range(per_page):
                simulated_productos.append({
                    "id": 200 + i,
                    "name": f"Producto de {query} - Resultado Completo {i+1}",
                    "price": 19.99 + i,
                    "image_url": "/static/images/default_product.png", # Placeholder image
                    "type": "Tipo Ejemplo",
                    "url": f"/store/product/{200+i}"
                })

    return render_template("search_results.html", 
                           query=query, 
                           category=category,
                           apuntes=simulated_apuntes, 
                           productos=simulated_productos,
                           page=page,
                           per_page=per_page,
                           # For a real app, you'd pass total_pages or has_next/has_prev for pagination controls
                           total_apuntes=len(simulated_apuntes), # This would be total count from DB
                           total_productos=len(simulated_productos) # This would be total count from DB
                           )

