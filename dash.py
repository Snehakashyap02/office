from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Dummy data for example (replace with DB)
dummy_expenses = [
    {"description": "Lunch", "amount": 120.5, "category": "Food", "date": "2025-07-10", "payment_method": "Cash"},
    {"description": "Bus", "amount": 40.0, "category": "Transport", "date": "2025-07-11", "payment_method": "Card"},
    {"description": "Groceries", "amount": 350.0, "category": "Shopping", "date": "2025-07-02", "payment_method": "UPI"},
    {"description": "Movie", "amount": 200.0, "category": "Entertainment", "date": "2025-06-25", "payment_method": "Card"},
    {"description": "Coffee", "amount": 80.0, "category": "Food", "date": "2025-07-14", "payment_method": "Cash"},
]

@app.route('/login')
def login():
    session['username'] = 'testuser'
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    all_expenses = dummy_expenses  # Replace with DB call
    filtered = []

    # Date filters
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        if start and end:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            filtered = [e for e in all_expenses if start_date <= datetime.strptime(e['date'], '%Y-%m-%d') <= end_date]
        else:
            # Default: This month
            today = datetime.today()
            filtered = [
                e for e in all_expenses
                if datetime.strptime(e['date'], '%Y-%m-%d').month == today.month and
                   datetime.strptime(e['date'], '%Y-%m-%d').year == today.year
            ]
    except ValueError:
        filtered = []

    category_totals = defaultdict(float)
    daily_totals = defaultdict(float)

    for e in filtered:
        category_totals[e['category']] += float(e['amount'])
        daily_totals[e['date']] += float(e['amount'])

    category_labels = list(category_totals.keys())
    category_amounts = list(category_totals.values())
    daily_labels = sorted(daily_totals.keys())
    daily_amounts = [daily_totals[d] for d in daily_labels]
    monthly_total = sum(category_amounts)
    recent_expenses = sorted(filtered, key=lambda x: x['date'], reverse=True)[:5]

    return render_template("dashboard.html",
                           monthly_total=monthly_total,
                           recent_expenses=recent_expenses,
                           category_labels=category_labels,
                           category_amounts=category_amounts,
                           daily_labels=daily_labels,
                           daily_amounts=daily_amounts,
                           start=start,
                           end=end)
