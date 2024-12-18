from flask import Blueprint, render_template, request, current_app, session, flash, redirect, url_for
from db_utils import execute_and_fetch
from sql_provider import SQL_Provider
from werkzeug.security import generate_password_hash, check_password_hash

bp_reg = Blueprint('bp_reg', __name__, template_folder='templates', static_folder='static')
provider = SQL_Provider('./sql')


@bp_reg.route('/registration', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('reg.html')

    elif request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not login or not password:
            flash('Логин и пароль обязательны', 'error')
            return redirect(url_for('bp_reg.register_page'))

        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return redirect(url_for('bp_reg.register_page'))

        # Хэширование пароля
        hashed_password = generate_password_hash(password)

        sql = provider.get_sql('reg.sql', login = login, hashed_password = hashed_password)
        execute_and_fetch(current_app.config['DB_CONFIG'], sql)

        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('bp_auth.user_login'))
