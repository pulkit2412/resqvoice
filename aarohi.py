from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

otp_store = {}

# -------- DATABASE --------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# -------- EMAIL OTP --------
def send_email_otp(to_email, otp):
    sender_email = "aarohibhattacharya28@gmail.com"
    sender_password = "doac sjvs hgjd htzs"

    msg = MIMEText(f"Your OTP is: {otp}")
    msg['Subject'] = "resQvoice OTP"
    msg['From'] = sender_email
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    send_email_otp(email, otp)

# -------- ROUTES --------
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data['email']

    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp

    send_email_otp(email, otp)

    return jsonify({"message": "OTP sent"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    user_otp = data['otp']

    if otp_store.get(email) != user_otp:
        return jsonify({"message": "Invalid OTP"})

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
              (email, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "Registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (data['email'], data['password']))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/sos', methods=['POST'])
def sos():
    data = request.json
    lat = data['latitude']
    lon = data['longitude']

    print(f"🚨 SOS ALERT! Location: {lat}, {lon}")

    return jsonify({"message": "SOS received"})

# -------- RUN --------
if __name__ == '__main__':
    app.run(debug=True)