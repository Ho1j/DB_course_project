from flask import Blueprint, render_template, request, current_app, session, redirect, flash, url_for
from pymysql import MySQLError
from datetime import date, timedelta

from database import execute_and_fetch, SqlProvider, DBContextManager
from access import group_required

bp_reports = Blueprint('bp_reports', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_reports/sql')


@bp_reports.route('/menu', methods=['GET'])
@group_required
def reports_menu():
    return render_template('reports_menu.html', login=session.get('login'))


@bp_reports.route('/create', methods=['GET'])
@group_required
def create_report():
    today = date.today()
    first_day_of_current_month = today.replace(day=1)
    # Последний день предыдущего месяца
    last_month = first_day_of_current_month - timedelta(days=1)
    max_month = last_month.strftime('%Y-%m')

    return render_template('create.html', login=session.get('login'),
                           report_type=request.args.get('report_type'), max_month=max_month)


@bp_reports.route('/create/monthly-report', methods=['GET'])
@group_required
def create_monthly_report():
    month = request.args.get('month') + '-01'
    report_type = request.args.get('report-type')

    try:
        with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
            if report_type == 'flights_revenue':
                sql = provider.get_sql('create_flights_revenue_report.sql', month=month)
            elif report_type == 'cashiers_sales':
                sql = provider.get_sql('create_cashiers_sales_report.sql', month=month)
            elif report_type == 'destinations':
                sql = provider.get_sql('create_destinations_report.sql', month=month)
            else:
                flash(f"Такого отчета не существует", 'error')
                return redirect(url_for('bp_reports.reports_menu'))
            print(sql)
            result = cursor.execute(sql)
            if result == 0:
                flash(f"Нет данных за месяц {month}", 'error')
                return redirect(url_for('bp_reports.reports_menu'))

        flash(f"Вы создали отчёт за месяц {month}", 'success')
        return redirect(url_for('bp_reports.reports_menu'))

    except MySQLError as e:
        if e.args[0] == 1644:
            flash(f"Отчет за месяц {month} уже существует", "error")
        else:
            flash("Произошла ошибка при создании отчета", "error")
        return redirect(url_for('bp_reports.reports_menu'))


@bp_reports.route('/view', methods=['GET'])
@group_required
def view_reports():
    report_type = request.args.get('report_type')
    sql = provider.get_sql('view_reports.sql', report_type=report_type + '_report')
    result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    print(result)
    return render_template('view_reports.html', report_type=report_type, result=result)


@bp_reports.route('/view/report', methods=['GET'])
@group_required
def view_report():
    report_type = request.args.get('report-type')
    report_month = request.args.get('report-month')
    report_month_full = report_month + '-01'

    if report_type == 'flights_revenue':
        sql = provider.get_sql('view_flights_revenue_report.sql', report_month_full=report_month_full)
        result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        return(render_template('report-result.html', report_type=report_type, result=result, report_month=report_month))
    elif report_type == 'cashiers_sales':
        sql = provider.get_sql('view_cashiers_sales_report.sql', report_month_full=report_month_full)
        result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        return(render_template('report-result.html', report_type=report_type, result=result, report_month=report_month))
    elif report_type == 'destinations':
        sql = provider.get_sql('view_destinations_report.sql', report_month_full=report_month_full)
        result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        return(render_template('report-result.html', report_type=report_type, result=result, report_month=report_month))
