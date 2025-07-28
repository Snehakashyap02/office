from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    user = {
        "name": "Sneha Kashyap",
        "bank_balance": 970,
        "transactions_count": 5,
        "budget_total": 200,
        "budget_left": 50,
        "daily_allowance": 2.78,
        "days_left": 18
    }

    transactions = [
        {"icon": "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
         "category": "Food", "date": "Wednesday, July 9", "amount": -150}
    ]

    trend_data = [825, 863, 900, 938, 938]
    trend_labels = ["Jun 14", "Jun 22", "Jun 29", "Jul 7", "Jul 14"]

    return render_template("dash.html", user=user, transactions=transactions,
                           trend_data=trend_data, trend_labels=trend_labels)

if __name__ == "__main__":
    app.run(debug=True)
