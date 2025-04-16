from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from extensions import db
from models import Calculation
import numpy as np
from functools import wraps
from auth import login_required

bp = Blueprint('calculator', __name__)

def compute_diffusion_coefficient(x_A, D_AB0, D_BA0, q_A, T, D_exp, q_B, a_BA, a_AB, ra, rb):
    """
    Compute the diffusion coefficient using the HSU-CHEN equation.
    
    Args:
        x_A (float): Mole fraction of component A
        D_AB0 (float): Infinite dilution diffusion coefficient of A in B
        D_BA0 (float): Infinite dilution diffusion coefficient of B in A
        q_A (float): Surface area parameter for component A
        T (float): Temperature
        D_exp (float): Experimental diffusion coefficient
        q_B (float): Surface area parameter for component B
        a_BA (float): Interaction parameter for B-A
        a_AB (float): Interaction parameter for A-B
        ra (float): Molecular radius of component A
        rb (float): Molecular radius of component B
    
    Returns:
        tuple: (D_AB, error) where D_AB is the calculated diffusion coefficient
               and error is the percentage error compared to experimental value
    """
    try:
        # Solvent fraction
        x_B = 1 - x_A
        
        # Tau values
        tau_AB = np.exp(-a_AB / T)
        tau_BA = np.exp(-a_BA / T)
        tau_AA = 1
        tau_BB = 1
        
        # Lambda values
        lambda_A = ra ** (1 / 3)
        lambda_B = rb ** (1 / 3)
        
        # Phi values
        phi_A = x_A * lambda_A / (x_A * lambda_A + x_B * lambda_B)
        phi_B = x_B * lambda_B / (x_A * lambda_A + x_B * lambda_B)
        
        # Theta values
        theta_A = (x_A * q_A) / (x_A * q_A + x_B * q_B)
        theta_B = (x_B * q_B) / (x_A * q_A + x_B * q_B)
        theta_BA = (theta_B * tau_BA) / (theta_A * tau_AA + theta_B * tau_BA)
        theta_AB = (theta_A * tau_AB) / (theta_A * tau_AB + theta_B * tau_BB)
        theta_AA = (theta_A * tau_AA) / (theta_A * tau_AA + theta_B * tau_BA)
        theta_BB = (theta_B * tau_BB) / (theta_A * tau_AB + theta_B * tau_BB)
        
        # HSU-CHEN equation
        term1 = x_B * np.log(D_AB0) + x_A * np.log(D_BA0) + 2 * (x_A * np.log(x_A / phi_A) + x_B * np.log(x_B / phi_B)) + 2 * x_A * x_B * ((phi_A / x_A) * (1 - (lambda_A / lambda_B)) + (phi_B / x_B) * (1 - (lambda_B / lambda_A)))
        term2 = (x_B * q_A) * ((1 - theta_BA ** 2) * np.log(tau_BA) + (1 - theta_BB ** 2) * tau_AB * np.log(tau_AB)) + (x_A * q_B) * ((1 - theta_AB ** 2) * np.log(tau_AB) + (1 - theta_AA ** 2) * tau_BA * np.log(tau_BA))
        
        ln_D_AB = term1 + term2
        D_AB = np.exp(ln_D_AB)
        
        # Error calculation
        error = (np.abs(D_AB - D_exp) / D_exp) * 100
        
        return D_AB, error
    except Exception as e:
        raise ValueError(f"Error in diffusion coefficient calculation: {str(e)}")

@bp.route('/calculator', methods=['GET'])
@login_required
def calculator():
    return render_template('calculator.html')

@bp.route('/results', methods=['POST'])
@login_required
def results():
    try:
        # Retrieve and validate form values
        form_data = {
            'x_A': float(request.form['x_A'].replace(',', '.')),
            'D_AB0': float(request.form['D_AB0']),
            'D_BA0': float(request.form['D_BA0']),
            'rA': float(request.form['rA']),
            'rB': float(request.form['rB']),
            'D_AB_exp': float(request.form['DAB_exp']),
            'a_AB': float(request.form['a_AB']),
            'a_BA': float(request.form['a_BA']),
            'T': float(request.form['T']),
            'q_A': float(request.form['q_A']),
            'q_B': float(request.form['q_B'])
        }

        # Compute diffusion coefficient and error
        D_AB, error = compute_diffusion_coefficient(
            form_data['x_A'], form_data['D_AB0'], form_data['D_BA0'],
            form_data['q_A'], form_data['T'], form_data['D_AB_exp'],
            form_data['q_B'], form_data['a_BA'], form_data['a_AB'],
            form_data['rA'], form_data['rB']
        )
        
        # Save calculation to database
        new_calculation = Calculation(
            user_id=session['user_id'],
            result_D_AB=D_AB,
            result_error=error,
            **form_data
        )
        db.session.add(new_calculation)
        db.session.commit()
        
        # Display results
        return render_template('results.html', D_AB=D_AB, error=error)
    
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('calculator.calculator'))
    except Exception as e:
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('calculator.calculator'))

@bp.route('/history')
@login_required
def history():
    user_calculations = Calculation.query.filter_by(user_id=session['user_id']).order_by(Calculation.date_created.desc()).all()
    return render_template('history.html', calculations=user_calculations) 