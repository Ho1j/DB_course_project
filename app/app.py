import json
from flask import Flask, render_template, session

from access import not_authenticated

from blueprints.bp_auth.route import bp_auth
from blueprints.bp_reg.route import bp_reg
from blueprints.bp_menu.route import bp_menu
from blueprints.bp_queries.route import bp_queries
from blueprints.bp_reports.route import bp_reports
from blueprints.bp_user_orders.route import bp_user_orders
from blueprints.bp_orders.route import bp_orders

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DB_CONFIG'] = json.load(open('configs/db_config_win.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['CACHE_CONFIG'] = json.load(open('configs/cache.json'))

app.register_blueprint(bp_queries, url_prefix='/queries')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_reports, url_prefix='/reports')
app.register_blueprint(bp_reg, url_prefix='/reg')
app.register_blueprint(bp_menu, url_prefix='/user-menu')
app.register_blueprint(bp_user_orders, url_prefix='/my-orders')
app.register_blueprint(bp_orders, url_prefix='/orders')


@app.route('/')
@not_authenticated
def welcome_page():
    return render_template('index.html', user_id=session.get('user_id'), login=session.get('login'))


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5003, debug = True)


