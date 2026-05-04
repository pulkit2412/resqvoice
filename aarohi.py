from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "sos_app.db"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            name TEXT,
            phone TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS sos_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

# -------- AUTH --------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (data["email"], data["password"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Registered successfully"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )

    user = c.fetchone()
    conn.close()

    return jsonify({"success": bool(user)})

# -------- CONTACTS --------
@app.route("/add_contact", methods=["POST"])
def add_contact():
    data = request.json

    user = data["user"].strip()

    conn = get_db()
    c = conn.cursor()

    c.execute(
        "INSERT INTO contacts (user, name, phone) VALUES (?, ?, ?)",
        (user, data["name"], data["phone"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Contact added"})


@app.route("/get_contacts/<user>")
def get_contacts(user):
    user = user.strip()

    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT name, phone FROM contacts WHERE user=?",
        (user,)
    )

    rows = c.fetchall()
    conn.close()

    contacts = [{"name": r[0], "phone": r[1]} for r in rows]

    return jsonify(contacts)

# -------- SOS (NO TWILIO, ONLY DATA RETURN) --------
@app.route("/sos", methods=["POST"])
def sos():
    data = request.json

    user = data["user"].strip()
    lat = data["latitude"]
    lon = data["longitude"]

    conn = get_db()
    c = conn.cursor()

    # Save SOS
    c.execute(
        "INSERT INTO sos_alerts (user, latitude, longitude) VALUES (?, ?, ?)",
        (user, lat, lon)
    )

    # Get contacts
    c.execute(
        "SELECT name, phone FROM contacts WHERE user=?",
        (user,)
    )

    contacts = c.fetchall()

    conn.commit()
    conn.close()

    return jsonify({
        "contacts": contacts,
        "latitude": lat,
        "longitude": lon
    })

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
