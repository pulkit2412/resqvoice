from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# -------- DATABASE --------
def get_db():
    return sqlite3.connect('database.db')

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS sos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude TEXT,
        longitude TEXT
    )''')

    conn.commit()
    conn.close()

init_db()

# -------- ROUTES --------
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
              (data['email'], data['password']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (data['email'], data['password']))
    user = c.fetchone()

    conn.close()

    return jsonify({"success": bool(user)})

@app.route('/sos', methods=['POST'])
def sos():
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO sos (latitude, longitude) VALUES (?, ?)",
              (data['latitude'], data['longitude']))

    conn.commit()
    conn.close()

    print("🚨 SOS RECEIVED:", data)

    return jsonify({"message": "SOS stored successfully"})


if __name__ == '__main__':
    app.run(debug=True)