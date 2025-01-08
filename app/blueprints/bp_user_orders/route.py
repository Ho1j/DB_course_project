﻿from flask import Blueprint, session, render_template, current_app
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
    print(result)
    orders = {}
    for order in result:
        order_id = order['order_id']
        if order_id not in orders:
            orders[order_id] = {
                'booking_date': order['booking_date'],
                'email': order['email'],
                'tickets': []
            }
        orders[order_id]['tickets'].append({
            'flight_number': order['flight_number'],
            'schedule_date': order['schedule_date'],
            'departure_time': order['departure_time'],
            'arrival_time': order['arrival_time'],
            'passport': order['passport'],
            'first_name': order['first_name'],
            'last_name': order['last_name'],
            'birth_date': order['birth_date'],
            'seat_number': order['seat_number'],
            'price': order['price'],
            'status': order['status']
        })

    return render_template('user-orders.html', orders=orders)