from flask import session, request, current_app, redirect, url_for, flash
from functools import wraps


def group_validation(config: dict):
    bp_endpoint = request.endpoint.split('.')[0]
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and bp_endpoint in config[user_group]:
            return True
        return False


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            if request.endpoint == 'bp_auth.user_login':
                return f(*args, **kwargs)
            flash('Необходимо авторизоваться', 'error')
            return redirect(url_for('bp_auth.user_auth'))
    return wrapper


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['ACCESS_CONFIG']
        if group_validation(config):
            return f(*args, **kwargs)
        else:
            flash('У Вас нет доступа к этому варианту использования', 'error')
            return redirect(url_for('bp_menu.menu'))
    return wrapper


def not_authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for('bp_menu.menu'))
        return f(*args, **kwargs)
    return wrapper

