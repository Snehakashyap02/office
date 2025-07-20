from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login')
def login():
    return render_template('login.html')  # must exist in templates/

@app.route('/signup')
def signup():
    return render_template('signup.html')  # must exist in templates/

if __name__ == '__main__':
    app.run(debug=True)
