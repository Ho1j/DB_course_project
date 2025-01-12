from flask import Blueprint, session, render_template, current_app
from utils import create_orders_list
from database import execute_and_fetch, SqlProvider
from access import auth_required, group_required


bp_user_orders = Blueprint('bp_user_orders', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_user_orders/sql')

@bp_user_orders.route('', methods=['GET'])
@auth_required
@group_required
def user_orders():
    email = session.get('email')
    sql = provider.get_sql("view_orders.sql", email=email)
    result = execute_and_fetch(current_app.config["DB_CONFIG"], sql)

    orders = create_orders_list(result)

    return render_template('user-orders.html', orders=orders)