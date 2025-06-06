from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from ..models import db
from ..models.user import User
from ..models.note import Note, Report
from ..models.product import Product

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Función auxiliar para manejar commits
def commit_changes():
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
        return False

# Decorador para verificar permisos de administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_role") != "admin":
            flash("Acceso no autorizado.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "total_users": User.query.count(),
        "total_notes": Note.query.count(),
        "total_products": Product.query.count(),
        "pending_reports": Report.query.filter_by(status="pending").count()
    }
    return render_template("admin/dashboard.html", stats=stats)

@admin_bp.route("/users")
@admin_required
def manage_users():
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("admin/manage_users.html", users=users)

@admin_bp.route("/users/<int:user_id>/toggle_ban")
@admin_required
def toggle_user_ban(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "admin":
        user.is_banned = not user.is_banned
        if commit_changes():
            status = "baneado" if user.is_banned else "desbaneado"
            flash(f"Usuario {status} exitosamente.", "success")
    else:
        flash("No se puede modificar el estado de un administrador.", "danger")
    return redirect(url_for("admin.manage_users"))

@admin_bp.route("/reports")
@admin_required
def manage_reports():
    page = request.args.get("page", 1, type=int)
    reports = Report.query.order_by(Report.report_date.desc()).paginate(page=page, per_page=10)
    return render_template("admin/manage_reports.html", reports=reports)

@admin_bp.route("/reports/<int:report_id>/update_status", methods=["POST"])
@admin_required
def update_report_status(report_id):
    report = Report.query.get_or_404(report_id)
    new_status = request.form.get("status")
    if new_status in ["pending", "reviewed", "resolved"]:
        report.status = new_status
        if new_status == "resolved":
            flash("Reporte resuelto.", "info")
        if commit_changes():
            flash(f"Estado del reporte actualizado a {new_status}.", "success")
    else:
        flash("Estado no válido.", "warning")
    return redirect(url_for("admin.manage_reports"))

@admin_bp.route("/store")
@admin_required
def manage_store():
    page = request.args.get("page", 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("admin/manage_store.html", products=products)

@admin_bp.route("/store/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        type = request.form.get("type")
        availability = request.form.get("availability") == "on"
        image_url = "/static/images/product_placeholder.png"

        if not all([name, price, type]):
            flash("Nombre, precio y tipo son requeridos.", "danger")
            return render_template("admin/add_edit_product.html", form_data=request.form, action="add")

        new_product = Product(
            name=name,
            description=description,
            price=price,
            type=type,
            availability=availability,
            image_url=image_url
        )
        db.session.add(new_product)
        if commit_changes():
            flash("Producto añadido exitosamente.", "success")
            return redirect(url_for("admin.manage_store"))

    return render_template("admin/add_edit_product.html", action="add")

@admin_bp.route("/store/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        product.name = request.form.get("name", product.name)
        product.description = request.form.get("description", product.description)
        product.price = request.form.get("price", product.price)
        product.type = request.form.get("type", product.type)
        product.availability = request.form.get("availability") == "on"

        if commit_changes():
            flash("Producto actualizado exitosamente.", "success")
            return redirect(url_for("admin.manage_store"))

    return render_template("admin/add_edit_product.html", action="edit", product=product)

@admin_bp.route("/store/delete/<int:product_id>", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    if commit_changes():
        flash("Producto eliminado exitosamente.", "success")
    return redirect(url_for("admin.manage_store"))