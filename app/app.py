import json
from flask import Flask, render_template, session, flash, redirect, url_for

from blueprints.bp_queries.route import bp_queries
from blueprints.bp_auth.route import bp_auth
from blueprints.bp_reg.route import bp_reg
from blueprints.bp_reports.route import bp_reports
from blueprints.bp_basket.route import bp_basket
from blueprints.bp_search.route import bp_search
from blueprints.bp_booking.route import bp_booking
from blueprints.bp_user_menu.route import bp_user_menu

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DB_CONFIG'] = json.load(open('configs/db_config_win.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['CACHE_CONFIG'] = json.load(open('configs/cache.json'))

app.register_blueprint(bp_queries, url_prefix='/queries')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_reports, url_prefix='/reports')
app.register_blueprint(bp_basket, url_prefix='/basket')
app.register_blueprint(bp_reg, url_prefix='/registration')
app.register_blueprint(bp_search, url_prefix='/search')
app.register_blueprint(bp_booking, url_prefix='/booking')
app.register_blueprint(bp_user_menu, url_prefix='/user-menu')


@app.route('/')
def welcome_page():
    user_id = session.get('user_id')
    return render_template('index.html', user_id=user_id)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5003, debug = True)


