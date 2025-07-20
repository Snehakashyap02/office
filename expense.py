from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'

def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

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

    return render_template('dashboard.html', expenses=expenses, chart_data=chart_data, selected_category=filter_category)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        session['username'] = user
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
