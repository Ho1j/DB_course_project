from flask import Blueprint, session, render_template, current_app, url_for, redirect, request, flash
from database import execute_and_fetch, SqlProvider, DBContextManager
from access import auth_required, group_required


bp_cashier_orders = Blueprint('bp_cashier_orders', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_cashier_orders/sql')

@bp_cashier_orders.route('', methods=['GET'])
@auth_required
@group_required
def pending_orders():
    sql = provider.get_sql("get_booked_orders.sql")
    result = execute_and_fetch(current_app.config["DB_CONFIG"], sql)

    if not result:
        flash('Заказы не найдены', 'error')
        return redirect(url_for('bp_user_menu.user_menu'))

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
            'ticket_id': order['ticket_id'],
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

    return render_template('pending-orders.html', orders=orders)


@bp_cashier_orders.route('/change/<int:order_id>', methods=['POST'])
@auth_required
@group_required
def change_order(order_id):
    action = request.form.get('action')
    if action == 'cancel':
        try:
            with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
                sql = provider.get_sql("transfer_order_to_cancelled.sql", order_id=order_id)
                cursor.execute(sql)
                sql = provider.get_sql("delete_order.sql", order_id=order_id)
                cursor.execute(sql)
            flash(f"Заказ №{order_id} удален!", "success")
            return redirect(url_for('bp_user_menu.user_menu'))

        except Exception as e:
            flash("Произошла ошибка при удалении заказа.", "error")
            return redirect(url_for('bp_user_menu.user_menu'))

    if action == 'confirm':
        sql = provider.get_sql("confirm_order.sql", order_id=order_id)
        execute_and_fetch(current_app.config["DB_CONFIG"], sql)
        return redirect(url_for('bp_user_menu.user_menu'))

    if action == 'change':
        try:
            ticket_count = int(request.form.get('ticket_count', 0))
            tickets = []

            for index in range(1, ticket_count + 1):
                ticket_data = {
                    'ticket_id': request.form.get(f'tickets[{index}][ticket_id]'),
                    'first_name': request.form.get(f'tickets[{index}][first_name]'),
                    'last_name': request.form.get(f'tickets[{index}][last_name]'),
                    'passport': request.form.get(f'tickets[{index}][passport]'),
                    'birth_date': request.form.get(f'tickets[{index}][birth_date]'),
                    'seat_number': request.form.get(f'tickets[{index}][seat_number]'),
                    'price': request.form.get(f'tickets[{index}][price]'),
                    'status': request.form.get(f'tickets[{index}][status]'),
                }
                tickets.append(ticket_data)


            with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
                for ticket in tickets:
                    if ticket['status'] == "canceled":
                        sql = provider.get_sql("transfer_ticket_to_cancelled.sql", ticket_id=ticket['ticket_id'])
                        print(sql)
                        cursor.execute(sql)
                        print(1)
                        sql = provider.get_sql("delete_ticket.sql", ticket_id=ticket['ticket_id'])
                        cursor.execute(sql)
                    else:
                        sql = provider.get_sql(
                            "update_ticket.sql",
                            ticket_id=ticket['ticket_id'],
                            first_name=ticket['first_name'],
                            last_name=ticket['last_name'],
                            passport=ticket['passport'],
                            birth_date=ticket['birth_date'],
                            seat_number=ticket['seat_number'],
                            price=ticket['price'],
                            status=ticket['status'],
                        )
                        cursor.execute(sql)

            flash(f"Заказ №{order_id} успешно обновлен!", "success")

        except Exception as e:
            flash(f"Ошибка обновления заказа: {str(e)}", "error")

        return redirect(url_for('bp_cashier_orders.pending_orders'))
