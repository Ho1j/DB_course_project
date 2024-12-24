from flask import Blueprint, session, render_template, request, current_app, flash, redirect, url_for
from datetime import date
from database import execute_and_fetch, SqlProvider
from access import auth_required, group_required


bp_user_orders = Blueprint('bp_user_orders', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_user_orders/sql')

@bp_user_orders.route('', methods=['GET'])
@auth_required
@group_required
def user_orders():
    user_id = session.get('user_id')
    sql = provider.get_sql("view_orders.sql", user_id=user_id)
    result = execute_and_fetch(current_app.config["DB_CONFIG"], sql)
    print(result)
    orders = {}
    for order in result:
        order_id = order['order_id']
        if order_id not in orders:
            orders[order_id] = {
                'booking_date': order['booking_date'],
                'tickets': []
            }
        orders[order_id]['tickets'].append({
            'ticket_id': order['ticket_id'],
            'schedule_id': order['schedule_id'],
            'passport': order['passport'],
            'first_name': order['first_name'],
            'last_name': order['last_name'],
            'birth_date': order['birth_date'],
            'seat_number': order['seat_number'],
            'price': order['price'],
            'status': order['status']
        })

    return render_template('user-orders.html', orders=orders)