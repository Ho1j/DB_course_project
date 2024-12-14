from calendar import month
from datetime import datetime

from flask import Blueprint, render_template, request, current_app, session, redirect, flash, url_for
from db_utils import execute_and_fetch
from sql_provider import SQL_Provider
import access


bp_reports = Blueprint('bp_reports', __name__, template_folder='templates', static_folder='static')
provider = SQL_Provider('./sql')

reports = [{'id': 1, 'name': 'Все заказы за месяц и год'}]


@bp_reports.route('/')
@access.auth_required
@access.group_required
def reports_choice():
    return render_template('reports_choice.html', reports=reports)

@bp_reports.route('/create_1', methods=['GET', 'POST'])
def create_1():
    if session['group_name'] == 'admin':
        if request.method == 'GET':
            return render_template('create_1.html')
        else:
            date_start = request.form.get('date_start')
            date_end = request.form.get('date_end')
            if datetime.strptime(date_start, "%Y-%m-%d") > datetime.strptime(date_end, "%Y-%m-%d"):
                flash('Дата начала периода не может быть меньше даты его конца', 'error')
                return render_template('create_1.html')

            find_check_count = provider.get_sql('check_total_orders_by_period_report_existence.sql', date_start=date_start, date_end=date_end)
            check_count = execute_and_fetch(current_app.config['DB_CONFIG'], find_check_count)
            print(check_count[0]['count'])
            print(check_count)
            if check_count[0]['count'] == 0:
                sql = provider.get_sql('create_total_orders_by_period_report.sql', date_start=date_start, date_end=date_end)
                result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
                if result is None:
                    flash(f"Вы создали отчёт за период с {date_start} по {date_end}", 'success')
                    return redirect(url_for('bp_reports.reports_choice'))
                else:
                    flash(f"Нельзя создать отчёт за период с {date_start} по {date_end}", 'error')
                    return render_template('create_1.html')

            else:
                flash('Такой отчёт уже существует', 'error')
                return render_template('create_1.html')
    else:
        flash('У Вас нет доступа', 'error')
        return render_template('reports_choice.html', reports=reports)

@bp_reports.route('/view_1', methods=['GET', 'POST'])
def view_1():
    if request.method == 'GET':
        sql = provider.get_sql('view_all_total_orders_by_period_reports.sql')
        print(sql)
        reports_list = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        if reports_list is None:
            flash('Нет доступных отчетов, создайте новый', 'error')
            return render_template('reports_choice.html', reports=reports)
        return render_template('view_1.html', reports_list=reports_list)
    else:
        date_start = request.form.get('date_start')
        date_end = request.form.get('date_end')
        sql = provider.get_sql('select_total_orders_by_period_report.sql', date_start=date_start, date_end=date_end)
        result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        title = f"Отчёт за период с {date_start} по {date_end}"
        num = 1
        return render_template('reports_result.html', result=result, title=title, num=num)
