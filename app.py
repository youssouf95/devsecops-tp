from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Initialiser une base SQLite simple
def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'password')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Hello from DevSecOps demo app!"

# Route VULNÉRABLE à l'injection SQL (pour CodeQL)
@app.route('/login')
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # VULNÉRABILITÉ : Requête SQL non sécurisée
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return f"Login successful for user: {result[1]}"
    else:
        return "Invalid credentials"

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
