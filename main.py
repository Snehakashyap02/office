from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session handling

def get_db_connection():
    """Get connection to expenses database"""
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_databases():
    """Initialize both databases if they don't exist"""
    # Initialize users database
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
        print("Users database created!")

    # Initialize expenses database
    if not os.path.exists('expenses.db'):
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT NOT NULL,
                        category TEXT NOT NULL,
                        amount REAL NOT NULL,
                        date TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )''')
        conn.commit()
        conn.close()
        print("Expenses database created!")

@app.route('/')
def index():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

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
            return redirect(url_for('dashboard'))
        else:
            message = "Invalid username or password."
    return render_template('login.html', message=message)

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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        date = request.form['date']
        conn.execute("INSERT INTO expenses (user, category, amount, date) VALUES (?, ?, ?, ?)",
                     (session['username'], category, amount, date))
        conn.commit()

    filter_category = request.args.get('category', 'All')
    cur = conn.cursor()

    if filter_category != 'All':
        cur.execute("SELECT * FROM expenses WHERE user=? AND category=?", (session['username'], filter_category))
    else:
        cur.execute("SELECT * FROM expenses WHERE user=?", (session['username'],))
        
    expenses = cur.fetchall()

    # Aggregate data for pie chart
    cur.execute("SELECT category, SUM(amount) as total FROM expenses WHERE user=? GROUP BY category", (session['username'],))
    chart_data = cur.fetchall()

    conn.close()

    return render_template('dash.html', expenses=expenses, chart_data=chart_data, selected_category=filter_category)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        # Here you would typically send a password reset email
        message = "If the email exists, a password reset link has been sent."
    return render_template('forgot_password.html', message=message)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    message = ""
    if request.method == 'POST':
        # Handle password reset logic
        message = "Password has been reset successfully."
    return render_template('reset_password.html', message=message)

@app.route('/budget')
def budget():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('budget.html')

@app.route('/view_expense')
def view_expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('view_expense.html')

if __name__ == '__main__':
    # Initialize databases on startup
    init_databases()
    app.run(debug=True, host='0.0.0.0', port=8000) 