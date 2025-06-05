# routes/store_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required
from models.product import Product  # ✅ CORREGIDO: usamos 'Product'
from app import db

store_bp = Blueprint('store', __name__, url_prefix='/tienda')

@store_bp.route('/')
def tienda():
    productos = Product.query.all()
    return render_template('tienda/store.html', productos=productos)

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
