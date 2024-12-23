from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_utils import execute_and_fetch
from sql_provider import SqlProvider
import json
import access


bp_queries = Blueprint('bp_queries', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./sql')
with open('blueprints/bp_queries/static/imgs/products.json') as f:
    products_imgs = json.load(f)


@bp_queries.route('/')
@access.auth_required
@access.group_required
def search_choice():
    print(session)
    return render_template('search_choice.html')

@bp_queries.route('/input_price', methods=['GET', 'POST'])
def input_price():
    if request.method == 'GET':
        find_categories = provider.get_sql('categories.sql')
        categories = execute_and_fetch(current_app.config['DB_CONFIG'], find_categories)
        return render_template('input_price.html', categories=categories)
    else:
        category = request.form.get('category')
        price = request.form.get('price')
        sql = provider.get_sql('queries.sql', category=category, price=price)

        products = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        return render_template('results.html', prod_title=f"Продукты категории {category} с ценой до {price} руб",
                               products=products, products_imgs=products_imgs, page='input_price')

@bp_queries.route('/input_market', methods=['GET', 'POST'])
def input_market():
    markets = {'на Тверской': 'Tverskaya', 'на Маяковской': 'Mayakovskaya', 'на Курской': 'Kurskaya',
               'на Рижской': 'Rizhskaya', 'онлайн': 'online'}
    if request.method == 'GET':
        find_categories = provider.get_sql('categories.sql')
        categories = execute_and_fetch(current_app.config['DB_CONFIG'], find_categories)
        return render_template('input_market.html', markets=markets.keys(), categories=categories)
    else:
        market_rus = request.form.get('market')
        market = markets[market_rus]
        category = request.form.get('category')
        sql = provider.get_sql('market.sql', market=market, category=category)
        products = execute_and_fetch(current_app.config['DB_CONFIG'], sql)
        return render_template('results.html', prod_title=f"Продукты категории {category} в наличии в магазине {market_rus}",
                               products=products, products_imgs=products_imgs, page='input_market')
