from flask import Blueprint, render_template, request, current_app, session, flash, redirect, url_for
from werkzeug.security import check_password_hash
from database import execute_and_fetch, SqlProvider
from access import already_authenticated


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./blueprints/bp_auth/sql')


@bp_auth.route('', methods=['GET'])
@already_authenticated
def user_auth():
    return render_template('auth.html', login_type="user")

@bp_auth.route('', methods=['POST'])
@already_authenticated
def process_user_auth():
    login = request.form.get('login')
    password = request.form.get('password')
    sql = provider.get_sql('auth.sql', login=login)
    result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    if not result:
        flash('Пользователь не найден', 'error')
        return render_template('auth.html', login_type="user")
    if not check_password_hash(result[0]['password'], password):
        flash('Неверный пароль', 'error')
        return render_template('auth.html', login_type="user")
    session['user_group'], session['login'] = result[0]['user_group'], result[0]['login']
    session['user_id'], session['email'] = result[0]['user_id'], result[0]['email']
    flash(f"Вы авторизовались как {session['login']}", 'success')
    return redirect(url_for('bp_user_menu.user_menu'))


@bp_auth.route('/staff', methods=['GET'])
@already_authenticated
def staff_auth():
    if request.method == 'GET':
        return render_template('auth.html', login_type="staff")


@bp_auth.route('/staff', methods=['POST'])
@already_authenticated
def process_staff_auth():
    login = request.form.get('login')
    password = request.form.get('password')
    sql = provider.get_sql('internal_auth.sql', login=login)
    result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    if not result:
        flash('Пользователь не найден', 'error')
        return render_template('auth.html', login_type="staff")
    if result[0]['password'] != password:
        flash('Неверный пароль', 'error')
        return render_template('auth.html', login_type="staff")
    session['user_id'], session['login'], session['user_group'] = result[0]['user_id'], result[0]['login'], result[0]['user_group']

    #Добавление id продавца в сессию
    if session['user_group'] == 'cashier':
        user_id = session['user_id']
        sql = provider.get_sql('get_cashier_id.sql', user_id=user_id)
        result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        session['cashier_id'] = result[0]['cashier_id']

    flash(f"Вы авторизовались как {session['login']}", 'success')
    return redirect(url_for('bp_user_menu.user_menu'))

@bp_auth.route('/logout', methods=['GET'])
def process_logout():
    session.clear()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('welcome_page'))
