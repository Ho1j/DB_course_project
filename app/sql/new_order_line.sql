INSERT INTO orders_lines(order_id, prod_id, amount)
VALUES((SELECT MAX(`order_id`) FROM user_orders), '$prod_id', '$amount');