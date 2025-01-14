from flask import Blueprint, session, render_template, current_app, url_for, redirect, request, flash
from datetime import date
from pymysql import MySQLError

from utils import create_orders_list
from database import execute_and_fetch, SqlProvider, DBContextManager
from access import group_required


bp_orders = Blueprint('bp_orders', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_orders/sql')


@bp_orders.route('/menu', methods=['GET'])
@group_required
def orders_menu():
    return render_template('orders-menu.html', login=session.get('login'))


@bp_orders.route('/create', methods=['GET'])
@group_required
def start_create_order():
    return render_template("start-create-order.html",
                           login=session.get('login'), today=date.today().isoformat())


@bp_orders.route('/create/check', methods=['GET'])
@group_required
def check_order_flight():
    flight_number = request.args.get('flight-number')
    schedule_date = request.args.get('schedule-date')

    sql = provider.get_sql("get_available_tickets.sql", flight_number=flight_number, schedule_date=schedule_date)
    get_available_tickets_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)

    if not get_available_tickets_result:
        flash("Данного рейса не существует", "error")
        return redirect(url_for('bp_orders.orders_menu'))

    available_tickets = get_available_tickets_result[0]['available_tickets']
    if available_tickets == 0:
        flash("На данный рейса нет свободных мест", "error")
        return redirect(url_for('bp_orders.orders_menu'))

    schedule_id = get_available_tickets_result[0]['schedule_id']

    return render_template('passengers-quantity-form.html',
                           available_tickets=available_tickets, schedule_id=schedule_id)


@bp_orders.route('/create-tickets', methods=['GET'])
@group_required
def create_tickets_forms():
    schedule_id = request.args.get('schedule-id')
    passengers = request.args.get('passengers')
    return render_template('create-tickets-forms.html', passengers=passengers,
                           schedule_id=schedule_id, today=date.today().isoformat())


@bp_orders.route('/create-tickets/process', methods=['POST'])
@group_required
def create_tickets():
    schedule_id = request.form.get('schedule-id')
    passengers = int(request.form.get('passengers'))
    email = request.form.get('email')

    try:
        with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
            cashier_id = session.get('cashier_id')
            sql = provider.get_sql("create_order.sql", email=email, cashier_id=cashier_id)
            status = "confirmed"

            cursor.execute(sql)
            order_id = cursor.lastrowid

            for i in range(1, passengers + 1):
                passport = request.form.get(f'passport-{i}')
                first_name = request.form.get(f'first-name-{i}')
                last_name = request.form.get(f'last-name-{i}')
                birth_date = request.form.get(f'birth-date-{i}')
                seat_number = request.form.get(f'seat-number-{i}')
                if not seat_number:
                    sql = provider.get_sql("create_ticket.sql", order_id=order_id,
                                           schedule_id=schedule_id, passport=passport,
                                           first_name=first_name, last_name=last_name,
                                           birth_date=birth_date, status=status)
                else:
                    sql = provider.get_sql("create_ticket_with_seat.sql", order_id=order_id,
                                       schedule_id=schedule_id, passport=passport,
                                           first_name=first_name, last_name=last_name,
                                           birth_date=birth_date, seat_number=seat_number, status=status)
                cursor.execute(sql)
                sql = provider.get_sql("decrement_available_tickets.sql", schedule_id = schedule_id)
                cursor.execute(sql)
        flash("Заказ успешно создан", "success")
        return redirect(url_for('bp_orders.orders_menu'))

    except MySQLError as e:
        if e.args[0] == 1062:
            error_message = str(e.args[1])
            if "passport" in error_message:
                flash(f"Билет с паспортом {passport} уже существует", "error")
            elif "seat_number" in error_message:
                flash(f"Место {seat_number} уже занято на этом рейсе", "error")
            else:
                flash("Дублирующая запись: проверьте данные", "error")
        else:
            flash("Произошла ошибка при создании заказа.", "error")

        return redirect(url_for('bp_orders.orders_menu'))


#Поиск заказа по id
@bp_orders.route('/search', methods=['GET'])
@group_required
def search_order():
    return render_template("search-order-form.html", login=session.get('login'))


#Вывод заказа по id
@bp_orders.route('/search/result', methods=['GET'])
@group_required
def show_order():
    order_id = request.args.get('order_id')
    sql = provider.get_sql("get_order.sql", order_id=order_id)
    result = execute_and_fetch(current_app.config["DB_CONFIG"], sql)

    if not result:
        flash('Заказы не найдены', 'error')
        return redirect(url_for('bp_menu.user_menu'))

    orders = create_orders_list(result)

    return render_template('show-order.html', order_id=order_id, orders=orders,
                           login=session.get('login'), today=date.today().isoformat())


@bp_orders.route('/search/result/change/<int:order_id>', methods=['POST'])
@group_required
def change_order(order_id):
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
                    sql = provider.get_sql("increment_available_tickets.sql", ticket_id=ticket['ticket_id'])
                    cursor.execute(sql)
                    if cursor.rowcount <= 0:
                        flash("Не удалось увеличить доступные билеты.", "error")
                        return redirect(url_for('bp_orders.orders_menu'))

                    sql = provider.get_sql("transfer_ticket_to_cancelled.sql", ticket_id=ticket['ticket_id'])
                    cursor.execute(sql)

                    sql = provider.get_sql("delete_ticket.sql", ticket_id=ticket['ticket_id'])
                    cursor.execute(sql)
                if ticket['status'] == 'confirmed':
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

    return redirect(url_for('bp_orders.orders_menu'))

