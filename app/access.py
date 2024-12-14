from flask import session, request, current_app, redirect, url_for, flash
from functools import wraps


def group_validation(config: dict):
    bp_endpoint = request.endpoint.split('.')[0]
    if 'group_name' in session:
        group_name = session['group_name']
        if group_name in config and bp_endpoint in config[group_name]:
            return True
        return False


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            if request.endpoint == 'bp_auth.login_page':
                return f(*args, **kwargs)
            flash('Необходимо авторизоваться', 'error')
            return redirect(url_for('bp_auth.login_page'))
            # flash('Необходимо авторизоваться', 'error')
            # return redirect(url_for('bp_auth.login_page'))
    return wrapper


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['ACCESS_CONFIG']
        if group_validation(config):
            return f(*args, **kwargs)
        else:
            flash('У Вас нет доступа к этому варианту использования', 'error')
            return redirect(url_for('home_page'))
    return wrapper
