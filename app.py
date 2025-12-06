from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "expenses.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # so we can use row["column_name"]
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    # Get all expenses, latest-to-oldest by date and created_at
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY date DESC, created_at DESC"
    ).fetchall()

    # Calculate total amount
    total = conn.execute("SELECT SUM(amount) AS total FROM expenses").fetchone()["total"]
    conn.close()

    if total is None:
        total = 0

    return render_template("index.html", expenses=expenses, total=total)


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount", "").strip()
    category = request.form.get("category", "").strip()
    date = request.form.get("date", "").strip()

    if not title or not amount:
        return redirect(url_for("index"))

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    try:
        amount_value = float(amount)
    except ValueError:
        return redirect(url_for("index"))

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (title, amount, category, date, created_at) VALUES (?, ?, ?, ?, ?)",
        (title, amount_value, category, date, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
