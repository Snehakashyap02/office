from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session handling

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = user[1]
            return "Login successful! Welcome, {}.".format(user[1])
            # Or redirect(url_for('dashboard'))
        else:
            message = "Invalid username or password."
    return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
