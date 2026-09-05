"""
TSB 1Ç26 Dashboard - Flask giriş ekranı
----------------------------------------
Basit, session tabanlı bir giriş sistemi. Dashboard sayfasını (templates/dashboard.html)
giriş yapmamış kullanıcılardan korur.

Çalıştırmak için:
    pip install -r requirements.txt
    python app.py
Sonra tarayıcıda http://127.0.0.1:5000 adresini açın.

Varsayılan giriş bilgileri (mutlaka değiştirin):
    kullanıcı adı: admin
    şifre:         changeme123
"""

import os
from datetime import timedelta
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Prod ortamında bunu mutlaka bir ortam değişkeninden okuyun, kodun içine yazmayın.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-secret-key")
# "Beni hatırla" işaretlenirse session bu süre boyunca kalıcı olur.
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=14)

# --- Basit kullanıcı deposu -------------------------------------------------
# Gerçek bir projede bunun yerine bir veritabanı (ör. SQLAlchemy + bir users
# tablosu) kullanın. Burada tek amaç, dashboard'u parola ile korumak.
USERS = {
    "admin": generate_password_hash(os.environ.get("ADMIN_PASSWORD", "changeme123")),
}


def login_required(view):
    """Session'da giriş yapmış bir kullanıcı yoksa /login sayfasına yönlendirir."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        stored_hash = USERS.get(username)
        if stored_hash and check_password_hash(stored_hash, password):
            session.clear()
            session["user"] = username
            if request.form.get("remember"):
                session.permanent = True
            next_url = request.args.get("next") or url_for("dashboard")
            return redirect(next_url)

        flash("Kullanıcı adı veya şifre hatalı.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=session.get("user"))


if __name__ == "__main__":
    # Yerelde çalıştırırken debug=True kalabilir; gerçek deploy'da bu dosya
    # değil, gunicorn (Procfile / requirements.txt) devreye girer.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
