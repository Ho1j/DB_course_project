from flask import Blueprint, render_template, session
from access import auth_required

bp_menu = Blueprint('bp_menu', __name__, template_folder='templates', static_folder='static')

@bp_menu.route('', methods=['GET'])
@auth_required
def menu():
    return render_template('menu.html', user_group=session.get('user_group'), login=session.get('login'))
