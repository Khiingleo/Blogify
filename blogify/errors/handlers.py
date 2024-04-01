from flask import Blueprint, render_template
"""handles errors"""

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    """handles 404 errors"""
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_404(error):
    """handles 403 errors"""
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_404(error):
    """handles 500 errors"""
    return render_template('errors/500.html'), 500
