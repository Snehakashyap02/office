import sqlite3
import os

def init_users_db():
    """Initialize the users database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                 )''')
    
    conn.commit()
    conn.close()
    print("Users database initialized successfully!")

def init_expenses_db():
    """Initialize the expenses database"""
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    
    # Create expenses table
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')
    
    conn.commit()
    conn.close()
    print("Expenses database initialized successfully!")

def setup_templates():
    """Move HTML files to templates directory"""
    html_files = [
        'login.html', 'signup.html', 'welcome.html', 'dash.html',
        'forgot_password.html', 'reset_password.html', 'logout.html',
        'view_expense.html', 'budget.html'
    ]
    
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Move HTML files to templates directory
    for file in html_files:
        if os.path.exists(file):
            os.rename(file, f'templates/{file}')
            print(f"Moved {file} to templates/")

if __name__ == "__main__":
    print("Initializing databases...")
    init_users_db()
    init_expenses_db()
    
    print("\nSetting up templates...")
    setup_templates()
    
    print("\nSetup complete! You can now run the application.") 