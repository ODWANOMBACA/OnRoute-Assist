from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_user, login_required, current_user
from flask_security.utils import hash_password
from flask_mail import Mail
from models.user import User

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Leye:leye@localhost/assist'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy()
user_datastore = SQLAlchemyUserDatastore(db, User)  # Import User model from models.user
security = Security()

# Configure Flask-Mail (if needed)
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_mail_username'
app.config['MAIL_PASSWORD'] = 'your_mail_password'
mail = Mail(app)

db.init_app(app)

# Define a simple route
@app.route('/')
def hello_world():
    return 'Hello, OnRoute Assist!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')  # Add username field
        
        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('login'))

        # Create a new user
        new_user = User(username=username, email=email, password=hash_password(password))  # Hash the password
        db.session.add(new_user)
        db.session.commit()

        # Log in the newly registered user
        login_user(new_user)
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Retrieve the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)