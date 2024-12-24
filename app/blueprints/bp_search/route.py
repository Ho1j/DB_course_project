from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from datetime import date
from database import execute_and_fetch, SqlProvider
from access import auth_required, group_required


bp_search = Blueprint('bp_search', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./sql')

@bp_search.route('', methods=['GET'])
@auth_required
@group_required
def tickets_search():
    today = date.today().isoformat()

    if request.method == 'GET':
        return render_template('tickets-search.html', today=today)

@bp_search.route('/results', methods=['POST'])
@auth_required
@group_required
def process_tickets_search():
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    flight_date = request.form.get('flight_date')

    sql = provider.get_sql("search.sql", departure_city=departure_city, arrival_city=arrival_city, flight_date=flight_date)
    result = execute_and_fetch(current_app.config["DB_CONFIG"], sql)
    if not result:
        flash("Рейсы по заданным параметрам не найдены. Попробуйте изменить критерии поиска.", "error")
        return redirect(url_for('bp_search.search_tickets'))

    return render_template('tickets-search-results.html', result=result)

