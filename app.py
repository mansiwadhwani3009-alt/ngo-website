from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# HOME
@app.route('/')
def home():
    return render_template('index.html')

# ABOUT
@app.route('/about')
def about():
    return render_template('about.html')

# VOLUNTEER
@app.route('/volunteer', methods=['GET','POST'])
def volunteer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO volunteers (name,email,phone) VALUES (?,?,?)",
                    (name,email,phone))
        conn.commit()
        conn.close()

        return "Volunteer Registered!"

    return render_template('volunteer.html')

# DONATION
@app.route('/donate', methods=['GET','POST'])
def donate():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO donations (name,amount) VALUES (?,?)",
                    (name,amount))
        conn.commit()
        conn.close()

        return "Donation Successful!"

    return render_template('donate.html')

# CONTACT
@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (name,email,message) VALUES (?,?,?)",
                    (name,email,message))
        conn.commit()
        conn.close()

        return "Message Sent!"

    return render_template('contact.html')

# ADMIN PANEL
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    volunteers = cur.execute("SELECT * FROM volunteers").fetchall()
    donations = cur.execute("SELECT * FROM donations").fetchall()
    contacts = cur.execute("SELECT * FROM contacts").fetchall()

    conn.close()

    return render_template('admin.html',
                           volunteers=volunteers,
                           donations=donations,
                           contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)