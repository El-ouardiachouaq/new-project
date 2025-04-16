from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from extensions import db
from models import User, Calculation
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    calculations = Calculation.query.filter_by(user_id=current_user.id).order_by(Calculation.date_created.desc()).all()
    return render_template('dashboard.html', calculations=calculations)

@bp.route('/history')
@login_required
def history():
    calculations = Calculation.query.filter_by(user_id=current_user.id).order_by(Calculation.date_created.desc()).all()
    return render_template('history.html', calculations=calculations)

@bp.route('/calculate', methods=['GET', 'POST'])
@login_required
def calculate():
    if request.method == 'POST':
        try:
            # Get form data with proper error handling
            form_data = {}
            required_fields = ['x_A', 'D_AB0', 'D_BA0', 'rA', 'rB', 'D_AB_exp', 'a_AB', 'a_BA', 'T', 'q_A', 'q_B']
            
            for field in required_fields:
                if field not in request.form:
                    raise ValueError(f"Missing required field: {field}")
                try:
                    # Handle comma in decimal numbers
                    value = request.form[field].replace(',', '.')
                    form_data[field] = float(value)
                except ValueError:
                    raise ValueError(f"Invalid value for {field}. Please enter a valid number.")
            
            # Import the compute_diffusion_coefficient function
            from calculator import compute_diffusion_coefficient
            
            # Compute diffusion coefficient and error
            D_AB, error = compute_diffusion_coefficient(
                form_data['x_A'], form_data['D_AB0'], form_data['D_BA0'],
                form_data['q_A'], form_data['T'], form_data['D_AB_exp'],
                form_data['q_B'], form_data['a_BA'], form_data['a_AB'],
                form_data['rA'], form_data['rB']
            )
            
            # Create new calculation
            calculation = Calculation(
                user_id=current_user.id,
                result_D_AB=D_AB,
                result_error=error,
                **form_data
            )
            
            db.session.add(calculation)
            db.session.commit()
            flash('Calculation saved successfully!', 'success')
            
            # Render results page
            return render_template('results.html', D_AB=D_AB, error=error, calculation=calculation)
            
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('main.calculate'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while saving the calculation: {str(e)}', 'error')
            return redirect(url_for('main.calculate'))
            
    return render_template('calculator.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        
        # Check if email is already taken by another user
        existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('edit_profile.html')
        
        try:
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('main.profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'error')
            
    return render_template('edit_profile.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html') 