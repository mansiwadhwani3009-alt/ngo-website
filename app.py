from flask import Flask, render_template, request, redirect
import mysql.connector
import smtplib

app = Flask(__name__)

# Database connection (XAMPP)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ngo_db"
)
cursor = db.cursor()

# ---------------- EMAIL FUNCTION ----------------
def send_email(to_email, subject, message):
    sender_email = "your_email@gmail.com"
    password = "your_app_password"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, email_message)

        server.quit()
    except Exception as e:
        print("Email error:", e)

# ---------------- ROUTES ----------------

# Home
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

        cursor.execute(
            "INSERT INTO volunteers (name, email, phone, program) VALUES (%s, %s, %s, %s)",
            (name, email, phone, program)
        )
        db.commit()

        # Send confirmation email
        #send_email(email, "Registration Successful",
                  # "Thank you for joining Trapti Jan Kalyan as a volunteer!")

        return render_template("success.html", message="Registration Successful!")

    return render_template("volunteer.html")


# Donation Form
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']   # IMPORTANT
        cause = request.form['cause']
        amount = request.form['amount']
        payment = request.form['payment']
        message = request.form['message']

        cursor.execute(
            "INSERT INTO donations (name, cause, amount, payment, message) VALUES (%s, %s, %s, %s, %s)",
            (name, cause, amount, payment, message)
        )
        db.commit()

        # Send confirmation email
        #send_email(email, "Donation Successful",
                  # "Thank you for your generous donation!")

        return render_template("success.html", message="Donation Successful!")

    return render_template("donate.html")


# Contact Form
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )
    db.commit()

    return render_template("success.html", message="Message Sent!")


# Admin Panel
@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM volunteers")
    volunteers = cursor.fetchall()

    cursor.execute("SELECT * FROM donations")
    donations = cursor.fetchall()

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    return render_template("admin.html",
                           volunteers=volunteers,
                           donations=donations,
                           contacts=contacts)


if __name__ == "__main__":
    app.run(debug=True)