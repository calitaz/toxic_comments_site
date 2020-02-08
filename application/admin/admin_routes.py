from flask import Blueprint, render_template
from flask import current_app as app

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='templates',
                     static_folder='../static',
                     url_prefix='/admin')

@admin_bp.route('/login')
def main_login():

    return render_template('login.html')    
