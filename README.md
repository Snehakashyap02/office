# Flask Expense Tracker

A web-based expense tracking application built with Flask and SQLite.

## Features

- User registration and authentication
- Expense tracking with categories
- Dashboard with expense visualization
- Budget management
- Password reset functionality

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize the Project

Run the initialization script to set up databases and organize files:

```bash
python init_databases.py
```

This will:
- Create the `users.db` database for user authentication
- Create the `expenses.db` database for expense tracking
- Move HTML files to the `templates/` directory

### 3. Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:5001`

## Database Schema

### Users Database (`users.db`)
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: User password

### Expenses Database (`expenses.db`)
- `id`: Primary key
- `user`: Username (foreign key to users)
- `category`: Expense category
- `amount`: Expense amount
- `date`: Date of expense
- `created_at`: Timestamp of record creation

## Application Routes

- `/` - Redirects to welcome page
- `/welcome` - Welcome page
- `/login` - User login
- `/signup` - User registration
- `/dashboard` - Main dashboard (requires login)
- `/logout` - User logout
- `/forgot_password` - Password reset request
- `/reset_password` - Password reset
- `/budget` - Budget management (requires login)
- `/view_expense` - Expense details (requires login)

## Usage

1. Visit the application at `http://localhost:5000`
2. Create a new account using the signup page
3. Log in with your credentials
4. Start tracking your expenses on the dashboard
5. Use the budget and expense view pages for detailed management

## Security Notes

- This is a development application with basic security
- Passwords are stored in plain text (not recommended for production)
- Session management is basic
- For production use, implement proper password hashing, HTTPS, and additional security measures 