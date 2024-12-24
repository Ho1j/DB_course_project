from flask import Blueprint, render_template, request, current_app, session, flash, redirect, url_for
from werkzeug.security import check_password_hash
from database import execute_and_fetch, SqlProvider


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./sql')


@bp_auth.route('/', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('auth.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        sql = provider.get_sql('auth.sql', login=login)
        result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        if not result:
            flash('Пользователь не найден', 'error')
            return render_template('auth.html')
        if not check_password_hash(result[0]['password'], password):
            flash('Неверный пароль', 'error')
            return render_template('auth.html')
        session['group_name'], session['login'] = result[0]['user_group'], result[0]['login']
        session['user_id'] = result[0]['user_id']
        flash(f"Вы авторизовались как {session['login']}", 'success')
        return redirect(url_for('home_page'))

@bp_auth.route('/staff', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'GET':
        return render_template('auth.html', login_type="staff")
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        sql = provider.get_sql('internal_auth.sql', login=login)
        print(sql)
        result = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        if not result:
            flash('Пользователь не найден', 'error')
            return render_template('auth.html')
        if result[0]['password'] != password:
            flash('Неверный пароль', 'error')
            return render_template('auth.html')
        session['group_name'], session['login'] = result[0]['user_group'], result[0]['login']
        session['user_id'] = result[0]['user_id']
        flash(f"Вы авторизовались как {session['login']}", 'success')
        return redirect(url_for('home_page'))

@bp_auth.route('/logout')
def logout():
    session.pop('group_name', None)
    session.pop('login', None)
    session.pop('user_id', None)
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('bp_auth.user_login'))
