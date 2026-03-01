import os

from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Configure application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Index Route
@app.route("/", methods=["GET", "POST"])
def index():
    return "Birthday Tracker — coming soon"


# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Validate the data and add the user to database
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Data Validation
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return render_template("register.html", error="Username already exists.")

        if not username or not password or not confirmation:
            return render_template("register.html", error="Empty Credentials.")

        if len(username) > 15:
            return render_template(
                "register.html", error="Username exceeds 15 characters."
            )

        if len(password) < 8:
            return render_template(
                "register.html", error="Password should be atleast 8 characters."
            )

        if any(c.isspace() for c in username):
            return render_template("register.html", error="username contain spaces.")

        if confirmation != password:
            return render_template("register.html", error="Passwords do not match.")

        # Create a hash and add data to database
        hash = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hash
        )

        return redirect("/login")

    else:
        return render_template("register.html")


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Data Validation
        if not username or not password:
            return render_template("login.html", error="Empty Credentials.")

        if len(username) > 15:
            return render_template(
                "login.html", error="Username exceeds 15 characters."
            )

        if any(c.isspace() for c in username):
            return render_template("login.html", error="username contain spaces.")

        # Check database for username and password
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], password
        ):
            return render_template("login.html", error="Invalid username or password.")

        # Start session for current user
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")

    else:
        return render_template("login.html")


# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
