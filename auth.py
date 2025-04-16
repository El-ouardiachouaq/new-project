from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from extensions import db, mail
from models import User
from flask_mail import Message
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Form validation
        if not all([first_name, last_name, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Invalid email or password', 'error')
            return render_template('login.html')
        
        # Check if user is blocked
        if user.is_blocked():
            remaining_time = (user.blocked_until - datetime.utcnow()).total_seconds() / 60
            flash(f'Account temporarily locked. Try again in {int(remaining_time)} minutes.', 'error')
            return render_template('login.html')
        
        # Check password
        if user.check_password(password):
            # Reset failed attempts
            user.reset_failed_attempts()
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log in user
            login_user(user, remember=remember)
            
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            # Increment failed attempts
            user.increment_failed_attempts()
            attempts_left = current_app.config['MAX_LOGIN_ATTEMPTS'] - user.failed_attempts
            flash(f'Invalid password. {attempts_left} attempts remaining.', 'error')
            
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expiry = datetime.utcnow() + timedelta(seconds=current_app.config['PASSWORD_RESET_TIMEOUT'])
            db.session.commit()
            
            # Send reset email
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset Request - Diffusion Calculator',
                         sender=('Diffusion Calculator', current_app.config['MAIL_DEFAULT_SENDER']),
                         recipients=[user.email])
            msg.body = f'''Hello {user.first_name},

You have requested to reset your password for your Diffusion Calculator account.

To reset your password, please visit the following link:
{reset_url}

This link will expire in 1 hour for security reasons.

If you did not make this request, please ignore this email and your password will remain unchanged.

Best regards,
The Diffusion Calculator Team
'''
            mail.send(msg)
            
            flash('Check your email for instructions to reset your password.', 'info')
            return redirect(url_for('auth.login'))
        
        flash('Email address not found.', 'error')
    return render_template('reset_password_request.html')

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or user.reset_token_expiry < datetime.utcnow():
        flash('Invalid or expired reset token. Please request a new one.', 'error')
        return redirect(url_for('auth.reset_password_request'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html')
        
        # Update password
        user.set_password(password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        
        flash('Your password has been reset. You can now log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html') 