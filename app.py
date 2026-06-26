import os

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "simple-ui-flask-secret"

VALID_CREDENTIALS = {"admin": "flask123"}
LOG_ENTRIES = [
    {"time": "2026-06-26 09:15", "level": "INFO", "message": "Application started successfully."},
    {"time": "2026-06-26 09:18", "level": "INFO", "message": "User admin signed in."},
    {"time": "2026-06-26 09:22", "level": "WARNING", "message": "Disk usage is above 80%."},
    {"time": "2026-06-26 09:30", "level": "ERROR", "message": "Connection retry failed for service B."},
]


@app.route("/")
def index():
    if session.get("logged_in"):
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if VALID_CREDENTIALS.get(username) == password:
            session["logged_in"] = True
            session["username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("home"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("home.html", username=session.get("username", "User"))


@app.route("/logs")
def logs():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("logs.html", entries=LOG_ENTRIES)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
