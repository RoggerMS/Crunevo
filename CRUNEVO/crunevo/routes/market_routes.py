from flask import Blueprint, render_template, request
from models.product import Product

market_bp = Blueprint('market', __name__, url_prefix='/marketplace')

@market_bp.route('/')
def market_home():
    productos = Product.query.filter_by(aprobado=True).all()
    return render_template('marketplace/market.html', productos=productos)

@market_bp.route('/producto/<int:id>')
def ver_producto(id):
    producto = Product.query.get_or_404(id)
    return render_template('marketplace/producto.html', producto=producto)
