from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, flash, redirect, render_template_string, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / os.environ.get("USERS_FILE", "users.csv")
ATTEMPTS_FILE = BASE_DIR / os.environ.get("ATTEMPTS_FILE", "attempts.csv")


def ensure_storage_files() -> None:
    """Create the CSV files if they do not exist."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not USERS_FILE.exists():
        with USERS_FILE.open("w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["username", "password_hash", "is_admin"])
            writer.writeheader()

    if not ATTEMPTS_FILE.exists():
        with ATTEMPTS_FILE.open("w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=["timestamp", "username", "reading_type", "total_score", "reading_score", "verbal_score", "math_score"],
            )
            writer.writeheader()


ensure_storage_files()


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def write_csv_rows(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    with path.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def init_storage() -> None:
    """Backward-compatible helper name for older code and imports."""
    ensure_storage_files()


def verify_user(username: str, password: str) -> bool:
    if not username or not password:
        return False
    for row in read_csv_rows(USERS_FILE):
        if row.get("username") == username:
            stored_hash = row.get("password_hash", "")
            return check_password_hash(stored_hash, password)
    return False


def is_admin(username: str) -> bool:
    for row in read_csv_rows(USERS_FILE):
        if row.get("username") == username:
            return row.get("is_admin", "False").strip().lower() == "true"
    return False


def create_user(username: str, password: str, is_admin: bool = False) -> bool:
    username = (username or "").strip()
    password = password or ""
    if not username or not password:
        return False

    rows = read_csv_rows(USERS_FILE)
    for row in rows:
        if row.get("username") == username:
            return False

    rows.append(
        {
            "username": username,
            "password_hash": generate_password_hash(password),
            "is_admin": "True" if is_admin else "False",
        }
    )
    write_csv_rows(USERS_FILE, rows, ["username", "password_hash", "is_admin"])
    return True


def delete_user(username: str) -> bool:
    username = (username or "").strip()
    if not username or username.lower() == "admin":
        return False

    rows = read_csv_rows(USERS_FILE)
    filtered = [row for row in rows if row.get("username") != username]
    if len(filtered) == len(rows):
        return False

    write_csv_rows(USERS_FILE, filtered, ["username", "password_hash", "is_admin"])
    return True


def get_all_users() -> List[Dict[str, object]]:
    rows = read_csv_rows(USERS_FILE)
    users = []
    for row in rows:
        users.append(
            {
                "username": row.get("username", ""),
                "is_admin": row.get("is_admin", "False").strip().lower() == "true",
            }
        )
    return users


def save_user_attempt(username: str, reading_type: str, total_score: float, reading_score: float, verbal_score: float, math_score: float) -> None:
    rows = read_csv_rows(ATTEMPTS_FILE)
    rows.append(
        {
            "timestamp": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "reading_type": reading_type,
            "total_score": str(total_score),
            "reading_score": str(reading_score),
            "verbal_score": str(verbal_score),
            "math_score": str(math_score),
        }
    )
    write_csv_rows(
        ATTEMPTS_FILE,
        rows,
        ["timestamp", "username", "reading_type", "total_score", "reading_score", "verbal_score", "math_score"],
    )


def get_user_attempts(username: str) -> List[Dict[str, str]]:
    rows = read_csv_rows(ATTEMPTS_FILE)
    return [row for row in rows if row.get("username") == username]


def reset_user_data(username: str) -> bool:
    username = (username or "").strip()
    if not username:
        return False

    rows = read_csv_rows(ATTEMPTS_FILE)
    filtered = [row for row in rows if row.get("username") != username]
    write_csv_rows(
        ATTEMPTS_FILE,
        filtered,
        ["timestamp", "username", "reading_type", "total_score", "reading_score", "verbal_score", "math_score"],
    )
    return True


def login_required(view):
    def wrapped(*args, **kwargs):
        if "username" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


def admin_required(view):
    def wrapped(*args, **kwargs):
        if "username" not in session or not is_admin(session["username"]):
            flash("Admin access required.")
            return redirect(url_for("home"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>SSAT Study App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6fb; color: #1d2736; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 14px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
        .nav { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
        a { color: #1f5eff; text-decoration: none; }
        form { display: grid; gap: 10px; max-width: 420px; }
        input, button, select { padding: 10px; font-size: 1rem; border-radius: 8px; border: 1px solid #d9dce2; }
        button { background: #1f5eff; color: #fff; border: none; cursor: pointer; }
        .flash { background: #fff4d6; padding: 10px; border-radius: 8px; margin-bottom: 12px; }
        table { width: 100%; border-collapse: collapse; margin-top: 16px; }
        th, td { padding: 10px; border-bottom: 1px solid #ebedf1; text-align: left; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('generate') }}">Generate</a>
            <a href="{{ url_for('data') }}">Data</a>
            {% if session.get('username') %}
                <a href="{{ url_for('logout') }}">Logout</a>
            {% else %}
                <a href="{{ url_for('login') }}">Login</a>
            {% endif %}
        </div>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="flash">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {{ content | safe }}
    </div>
</body>
</html>
"""


def render_page(content: str):
    return render_template_string(PAGE_TEMPLATE, content=content)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        action = request.form.get("action", "login")

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("login"))

        if action == "register":
            created = create_user(username, password, is_admin=False)
            if not created:
                flash("That username already exists or is invalid.")
                return redirect(url_for("login"))
            flash("Account created. You can log in now.")
            return redirect(url_for("login"))

        if verify_user(username, password):
            session["username"] = username
            session["is_admin"] = is_admin(username)
            flash("Logged in successfully.")
            return redirect(url_for("home"))

        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_page("""
        <h1>SSAT Study App</h1>
        <p>Log in to continue or create a new account.</p>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" name="action" value="login">Login</button>
            <button type="submit" name="action" value="register">Create Account</button>
        </form>
    """)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/")
def home():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    user_attempts = get_user_attempts(username)
    attempts_html = "<h2>Recent attempt history</h2>"
    if not user_attempts:
        attempts_html += "<p>No attempts recorded yet.</p>"
    else:
        attempts_html += """
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Type</th>
                        <th>Total</th>
                        <th>Reading</th>
                        <th>Verbal</th>
                        <th>Math</th>
                    </tr>
                </thead>
                <tbody>
        """
        for row in user_attempts[-10:]:
            attempts_html += f"""
                <tr>
                    <td>{row.get('timestamp', '')}</td>
                    <td>{row.get('reading_type', '')}</td>
                    <td>{row.get('total_score', '')}</td>
                    <td>{row.get('reading_score', '')}</td>
                    <td>{row.get('verbal_score', '')}</td>
                    <td>{row.get('math_score', '')}</td>
                </tr>
            """
        attempts_html += "</tbody></table>"

    content = f"""
        <h1>Welcome, {username}</h1>
        <p>This app is ready to run on Render and uses a CSV file for simple account storage.</p>
        <p><a href="{url_for('generate')}">Generate a practice set</a></p>
        {attempts_html}
    """
    return render_page(content)


@app.route("/generate")
@login_required
def generate():
    sample = {
        "question": "Which word is closest in meaning to 'diligent'?",
        "choices": ["careless", "hardworking", "confused", "lazy"],
        "answer": "hardworking",
        "explanation": "Diligent means showing steady, careful effort.",
    }

    content = f"""
        <h1>Practice Problem</h1>
        <p><strong>{sample['question']}</strong></p>
        <ol>
            {''.join(f'<li>{choice}</li>' for choice in sample['choices'])}
        </ol>
        <p><strong>Answer:</strong> {sample['answer']}</p>
        <p><strong>Explanation:</strong> {sample['explanation']}</p>
    """
    return render_page(content)


@app.route("/data")
@login_required
def data():
    if not is_admin(session.get("username", "")):
        flash("You do not have admin access.")
        return redirect(url_for("home"))

    users = get_all_users()
    rows = ""
    if not users:
        rows = "<p>No users found.</p>"
    else:
        rows = """
            <table>
                <thead><tr><th>Username</th><th>Admin</th></tr></thead>
                <tbody>
        """
        for user in users:
            rows += f"<tr><td>{user['username']}</td><td>{'Yes' if user['is_admin'] else 'No'}</td></tr>"
        rows += "</tbody></table>"

    content = f"""
        <h1>Data</h1>
        {rows}
    """
    return render_page(content)


@app.route("/admin/reset-user", methods=["POST"])
@login_required
@admin_required
def reset_user():
    username = request.form.get("username", "").strip()
    if username:
        reset_user_data(username)
        flash(f"Cleared attempts for {username}.")
    return redirect(url_for("data"))


@app.before_request
def ensure_files_exist():
    ensure_storage_files()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
