from flask import Blueprint, request, render_template, redirect, url_for, session
import os
from functools import wraps

auth_bp = Blueprint("auth_bp", __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            # Вместо main_bp.index используем строку: "main_bp.index"
            return redirect(url_for("main_bp.index"))
        return f(*args, **kwargs)
    return decorated

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        if password == os.environ.get("PASSWORD"):
            session["logged_in"] = True
            return redirect(url_for("main_bp.index"))
        else:
            error = "Неверный пароль"
    return render_template("login.html", error=error)

@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("auth_bp.login"))
