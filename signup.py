from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Runs only once, when the database doesn't exist
def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                     )''')
        conn.commit()
        conn.close()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, password))
            conn.commit()
            message = "Signup successful! You can now log in."
        except sqlite3.IntegrityError:
            message = "Username or email already exists."
        finally:
            conn.close()
    return render_template('signup.html', message=message)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
