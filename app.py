from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
import bcrypt
import random
import smtplib
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'roshan_tech_secret_key_2024'

# MongoDB Atlas Configuration - ADD DATABASE NAME
app.config['MONGO_URI'] = 'mongodb+srv://roshan_admin:Er6zAXKGcHjPCUTB@cluster0.jrwmjfa.mongodb.net/roshan_tech_users?retryWrites=true&w=majority&appName=Cluster0'

# Initialize MongoDB with error handling
try:
    mongo = PyMongo(app)
    # Test the connection
    mongo.db.command('ping')
    print("✅ MongoDB Atlas connected successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    mongo = None

def send_otp(email, otp):
    try:
        print(f"Sending OTP {otp} to {email}")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('roshansasi2018@gmail.com', 'szpklgzzaanxmoio')
        
        message = f"""Subject: ROSHAN TECHNOLOGIES - Email Verification

Welcome to ROSHAN TECHNOLOGIES!

Your verification code is: {otp}

This OTP is valid for 10 minutes.

INNOVATE. ELEVATE. DOMINATE.

Best regards,
ROSHAN TECHNOLOGIES Team"""
        
        server.sendmail('roshansasi2018@gmail.com', email, message)
        server.quit()
        print(f"✅ OTP sent successfully to {email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    # Check if MongoDB is connected
    if mongo is None:
        flash("Database connection error. Please try again later.", "error")
        return redirect(url_for('login_page'))
    
    email = request.form['email']
    password = request.form['password']
    
    print(f"🔍 Login attempt for: {email}")
    
    try:
        user = mongo.db.users.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['logged_in_user'] = email
            session['user_name'] = user.get('name', email.split('@')[0])
            flash("Welcome back to ROSHAN TECHNOLOGIES!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for('login_page'))
    except Exception as e:
        print(f"❌ Login error: {e}")
        flash("Login failed. Please try again.", "error")
        return redirect(url_for('login_page'))

@app.route('/signup', methods=['POST'])
def signup():
    # Check if MongoDB is connected
    if mongo is None:
        flash("Database connection error. Please try again later.", "error")
        return redirect(url_for('signup_page'))
    
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    print(f"📝 Signup attempt for: {email}")
    
    if password != confirm_password:
        flash("Passwords do not match!", "error")
        return redirect(url_for('signup_page'))
    
    if len(password) < 6:
        flash("Password must be at least 6 characters long!", "error")
        return redirect(url_for('signup_page'))
    
    try:
        user_exists = mongo.db.users.find_one({'email': email})
        if user_exists:
            flash("Email already registered with ROSHAN TECHNOLOGIES", "error")
            return redirect(url_for('signup_page'))
        
        otp = str(random.randint(100000, 999999))
        otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        
        # Store OTP temporarily - FIXED SYNTAX ERROR
        mongo.db.otps.update_one(
            {'email': email},
            {'$set': {'otp': otp, 'expires_at': otp_expiry}},
            upsert=True
        )
        
        # Store user data temporarily in session - FIXED SYNTAX ERROR
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        session['signup_data'] = {
            'name': name,
            'email': email,
            'password': hashed_password
        }
        
        if send_otp(email, otp):
            flash("Verification code sent to your email!", "success")
            return redirect(url_for('verify_email'))
        else:
            flash("Failed to send verification email. Please try again.", "error")
            session.pop('signup_data', None)
            return redirect(url_for('signup_page'))
            
    except Exception as e:
        print(f"❌ Signup error: {e}")
        flash("Signup failed. Please try again.", "error")
        return redirect(url_for('signup_page'))

@app.route('/verify-email')
def verify_email():
    if 'signup_data' not in session:
        flash("Please complete signup process first.", "error")
        return redirect(url_for('signup_page'))
    return render_template('verify_email.html')

@app.route('/verify-email', methods=['POST'])
def verify_email_post():
    # Check if MongoDB is connected
    if mongo is None:
        flash("Database connection error. Please try again later.", "error")
        return redirect(url_for('signup_page'))
    
    if 'signup_data' not in session:
        flash("Session expired. Please signup again.", "error")
        return redirect(url_for('signup_page'))
    
    entered_otp = request.form['otp']
    signup_data = session['signup_data']
    email = signup_data['email']
    
    print(f"🔐 Verifying OTP for {email}: {entered_otp}")
    
    try:
        otp_record = mongo.db.otps.find_one({'email': email})
        
        if otp_record and otp_record['otp'] == entered_otp and datetime.utcnow() < otp_record['expires_at']:
            # Save user to database - FIXED SYNTAX ERROR
            user_data = {
                'name': signup_data['name'],
                'email': signup_data['email'],
                'password': signup_data['password'],
                'created_at': datetime.utcnow(),
                'verified': True
            }
            
            result = mongo.db.users.insert_one(user_data)
            print(f"✅ User saved with ID: {result.inserted_id}")
            
            mongo.db.otps.delete_one({'email': email})
            session.pop('signup_data', None)
            
            flash("Account created successfully! Welcome to ROSHAN TECHNOLOGIES!", "success")
            return redirect(url_for('login_page'))
        else:
            flash("Invalid or expired verification code!", "error")
            return redirect(url_for('verify_email'))
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        flash("Verification failed. Please try again.", "error")
        return redirect(url_for('verify_email'))

@app.route('/resend-otp')
def resend_otp():
    if 'signup_data' not in session:
        flash("Session expired. Please signup again.", "error")
        return redirect(url_for('signup_page'))
    
    email = session['signup_data']['email']
    otp = str(random.randint(100000, 999999))
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    
    try:
        # FIXED SYNTAX ERROR
        mongo.db.otps.update_one(
            {'email': email},
            {'$set': {'otp': otp, 'expires_at': otp_expiry}},
            upsert=True
        )
        
        if send_otp(email, otp):
            flash("New verification code sent!", "success")
        else:
            flash("Failed to resend verification code.", "error")
    except Exception as e:
        print(f"❌ Resend OTP error: {e}")
        flash("Failed to resend verification code.", "error")
    
    return redirect(url_for('verify_email'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in_user' not in session:
        flash("Please login to access dashboard.", "error")
        return redirect(url_for('login_page'))
    
    user_name = session.get('user_name', 'User')
    return render_template('dashboard.html', user_name=user_name)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('home'))

# Health check route
@app.route('/health')
def health_check():
    if mongo is None:
        return "❌ Database: Disconnected", 500
    try:
        mongo.db.command('ping')
        user_count = mongo.db.users.count_documents({})
        return f"✅ Database: Connected | Users: {user_count}", 200
    except Exception as e:
        return f"❌ Database Error: {str(e)}", 500

# FIXED: Only one app.run() call
if __name__ == '__main__':
    app.run(debug=True)
