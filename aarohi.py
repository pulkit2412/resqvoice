from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

# -------------------- CONFIG --------------------
DB_NAME = "sos_app.db"

# 🔴 PUT YOUR TWILIO DETAILS HERE
ACCOUNT_SID = "YOUR_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_NUMBER = "+1234567890"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# -------------------- DATABASE --------------------
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

# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return "🚀 SOS Backend Running Successfully"

# -------- REGISTER --------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
              (data["email"], data["password"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Registered successfully"})


# -------- LOGIN --------
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (data["email"], data["password"]))

    user = c.fetchone()
    conn.close()

    return jsonify({"success": bool(user)})


# -------- ADD CONTACT --------
@app.route("/add_contact", methods=["POST"])
def add_contact():
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute("""
        INSERT INTO contacts (user, name, phone)
        VALUES (?, ?, ?)
    """, (data["user"], data["name"], data["phone"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Contact added successfully"})


# -------- GET CONTACTS --------
@app.route("/get_contacts/<user>")
def get_contacts(user):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT name, phone FROM contacts WHERE user=?", (user,))
    rows = c.fetchall()
    conn.close()

    contacts = [{"name": r[0], "phone": r[1]} for r in rows]

    return jsonify(contacts)


# -------- SOS FUNCTION --------
@app.route("/sos", methods=["POST"])
def sos():
    data = request.json

    user = data.get("user")
    lat = data.get("latitude")
    lon = data.get("longitude")

    conn = get_db()
    c = conn.cursor()

    # Save SOS
    c.execute("""
        INSERT INTO sos_alerts (user, latitude, longitude)
        VALUES (?, ?, ?)
    """, (user, lat, lon))

    # Fetch contacts
    c.execute("SELECT name, phone FROM contacts WHERE user=?", (user,))
    contacts = c.fetchall()

    conn.commit()
    conn.close()

    # 🚨 SOS MESSAGE
    message_body = f"""🚨 SOS ALERT!
User: {user}
Location: https://maps.google.com/?q={lat},{lon}
"""

    sent_count = 0

    for contact in contacts:
        try:
            client.messages.create(
                body=message_body,
                from_=TWILIO_NUMBER,
                to=contact[1]
            )
            sent_count += 1
        except Exception as e:
            print(f"❌ Failed for {contact[1]}:", e)

    return jsonify({
        "message": "SOS sent!",
        "contacts_notified": sent_count
    })


# -------- VIEW ALL SOS --------
@app.route("/get_sos")
def get_sos():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM sos_alerts")
    rows = c.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "user": row[1],
            "latitude": row[2],
            "longitude": row[3]
        })

    return jsonify(data)


# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)
