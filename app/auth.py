from flask import Blueprint, request, render_template, redirect, url_for, session
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        # Берём пароль из .env
        if password == os.environ.get("PASSWORD"):
            session["logged_in"] = True
            return redirect(url_for("main_bp.index"))
        else:
            error = "Неверный пароль"
    return render_template("login.html", error=error)
