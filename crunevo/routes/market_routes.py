from flask import Blueprint, render_template
from crunevo.models.product import Product

market_bp = Blueprint('market', __name__, url_prefix='/marketplace')

@market_bp.route('/')
def market_home():
    # Retrieve all products without filtering by an "aprobado" field, since
    # that attribute does not exist in the Product model.
    productos = Product.query.all()
    return render_template('marketplace/market.html', productos=productos)

@market_bp.route('/producto/<int:id>')
def ver_producto(id):
    producto = Product.query.get_or_404(id)
    return render_template('marketplace/producto.html', producto=producto)
