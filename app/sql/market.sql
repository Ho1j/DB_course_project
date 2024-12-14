SELECT prod_name, prod_price, prod_measure
FROM availability JOIN products
ON availability.prod_id = products.prod_id
WHERE $market = 1 AND prod_cat = '$category'