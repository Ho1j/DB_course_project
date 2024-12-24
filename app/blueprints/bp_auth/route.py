from flask import Blueprint, render_template, request, current_app, session, flash, redirect, url_for
from werkzeug.security import check_password_hash
from database import execute_and_fetch, SqlProvider
from access import already_authenticated


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./sql')


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
    session['group_name'], session['login'] = result[0]['user_group'], result[0]['login']
    session['user_id'] = result[0]['user_id']
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
    print(sql)
    result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
    if not result:
        flash('Пользователь не найден', 'error')
        return render_template('auth.html', login_type="staff")
    if result[0]['password'] != password:
        flash('Неверный пароль', 'error')
        return render_template('auth.html', login_type="staff")
    session['group_name'], session['login'] = result[0]['user_group'], result[0]['login']
    session['user_id'] = result[0]['user_id']
    flash(f"Вы авторизовались как {session['login']}", 'success')
    return redirect(url_for('bp_user_menu.user_menu'))

@bp_auth.route('/logout', methods=['GET'])
def process_logout():
    session.pop('group_name', None)
    session.pop('login', None)
    session.pop('user_id', None)
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('welcome_page'))
