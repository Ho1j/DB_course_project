from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from database import execute_and_fetch, SqlProvider
from access import already_authenticated

bp_reg = Blueprint('bp_reg', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./sql')


@bp_reg.route('', methods=['GET'])
@already_authenticated
def user_reg():
    return render_template('reg.html')


@bp_reg.route('', methods=['POST'])
@already_authenticated
def process_user_reg():
    login = request.form.get('login')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not login or not password:
        flash('Логин и пароль обязательны', 'error')
        return redirect(url_for('bp_reg.user_reg'))

    if password != confirm_password:
        flash('Пароли не совпадают', 'error')
        return redirect(url_for('bp_reg.user_reg'))

    hashed_password = generate_password_hash(password)

    sql = provider.get_sql('reg.sql', login=login, hashed_password=hashed_password)
    execute_and_fetch(current_app.config['DB_CONFIG'], sql)

    flash('Вы успешно зарегистрировались!', 'success')
    return redirect(url_for('bp_auth.user_auth'))
