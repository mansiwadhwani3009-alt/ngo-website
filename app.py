from flask import Flask, render_template, request
import sqlite3
import smtplib

app = Flask(__name__)

# ---------------- DATABASE FUNCTION ----------------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Volunteers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        program TEXT
    )
    """)

    # Donations table (FIXED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        cause TEXT,
        amount TEXT,
        payment TEXT,
        message TEXT
    )
    """)

    # Contacts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()
# Call once
create_tables()

# ---------------- EMAIL FUNCTION ----------------
#def send_email(to_email, subject, message):
 #   sender_email = "your_email@gmail.com"
  #  password = "your_app_password"

   # try:
    #   server.starttls()
     #   server.login(sender_email, password)

      #  email_message = f"Subject: {subject}\n\n{message}"
       # server.sendmail(sender_email, to_email, email_message)

        #server.quit()
    ##   print("Email error:", e)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template("index.html")

# Volunteer Form
@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        program = request.form['program']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO volunteers (name, email, phone, program) VALUES (?, ?, ?, ?)",
            (name, email, phone, program)
        )

        conn.commit()
        conn.close()

        return render_template("success.html", message="Registration Successful!")

    return render_template("volunteer.html")
if not name or not email or not phone or not program:
    return "All fields are required!" 

# Donation Form
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cause = request.form['cause']
        amount = request.form['amount']
        payment = request.form['payment']
        message = request.form['message']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO donations (name, email, cause, amount, payment, message) VALUES (?, ?, ?, ?, ?, ?)",
        (name, email, cause, amount, payment, message)
        )

        conn.commit()
        conn.close()

        return render_template("success.html", message="Donation Successful!")

    return render_template("donate.html")
if not name or not email or not amount:
    return "Please fill all required fields!"

# Contact Form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return render_template("success.html", message="Message Sent!")
if request.method == 'POST':
    # existing code

return render_template("contact.html")
# Admin Panel
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM volunteers")
    volunteers = cursor.fetchall()

    cursor.execute("SELECT * FROM donations")
    donations = cursor.fetchall()

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    conn.close()

    return render_template("admin.html",
                           volunteers=volunteers,
                           donations=donations,
                           contacts=contacts)

if __name__ == "__main__":
    app.run()