from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route: Forgot Password
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user:
            return redirect(url_for('reset_password', username=username))
        else:
            flash("Username not found.")
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

# Route: Reset Password
@app.route('/reset-password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password)

        conn = get_db_connection()
        conn.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
        conn.commit()
        conn.close()

        flash("Password updated successfully. Please login.")
        return redirect(url_for('login'))  # Ensure you have a login route in your full app

    return render_template('reset_password.html', username=username)

# Dummy route for login (just for redirect to work)
@app.route('/login')
def login():
    return "Login Page Placeholder"

if __name__ == '__main__':
    app.run(debug=True)
