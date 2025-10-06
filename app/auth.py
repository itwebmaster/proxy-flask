from flask import Blueprint, render_template, request, redirect, url_for, session
import os

auth_bp = Blueprint("auth", __name__)

PASSWORD = os.environ.get("PASSWORD")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("main.index"))
        else:
            return render_template("login.html", error="Неверный пароль")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

def login_required(f):
    from functools import wraps
    from flask import redirect, url_for, session
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
