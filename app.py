from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------------
# Initialize the SQLite database
# -----------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.close()

# -----------------------------
# Home route: Display all expenses
# -----------------------------
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    data = cursor.fetchall()
    total = sum([row[2] for row in data])
    conn.close()
    return render_template('index.html', expenses=data, total=total)

# -----------------------------
# Add new expense
# -----------------------------
@app.route('/add', methods=['POST'])
def add():
    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    date = request.form.get('date')

    conn = sqlite3.connect('database.db')
    conn.execute(
        'INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)',
        (description, amount, date)
    )
    conn.commit()
    conn.close()
    return redirect('/')

# -----------------------------
# Delete an expense by ID
# -----------------------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# -----------------------------
# Run the Flask App
# -----------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
