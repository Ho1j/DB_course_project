SELECT prod_name, prod_measure, prod_price
FROM products
WHErE prod_cat = '$category' AND prod_price < '$price'