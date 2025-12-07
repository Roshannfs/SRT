from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)
app.secret_key = 'roshan_tech_secret_key_2024'

# MongoDB Atlas Configuration
app.config['MONGO_URI'] = 'mongodb+srv://roshan_admin:W9KKFwJg0jeOJPNm@cluster0.rqu4lvj.mongodb.net/roshan_tech_db'

# Initialize MongoDB with error handling
try:
    mongo = PyMongo(app)
    mongo.db.command('ping')
    print("✅ MongoDB Atlas connected successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    mongo = None

def send_otp(email, otp):
    """Send OTP with HTML email template"""
    try:
        print(f"Sending OTP {otp} to {email}")
         
        message = MIMEMultipart('alternative')
        message['Subject'] = 'ROSHAN TECHNOLOGIES - Email Verification'
        message['From'] = 'roshansasi2018@gmail.com'
        message['To'] = email
        logo_url = "https://i.ibb.co/27h5cMnt/logo.png"
        # Create email message
        # Create HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification - Roshan Technologies</title>
           

            
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
                    padding: 40px 20px;
                }}
                
                .email-content {{
                    background: rgba(25, 25, 25, 0.95);
                    border: 2px solid #d4af37;
                    border-radius: 16px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8),
                                0 0 40px rgba(212, 175, 55, 0.15);
                }}
                
                .logo-section {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                
                .logo {{
                    width: 60px;
                    height: 60px;
                    margin: 0 auto 15px;
                    background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 32px;
                    font-weight: bold;
                }}
                
                .company-name {{
                    font-size: 14px;
                    color: #d4af37;
                    letter-spacing: 2px;
                    text-transform: uppercase;
                    margin-bottom: 5px;
                    font-weight: 600;
                }}
                
                .tagline {{
                    font-size: 11px;
                    color: #888;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }}
                
                h1 {{
                    font-size: 28px;
                    font-weight: 700;
                    margin-bottom: 15px;
                    color: #fff;
                    text-align: center;
                }}
                
                .subtitle {{
                    font-size: 14px;
                    color: #aaa;
                    margin-bottom: 30px;
                    line-height: 1.6;
                    text-align: center;
                }}
                
                .otp-box {{
                    background: rgba(212, 175, 55, 0.12);
                    border: 2px solid #d4af37;
                    border-radius: 12px;
                    padding: 30px;
                    margin: 30px 0;
                    text-align: center;
                }}
                
                .otp-label {{
                    font-size: 12px;
                    color: #d4af37;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    margin-bottom: 15px;
                    display: block;
                    font-weight: 600;
                }}
                
                .otp-code {{
                    font-size: 36px;
                    font-weight: 700;
                    color: #f4d03f;
                    letter-spacing: 8px;
                    font-family: 'Courier New', monospace;
                    margin: 15px 0;
                }}
                
                .otp-timer {{
                    font-size: 12px;
                    color: #aaa;
                    margin-top: 15px;
                }}
                
                .timer-highlight {{
                    color: #f4d03f;
                    font-weight: 600;
                }}
                
                .details-section {{
                    background: rgba(212, 175, 55, 0.08);
                    border: 1px solid rgba(212, 175, 55, 0.2);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 25px 0;
                    font-size: 13px;
                    color: #aaa;
                }}
                
                .detail-row {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 12px;
                    padding-bottom: 12px;
                    border-bottom: 1px solid rgba(212, 175, 55, 0.1);
                }}
                
                .detail-row:last-child {{
                    margin-bottom: 0;
                    padding-bottom: 0;
                    border-bottom: none;
                }}
                
                .detail-label {{
                    color: #888;
                    font-weight: 500;
                }}
                
                .detail-value {{
                    color: #d4af37;
                    font-weight: 600;
                }}
                
                .instructions {{
                    background: rgba(51, 205, 102, 0.08);
                    border-left: 4px solid #33cd66;
                    border-radius: 8px;
                    padding: 16px;
                    margin: 25px 0;
                    font-size: 12px;
                    color: #aaa;
                    line-height: 1.6;
                }}
                
                .instructions-title {{
                    color: #33cd66;
                    font-weight: 600;
                    margin-bottom: 8px;
                    display: block;
                }}
                
                .security-note {{
                    background: rgba(212, 175, 55, 0.08);
                    border: 1px solid rgba(212, 175, 55, 0.2);
                    border-radius: 8px;
                    padding: 16px;
                    margin: 25px 0;
                    font-size: 12px;
                    color: #aaa;
                    line-height: 1.6;
                }}
                
                .security-icon {{
                    font-size: 14px;
                    margin-right: 8px;
                }}
                
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid rgba(212, 175, 55, 0.1);
                    text-align: center;
                    font-size: 11px;
                    color: #888;
                }}
                
                .footer-tagline {{
                    color: #d4af37;
                    font-weight: 600;
                    margin: 10px 0;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }}
                
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
                    color: #1a1a1a;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin: 20px 0;
                    font-size: 12px;
                }}
                
                @media (max-width: 600px) {{
                    .email-content {{
                        padding: 25px;
                    }}
                    
                    h1 {{
                        font-size: 22px;
                    }}
                    
                    .otp-code {{
                        font-size: 28px;
                        letter-spacing: 6px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-content">
                    <!-- Logo Section -->
                    <div class="logo-section">
    <img src="{logo_url}" alt="Roshan Technologies Logo" style="width: 80px; height: auto; margin-bottom: 15px;">
    <div class="company-name">Roshan Technologies</div>
    <div class="tagline">Innovate. Elevate. Dominate.</div>
</div>
           
                    
                    <!-- Main Content -->
                    <h1>Verify Your Email</h1>
                    <p class="subtitle">Welcome to Roshan Technologies! To complete your registration, please use the verification code below.</p>
                    
                    <!-- OTP Box -->
                    <div class="otp-box">
                        <span class="otp-label">📧 Your Verification Code</span>
                        <div class="otp-code">{otp}</div>
                        <div class="otp-timer">
                            Valid for <span class="timer-highlight">10 minutes</span>
                        </div>
                    </div>
                    
                    <!-- Details -->
                    <div class="details-section">
                        <div class="detail-row">
                            <span class="detail-label">Status:</span>
                            <span class="detail-value">✓ Active</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Sent To:</span>
                            <span class="detail-value">{email}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Expires In:</span>
                            <span class="detail-value">10 Minutes</span>
                        </div>
                    </div>
                    
                    <!-- Instructions -->
                    <div class="instructions">
                        <span class="instructions-title">✓ What to do next:</span>
                        1. Copy the verification code above<br>
                        2. Return to the verification page<br>
                        3. Paste the code in the input field<br>
                        4. Click 'Verify Code' to complete registration
                    </div>
                    
                    <!-- Security Note -->
                    <div class="security-note">
                        <span class="security-icon">🛡️</span>
                        <strong>Security Alert:</strong> Never share your verification code with anyone. Roshan Technologies will never ask for your OTP via email or phone.
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer">
                        <div class="footer-tagline">Thank you for choosing us!</div>
                        <p>If you did not request this verification code, please ignore this email.</p>
                        <p style="margin-top: 15px; color: #666;">
                            © 2024 Roshan Technologies. All rights reserved.
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        msg_alternative = MIMEText(html_body, 'html')
        message.attach(msg_alternative)
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 465)
        server.starttls()
        server.login('roshansasi2018@gmail.com', 'niwdnhxgwrwsmpfm')
        server.sendmail('roshansasi2018@gmail.com', email, message.as_string())
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
        
        mongo.db.otps.update_one(
            {'email': email},
            {'$set': {'otp': otp, 'expires_at': otp_expiry}},
            upsert=True
        )
        
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

if __name__ == '__main__':

    app.run(debug=True)
