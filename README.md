# 🎂 Birthday Tracker

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-lightgrey?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Deployed-Render-blueviolet?style=flat-square)

A full-stack web app to track and manage friends' birthdays — with secure auth, per-user data isolation, and a clean dark UI.

🔗 **[Live Demo](https://sajjadahmed8269.pythonanywhere.com)**

> ⚠️ **Heads-up for demo viewers:**
>
> - The app is hosted on PythonAnywhere's free tier — no cold starts, it responds instantly.
> - Data is stored in **SQLite**. The database persists across restarts but may be lost if the app is redeployed from scratch.

---

## Features

- **Auth from scratch** — Secure registration & login using PBKDF2 password hashing (no auth libraries)
- **Per-user isolation** — Foreign key relationships scope all data strictly to the logged-in user
- **Full CRUD** — Add and delete birthdays with server-side validation
- **Persistent sessions** — Stay logged in across browser restarts
- **Responsive dark UI** — Mobile-friendly navbar with dropdown, self-hosted fonts (fully offline-capable)

## Tech Stack

| Layer    | Technology                    |
| -------- | ----------------------------- |
| Backend  | Python, Flask, Werkzeug       |
| Database | SQLite                        |
| Frontend | HTML, CSS (custom dark theme) |
| Config   | python-dotenv                 |

## Getting Started

```bash
git clone https://github.com/sajjad-thedev/birthday-tracker.git
cd birthday-tracker

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

echo "SECRET_KEY=your-secret-key" > .env

sqlite3 birthdays.db < schema.sql

flask run
```

Replace 'your-secret-key' with a strong random string.
Then open [http://localhost:5000](http://localhost:5000).

## Project Structure

```
birthday-tracker/
├── app.py
├── templates/
├── static/
├── requirements.txt
└── .env.example
```

## What I Learned

- Implementing authentication without third-party libraries — understanding what frameworks abstract away
- Why server-side validation is the real security boundary, not the client
- Scoping database queries by user via foreign keys to enforce data isolation
- Managing environment variables and secrets across local and production environments
- Deploying a Python/Flask app to a cloud platform (Render)

---

> Built by [Sajjad](https://github.com/sajjad-thedev)
