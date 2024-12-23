from flask import (
	Blueprint, render_template,
	request, current_app,
	session, redirect, url_for
)

from db_connect import DB_Context_Manager
from db_utils import execute_and_fetch
from sql_provider import SqlProvider
from cache.wrapper import fetch_from_cache
import access


bp_basket = Blueprint('bp_basket', __name__, template_folder='templates', static_folder='static')
provider = SqlProvider('./sql')


@bp_basket.route('/', methods=['GET', 'POST'])
@access.auth_required
@access.group_required
def basket_index():
	db_config = current_app.config['DB_CONFIG']
	cache_config = current_app.config['CACHE_CONFIG']
	cached_func = fetch_from_cache('all_items_cached', cache_config)(execute_and_fetch)
	sql = provider.get_sql('all_items.sql')
	items = cached_func(db_config, sql)
	if request.method == 'GET':
		basket_items = session.get('basket', {})
		print(session)
		print(basket_items)
		return render_template('index.html', items=items, basket_items=basket_items)
	else:
		prod_id = request.form['prod_id']
		item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]
		item_description = item_description[0]
		curr_basket = session.get('basket', {})

		if prod_id in curr_basket:
			curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount'] + 1
		else:
			curr_basket[prod_id] = {
				'name': item_description['name'],
				'price': item_description['price'],
				'amount': 1
			}
		session['basket'] = curr_basket
		session.permanent = True

		return redirect(url_for('bp_basket.basket_index'))


@bp_basket.route('/clear-basket')
def clear_basket():
	if 'basket' in session:
		session.pop('basket')
	return redirect(url_for('bp_basket.basket_index'))

@bp_basket.route('/order')
def order():
	sum = 0
	for item in session.get('basket').values():
		sum += item['amount'] * item['price']
	with DB_Context_Manager(current_app.config['DB_CONFIG']) as cursor:
		sql_order = provider.get_sql('new_order.sql', user_id=session['user_id'], sum=sum)
		cursor.execute(sql_order)
		session['basket'].items()
		for key, value in session['basket'].items():
			sql_basket = provider.get_sql('new_order_line.sql', prod_id=key, amount=value['amount'])
			cursor.execute(sql_basket)
		session.pop('basket')
	return render_template('order.html', sum=sum)