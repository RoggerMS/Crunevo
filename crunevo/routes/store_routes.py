# routes/store_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from flask_login import login_required
from crunevo.models.product import Product

store_bp = Blueprint('store', __name__, url_prefix='/tienda')

@store_bp.route('/')
def tienda():
    query = Product.query
    search = request.args.get('search', '')
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    available = request.args.get('available')

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Product.type == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if available:
        query = query.filter(Product.availability.is_(True))

    productos = query.order_by(Product.created_at.desc()).all()
    return render_template(
        'tienda/store.html',
        productos=productos,
        search=search,
        category=category,
        min_price=min_price,
        max_price=max_price,
        available=bool(available),
    )

@store_bp.route('/<int:id>')
def producto(id):
    producto = Product.query.get_or_404(id)
    return render_template('tienda/producto.html', producto=producto)

@store_bp.route('/carrito')
@login_required
def carrito():
    carrito = session.get('carrito', [])
    return render_template('tienda/carrito.html', carrito=carrito)

@store_bp.route('/carrito/eliminar/<int:producto_id>')
@login_required
def remove_from_cart(producto_id):
    carrito = session.get('carrito', [])
    carrito = [p for p in carrito if p['id'] != producto_id]
    session['carrito'] = carrito
    flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('store.carrito'))

