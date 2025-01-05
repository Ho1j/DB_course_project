from flask import Blueprint, render_template, request, current_app, session, flash, redirect, url_for
from pymysql.err import IntegrityError
from database import execute_and_fetch, SqlProvider, DBContextManager
from access import auth_required, group_required


bp_booking = Blueprint('bp_booking', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./sql')


@bp_booking.route('', methods=['POST'])
@auth_required
@group_required
def tickets_booking():
    quantity = request.form.get('quantity')
    schedule_id = request.form.get('schedule_id')
    flight_number = request.form.get('flight_number')
    flight_date = request.form.get('flight_date')
    return render_template("tickets-booking.html", quantity=quantity, schedule_id=schedule_id, flight_number=flight_number, flight_date=flight_date)


@bp_booking.route('/process', methods=['POST'])
@auth_required
@group_required
def process_tickets_booking():
    quantity = int(request.form.get('quantity'))
    schedule_id = request.form.get('schedule_id')
    user_id = session.get('user_id')

    try:
        with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
            sql = provider.get_sql("create_order.sql", user_id=user_id)
            cursor.execute(sql)
            order_id = cursor.lastrowid

            for i in range(1, quantity + 1):
                passport = request.form.get(f'passport-{i}')
                first_name = request.form.get(f'first-name-{i}')
                last_name = request.form.get(f'last-name-{i}')
                birth_date = request.form.get(f'birth-date-{i}')
                sql = provider.get_sql("create_ticket.sql", order_id=order_id, schedule_id=schedule_id, passport=passport, first_name=first_name, last_name=last_name,
                                       birth_date=birth_date)
                cursor.execute(sql)
        flash("Заказ успешно создан!", "success")
        return redirect(url_for('bp_user_menu.user_menu'))

    except IntegrityError as e:
        flash(f"Бронь на паспорт {passport} уже существует.", "error")
        return redirect(url_for('bp_user_menu.user_menu'))

    except Exception as e:
        flash("Произошла ошибка при создании заказа.", "error")
        return redirect(url_for('bp_user_menu.user_menu'))
