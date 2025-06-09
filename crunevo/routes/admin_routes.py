from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
import os
from crunevo.utils.storage import save_file_local
from functools import wraps
from flask_login import login_required, current_user
from crunevo.models import db
from crunevo.models.user import User
from crunevo.models.note import Note, Report
from crunevo.models.product import Product
from crunevo.models.log import LoginLog

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def log_admin_access():
    if current_user.is_authenticated:
        current_app.logger.info(
            "Admin access user=%s ip=%s ua=%s",
            current_user.id,
            request.remote_addr,
            request.user_agent.string,
        )


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash("Acceso no autorizado.", "danger")
                return redirect(url_for("main.index"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


admin_required = roles_required("admin")


# Función auxiliar para manejar commits
def commit_changes():
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
        return False


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "total_users": User.query.count(),
        "active_users": User.query.filter_by(is_banned=False).count(),
        "inactive_users": User.query.filter_by(is_banned=True).count(),
        "total_notes": Note.query.count(),
        "total_products": Product.query.count(),
        "pending_reports": Report.query.filter_by(status="pending").count(),
        "top_downloads": Note.query.order_by(Note.downloads_count.desc())
        .limit(5)
        .all(),
        "dates": [],
        "user_growth": [],
        "note_growth": [],
        "last_updated": "",
    }
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route("/users")
@admin_required
def manage_users():
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("admin/manage_users.html", users=users)


@admin_bp.route("/notes")
@roles_required("admin", "moderator")
def manage_notes():
    page = request.args.get("page", 1, type=int)
    query = Note.query
    title = request.args.get("title")
    user = request.args.get("user")
    if title:
        query = query.filter(Note.title.ilike(f"%{title}%"))
    if user:
        query = query.join(User).filter(User.username.ilike(f"%{user}%"))
    notes = query.order_by(Note.upload_date.desc()).paginate(page=page, per_page=10)
    return render_template(
        "admin/manage_notes.html", notes=notes, search_title=title, search_user=user
    )


@admin_bp.route("/notes/delete/<int:note_id>", methods=["POST"])
@admin_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    if commit_changes():
        flash("Apunte eliminado exitosamente.", "success")
    return redirect(url_for("admin.manage_notes"))


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


@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@admin_required
def change_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get("role")
    if new_role in {"admin", "moderator", "editor", "user"}:
        user.role = new_role
        if commit_changes():
            flash("Rol actualizado", "success")
    else:
        flash("Rol inválido", "danger")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/reports")
@roles_required("admin", "moderator")
def manage_reports():
    page = request.args.get("page", 1, type=int)
    reports = Report.query.order_by(Report.report_date.desc()).paginate(
        page=page, per_page=10
    )
    return render_template("admin/manage_reports.html", reports=reports)


@admin_bp.route("/reports/<int:report_id>/update_status", methods=["POST"])
@roles_required("admin", "moderator")
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
@roles_required("admin", "editor")
def manage_store():
    page = request.args.get("page", 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=10
    )
    return render_template("admin/manage_store.html", products=products)


@admin_bp.route("/store/add", methods=["GET", "POST"])
@roles_required("admin", "editor")
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        type = request.form.get("type")
        stock = request.form.get("stock", type=int)
        availability = request.form.get("availability") == "on"
        featured = request.form.get("featured") == "on"
        image = request.files.get("image")
        image_url = "/static/images/product_placeholder.png"
        if image and image.filename:
            upload_folder = os.path.join(
                current_app.static_folder, "uploads", "products"
            )
            os.makedirs(upload_folder, exist_ok=True)
            saved = save_file_local(image, upload_folder)
            if saved:
                image_url = saved

        if not all([name, price, type]):
            flash("Nombre, precio y tipo son requeridos.", "danger")
            return render_template(
                "admin/add_edit_product.html", form_data=request.form, action="add"
            )

        new_product = Product(
            name=name,
            description=description,
            price=price,
            type=type,
            availability=availability,
            stock=stock or 0,
            featured=featured,
            image_url=image_url,
        )
        db.session.add(new_product)
        if commit_changes():
            flash("Producto añadido exitosamente.", "success")
            return redirect(url_for("admin.manage_store"))

    return render_template("admin/add_edit_product.html", action="add")


@admin_bp.route("/store/edit/<int:product_id>", methods=["GET", "POST"])
@roles_required("admin", "editor")
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        product.name = request.form.get("name", product.name)
        product.description = request.form.get("description", product.description)
        product.price = request.form.get("price", product.price)
        product.type = request.form.get("type", product.type)
        product.stock = request.form.get("stock", product.stock, type=int)
        product.availability = request.form.get("availability") == "on"
        product.featured = request.form.get("featured") == "on"
        image = request.files.get("image")
        if image and image.filename:
            upload_folder = os.path.join(
                current_app.static_folder, "uploads", "products"
            )
            os.makedirs(upload_folder, exist_ok=True)
            saved = save_file_local(image, upload_folder)
            if saved:
                product.image_url = saved

        if commit_changes():
            flash("Producto actualizado exitosamente.", "success")
            return redirect(url_for("admin.manage_store"))

    return render_template(
        "admin/add_edit_product.html", action="edit", product=product
    )


@admin_bp.route("/store/delete/<int:product_id>", methods=["POST"])
@roles_required("admin", "editor")
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    if commit_changes():
        flash("Producto eliminado exitosamente.", "success")
    return redirect(url_for("admin.manage_store"))


@admin_bp.route("/store/toggle/<int:product_id>", methods=["POST"])
@roles_required("admin", "editor")
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.availability = not product.availability
    if commit_changes():
        flash("Disponibilidad actualizada", "success")
    return redirect(url_for("admin.manage_store"))


@admin_bp.route("/credits", methods=["GET"])
@roles_required("admin")
def manage_credits():
    users = User.query.order_by(User.username.asc()).all()
    return render_template("admin/manage_credits.html", users=users)


@admin_bp.route("/credits/<int:user_id>", methods=["POST"])
@roles_required("admin")
def adjust_credits(user_id):
    user = User.query.get_or_404(user_id)
    amount = request.form.get("amount", type=int)
    if amount is not None:
        user.credits = (user.credits or 0) + amount
        if commit_changes():
            flash("Créditos actualizados.", "success")
    else:
        flash("Cantidad inválida.", "danger")
    return redirect(url_for("admin.manage_credits"))


@admin_bp.route("/security/logs")
@admin_required
def security_logs():
    page = request.args.get("page", 1, type=int)
    logs = LoginLog.query.order_by(LoginLog.timestamp.desc()).paginate(
        page=page, per_page=20
    )
    return render_template("admin/security_logs.html", logs=logs)


# Temporary route to promote a specific user to admin.
# NOTE: This route is intended for one-time use and does not require
# authentication. It can be removed after promoting the desired user.
@admin_bp.route("/promote-temp", methods=["GET"])
def promote_temp():
    from crunevo.models.user import User  # Local import to avoid circular deps
    from crunevo import db

    email = "leibicastell@gmail.com"
    user = User.query.filter_by(email=email).first()

    if user:
        user.role = "admin"
        db.session.commit()
        return "Usuario promovido a admin exitosamente."
    else:
        return "Usuario no encontrado.", 404
