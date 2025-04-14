from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """
    Function to restrict access to admin routes

    Notes:
        *args and **kwargs are used to pass any positional and keyword arguments 
        from the original view function to the wrapped function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in and has admin rights
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
