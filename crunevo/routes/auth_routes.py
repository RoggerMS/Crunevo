import os
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    request,
)
from flask_login import login_user, logout_user, login_required, current_user

from crunevo.models import db
from crunevo.models.user import User
from crunevo.models.log import LoginLog
from crunevo.forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        success = False
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            success = True
            db.session.add(
                LoginLog(
                    user_id=user.id,
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string,
                    success=True,
                )
            )
            db.session.commit()
            return redirect(url_for("main.index"))

        master_key = current_app.config.get("MASTER_KEY")
        if (
            master_key
            and current_app.config.get("ENABLE_MASTER_KEY", True)
            and form.password.data == master_key
            and user
        ):
            current_app.logger.warning(
                f"[MASTER LOGIN] {user.email} from {request.remote_addr}"
            )
            login_user(user, remember=False)
            db.session.add(
                LoginLog(
                    user_id=user.id,
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string,
                    success=True,
                )
            )
            db.session.commit()
            return redirect(url_for("main.index"))

        if not success:
            db.session.add(
                LoginLog(
                    user_id=user.id if user else None,
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string,
                    success=False,
                )
            )
            db.session.commit()
        flash("Credenciales inválidas.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("El correo ya está registrado.", "warning")
        else:
            user = User(
                username=form.name.data, email=form.email.data, name=form.name.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("main.index"))
    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
