from pickletools import long1

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for, flash
from utils import create_orders_list
from database import execute_and_fetch, SqlProvider
from access import auth_required, group_required

bp_queries = Blueprint('bp_queries', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_queries/sql')


@bp_queries.route('/menu')
@group_required
def queries_menu():
    return render_template('queries-menu.html', user_group=session.get('user_group'),
                           login=session.get('login'))


@bp_queries.route('/all-flights', methods=['GET'])
@group_required
def show_flights_list():
    sql = provider.get_sql('get_domestic_flights.sql')
    domestic_flights_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)

    sql = provider.get_sql('get_international_flights.sql')
    international_flights_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)

    return render_template('all-flights.html', domestic_flights_result=domestic_flights_result,
                           international_flights_result=international_flights_result, login=session.get('login'))


@bp_queries.route('/orders-by-email', methods=['GET'])
@group_required
def search_orders_by_mail():
    return render_template('orders-by-email-form.html', login=session.get('login'))


@bp_queries.route('/orders-by-mail/results', methods=['GET'])
@group_required
def show_orders_by_email():
    email = request.args.get('email')
    sql = provider.get_sql('get_orders_by_email.sql', email=email)
    get_orders_by_mail_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)

    if not get_orders_by_mail_result:
        flash(f"Заказы с почтой {email} не найдены", "error")
        return redirect(url_for('bp_queries.queries_menu'))

    orders = create_orders_list(get_orders_by_mail_result)
    return render_template('orders-by-email-results.html', orders=orders, login=session.get('login'))


@bp_queries.route('/flights-by-month', methods=['GET'])
@group_required
def search_flights_by_month():
    return render_template('flights-by-month-form.html', login=session.get('login'))


@bp_queries.route('/flights-by-month/results', methods=['GET'])
@group_required
def show_flights_by_month():
    month = request.args.get('month')
    sql = provider.get_sql('get_flights_by_month.sql', month=month)
    get_flights_by_month_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)

    if not get_flights_by_month_result:
        flash(f"Рейсы за {month} не найдены", "error")
        return redirect(url_for('bp_queries.queries_menu'))

    return render_template('flights-by-month-results.html', result=get_flights_by_month_result,
                           login=session.get('login'))


@bp_queries.route('/flights-by-countries', methods=['GET'])
@group_required
def search_flights_by_countries():
    return render_template('flights-by-countries-form.html', login=session.get('login'))


@bp_queries.route('/search-flights-by-countries/results', methods=['GET'])
@group_required
def show_flights_by_countries():
    departure_country = request.args.get('departure-country')
    arrival_country = request.args.get('arrival-country')

    sql = provider.get_sql('get_flights_by_countries.sql', departure_country=departure_country, arrival_country=arrival_country)
    get_flights_by_countries_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)

    if not get_flights_by_countries_result:
        flash(f"Рейсы из {departure_country} в {arrival_country} не найдены", "error")
        return redirect(url_for('bp_queries.queries_menu'))

    return render_template('flights-by-countries-results.html', result=get_flights_by_countries_result)


@bp_queries.route('/cashiers', methods=['GET'])
@group_required
def show_cashiers():
    sql = provider.get_sql('get_cashiers.sql')
    cashiers_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    print(cashiers_result)
    return render_template('cashiers-results.html', result=cashiers_result, login=session.get('login'))


