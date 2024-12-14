import json
from flask import Flask, render_template, session, flash, redirect, url_for
from blueprints.bp_queries.route import bp_queries
from blueprints.bp_auth.route import bp_auth
from blueprints.bp_reg.route import bp_reg
from blueprints.bp_reports.route import bp_reports
from blueprints.bp_basket.route import bp_basket

from access import auth_required, group_required
from sql_provider import SQL_Provider


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DB_CONFIG'] = json.load(open('configs/db_config.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['CACHE_CONFIG'] = json.load(open('configs/cache.json'))

app.register_blueprint(bp_queries, url_prefix='/queries')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_reports, url_prefix='/reports')
app.register_blueprint(bp_basket, url_prefix='/basket')
app.register_blueprint(bp_reg, url_prefix='/registration')



provider = SQL_Provider('sql/')


@app.route('/')
@auth_required
def home_page():
    if session['group_name'] == 'user':
        return render_template('home.html', group_name=session['group_name'])
    if session['group_name'] == 'admin':
        return render_template('admin.html', group_name=session['group_name'])

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5003, debug = True)


