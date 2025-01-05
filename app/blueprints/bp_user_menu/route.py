from flask import Blueprint, render_template, session
from access import auth_required

bp_user_menu = Blueprint('bp_user_menu', __name__, template_folder='templates', static_folder='static')

@bp_user_menu.route('', methods=['GET'])
@auth_required
def user_menu():
    group_name = session.get('group_name')
    return render_template('user-menu.html', group_name=group_name)


