document.addEventListener('DOMContentLoaded', function() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    if (password && confirmPassword) {
        // Create password requirements container
        const requirementsDiv = document.createElement('div');
        requirementsDiv.className = 'password-requirements mt-2';
        requirementsDiv.innerHTML = `
            <div class="requirement" id="length"><i class="bi bi-x-circle"></i> At least 8 characters</div>
            <div class="requirement" id="lowercase"><i class="bi bi-x-circle"></i> At least one lowercase letter</div>
            <div class="requirement" id="uppercase"><i class="bi bi-x-circle"></i> At least one uppercase letter</div>
            <div class="requirement" id="number"><i class="bi bi-x-circle"></i> At least one number</div>
            <div class="requirement" id="match"><i class="bi bi-x-circle"></i> Passwords match</div>
        `;
        
        password.parentNode.appendChild(requirementsDiv);
        
        // Validation function
        function validatePassword() {
            const passwordValue = password.value;
            const confirmValue = confirmPassword.value;
            
            // Length validation
            const lengthRequirement = document.getElementById('length');
            if (passwordValue.length >= 8) {
                lengthRequirement.classList.add('valid');
                lengthRequirement.classList.remove('invalid');
                lengthRequirement.innerHTML = '<i class="bi bi-check-circle"></i> At least 8 characters';
            } else {
                lengthRequirement.classList.add('invalid');
                lengthRequirement.classList.remove('valid');
                lengthRequirement.innerHTML = '<i class="bi bi-x-circle"></i> At least 8 characters';
            }
            
            // Lowercase validation
            const lowercaseRequirement = document.getElementById('lowercase');
            if (/[a-z]/.test(passwordValue)) {
                lowercaseRequirement.classList.add('valid');
                lowercaseRequirement.classList.remove('invalid');
                lowercaseRequirement.innerHTML = '<i class="bi bi-check-circle"></i> At least one lowercase letter';
            } else {
                lowercaseRequirement.classList.add('invalid');
                lowercaseRequirement.classList.remove('valid');
                lowercaseRequirement.innerHTML = '<i class="bi bi-x-circle"></i> At least one lowercase letter';
            }
            
            // Uppercase validation
            const uppercaseRequirement = document.getElementById('uppercase');
            if (/[A-Z]/.test(passwordValue)) {
                uppercaseRequirement.classList.add('valid');
                uppercaseRequirement.classList.remove('invalid');
                uppercaseRequirement.innerHTML = '<i class="bi bi-check-circle"></i> At least one uppercase letter';
            } else {
                uppercaseRequirement.classList.add('invalid');
                uppercaseRequirement.classList.remove('valid');
                uppercaseRequirement.innerHTML = '<i class="bi bi-x-circle"></i> At least one uppercase letter';
            }
            
            // Number validation
            const numberRequirement = document.getElementById('number');
            if (/[0-9]/.test(passwordValue)) {
                numberRequirement.classList.add('valid');
                numberRequirement.classList.remove('invalid');
                numberRequirement.innerHTML = '<i class="bi bi-check-circle"></i> At least one number';
            } else {
                numberRequirement.classList.add('invalid');
                numberRequirement.classList.remove('valid');
                numberRequirement.innerHTML = '<i class="bi bi-x-circle"></i> At least one number';
            }
            
            // Match validation
            const matchRequirement = document.getElementById('match');
            if (passwordValue === confirmValue && passwordValue !== '') {
                matchRequirement.classList.add('valid');
                matchRequirement.classList.remove('invalid');
                matchRequirement.innerHTML = '<i class="bi bi-check-circle"></i> Passwords match';
            } else {
                matchRequirement.classList.add('invalid');
                matchRequirement.classList.remove('valid');
                matchRequirement.innerHTML = '<i class="bi bi-x-circle"></i> Passwords match';
            }
        }
        
        // Event listeners
        password.addEventListener('keyup', validatePassword);
        confirmPassword.addEventListener('keyup', validatePassword);
        
        // Form submission validation
        const form = password.closest('form');
        if (form) {
            form.addEventListener('submit', function(event) {
                validatePassword();
                
                // Check if all requirements are met
                const requirements = document.querySelectorAll('.requirement');
                let allValid = true;
                
                requirements.forEach(function(req) {
                    if (!req.classList.contains('valid')) {
                        allValid = false;
                    }
                });
                
                if (!allValid) {
                    event.preventDefault();
                    alert('Please make sure your password meets all requirements.');
                }
            });
        }
    }
});