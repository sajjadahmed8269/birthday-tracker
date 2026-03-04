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
    # POST Route for index
    if request.method == "POST":
        # Check for session of current user
        if not session.get("user_id"):
            return redirect("/login")

        # Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validate Name
        if not name or not all(c.isalpha() or c.isspace() for c in name):
            return redirect("/")

        # Validate Month and day
        try:
            month = int(month)
        except (ValueError, TypeError):
            return redirect("/")

        if not 1 <= month <= 12:
            return redirect("/")

        try:
            day = int(day)
        except (ValueError, TypeError):
            return redirect("/")

        if not 1 <= day <= 31:
            return redirect("/")

        # Add data to database
        db.execute(
            "INSERT INTO birthdays (user_id, name, month, day) VALUES (?, ?, ?, ?)",
            session["user_id"],
            name,
            month,
            day,
        )

        return redirect("/")

    # GET Route
    else:
        # Check for session of current user
        if not session.get("user_id"):
            return redirect("/login")

        # Display birthdays for current user
        birthdays = db.execute(
            "SELECT * FROM birthdays WHERE user_id = ?", session["user_id"]
        )
        return render_template("index.html", birthdays=birthdays)


# Delete Route
@app.route("/delete", methods=["POST"])
def delete():
    # Check for session of current user
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    id_to_delete = request.form.get("id")

    if id_to_delete:
        db.execute(
            "DELETE FROM birthdays WHERE id = ? AND user_id = ?", id_to_delete, user_id
        )

    return redirect("/")


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
            return render_template(
                "register.html", error="Username already exists."
            ), 409

        if not username or not password or not confirmation:
            return render_template("register.html", error="Empty Credentials."), 400

        if len(username) > 15:
            return render_template(
                "register.html",
                error="Username exceeds 15 characters.",
            ), 400

        if len(password) < 8:
            return render_template(
                "register.html", error="Password should be atleast 8 characters."
            ), 400

        if any(c.isspace() for c in username):
            return render_template(
                "register.html", error="username contain spaces."
            ), 400

        if confirmation != password:
            return render_template(
                "register.html", error="Passwords do not match."
            ), 400

        # Create a hash and add data to database
        hash = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hash
        )

        # Start session for current user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")

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
            return render_template("login.html", error="Empty Credentials."), 400

        if len(username) > 15:
            return render_template(
                "login.html", error="Username exceeds 15 characters."
            ), 400

        if any(c.isspace() for c in username):
            return render_template("login.html", error="username contain spaces."), 400

        # Check database for username and password
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], password
        ):
            return render_template(
                "login.html", error="Invalid username or password."
            ), 401

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
