from flask import Blueprint, render_template, request, current_app, session, flash, redirect, url_for
from werkzeug.security import check_password_hash
from database import execute_and_fetch, SqlProvider, DBContextManager
from access import not_authenticated


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_auth/sql')


@bp_auth.route('', methods=['GET'])
@not_authenticated
def user_auth():
    return render_template('auth.html', login_type="user")

@bp_auth.route('', methods=['POST'])
@not_authenticated
def process_user_auth():
    login = request.form.get('login')
    password = request.form.get('password')

    sql = provider.get_sql('auth.sql', login=login)
    auth_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    if not auth_result:
        flash('Пользователь не найден', 'error')
        return render_template('auth.html', login_type="user")
    if not check_password_hash(auth_result[0]['password'], password):
        flash('Неверный пароль', 'error')
        return render_template('auth.html', login_type="user")
    session['user_group'], session['login'] = auth_result[0]['user_group'], auth_result[0]['login']
    session['user_id'], session['email'] = auth_result[0]['user_id'], auth_result[0]['email']
    flash(f"Вы авторизовались как {session['login']}", 'success')
    return redirect(url_for('bp_user_menu.user_menu'))


@bp_auth.route('/staff', methods=['GET'])
@not_authenticated
def staff_auth():
    if request.method == 'GET':
        return render_template('auth.html', login_type="staff")


@bp_auth.route('/staff', methods=['POST'])
@not_authenticated
def process_staff_auth():
    login = request.form.get('login')
    password = request.form.get('password')

    try:
        with (DBContextManager(current_app.config['DB_CONFIG']) as cursor):
            sql = provider.get_sql('internal_auth.sql', login=login)
            auth_result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)

            if not auth_result:
                flash('Пользователь не найден', 'error')
                return render_template('auth.html', login_type="staff")
            if auth_result[0]['password'] != password:
                flash('Неверный пароль', 'error')
                return render_template('auth.html', login_type="staff")
            if auth_result[0]['user_group'] == 'cashier':
                sql = provider.get_sql('cashier_info.sql', user_id=auth_result[0]['user_id'])
                print(sql)
                cashier_info = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
                if not cashier_info:
                    flash(f'Кассир с user id {auth_result[0]['user_id']} не найден', 'error')
                    return render_template('auth.html', login_type="staff")
                if cashier_info[0]['termination_date'] is not None:
                    flash('Доступ запрещен', 'error')
                    return render_template('auth.html', login_type="staff")
                session['cashier_id'] = cashier_info[0]['cashier_id']

            session['user_id'], session['login'], session['user_group'] = auth_result[0]['user_id'], auth_result[0]['login'], auth_result[0]['user_group']

    except Exception as e:
        flash("Произошла ошибка при авторизации", "error")
        return redirect(url_for('bp_user_menu.user_menu'))

    flash(f"Вы авторизовались как {session['login']}", 'success')
    return redirect(url_for('bp_user_menu.user_menu'))

@bp_auth.route('/logout', methods=['GET'])
def process_logout():
    session.clear()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('welcome_page'))
