from flask import Blueprint, render_template, request, current_app, session, redirect, url_for, flash
from utils import create_orders_list
from database import execute_and_fetch, SqlProvider
from access import auth_required, group_required

bp_queries = Blueprint('bp_queries', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_queries/sql')


@bp_queries.route('/menu')
@auth_required
@group_required
def queries_menu():
    user_group = session.get('user_group')
    login = session.get('login')
    return render_template('queries-menu.html', user_group=user_group, login=login)


@bp_queries.route('/search-orders-by-mail', methods=['GET'])
@auth_required
@group_required
def search_orders_by_mail():
    return render_template('search-orders-by-email.html')

@bp_queries.route('/search-orders-by-mail/results', methods=['GET'])
@auth_required
@group_required
def show_orders_by_email():
    email = request.args.get('email')
    sql = provider.get_sql('get_orders_by_email.sql', email=email)
    get_orders_by_mail_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    if not get_orders_by_mail_result:
        flash(f"Заказы с почтой {email} не найдены", "error")
        return redirect(url_for('bp_queries.queries_menu'))
    orders = create_orders_list(get_orders_by_mail_result)
    return render_template('show-orders.html', orders=orders)


@bp_queries.route('/search-flights-by-month', methods=['GET'])
@auth_required
@group_required
def search_flights_by_month():
    return render_template('search-flights-by-month.html')


@bp_queries.route('/search-flights-by-month/results', methods=['GET'])
@auth_required
@group_required
def show_flights_by_month():
    month = request.args.get('month')
    sql = provider.get_sql('get_flights_by_month.sql', month=month)
    get_flights_by_month_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    if not get_flights_by_month_result:
        flash(f"Заказы за {month} не найдены", "error")
        return redirect(url_for('bp_queries.queries_menu'))
    return render_template('show-flights.html', result=get_flights_by_month_result)


@bp_queries.route('/search-flights-by-countries', methods=['GET'])
@auth_required
@group_required
def search_flights_by_countries():
    return render_template('search-flights-by-countries.html')


@bp_queries.route('/search-flights-by-countries/results', methods=['GET'])
@auth_required
@group_required
def show_flights_by_countries():
    departure_country = request.args.get('departure-country')
    arrival_country = request.args.get('arrival-country')
    sql = provider.get_sql('get_flights_by_countries.sql', departure_country=departure_country, arrival_country=arrival_country)
    get_flights_by_countries_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    if not get_flights_by_countries_result:
        flash(f"Рейсы из {departure_country} в {arrival_country} не найдены", "error")
        return redirect(url_for('bp_queries.queries_menu'))
    return render_template('show-flights.html', result=get_flights_by_countries_result)

