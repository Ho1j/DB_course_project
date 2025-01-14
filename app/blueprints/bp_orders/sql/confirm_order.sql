UPDATE tickets
SET status = 'confirmed'
WHERE order_id = '$order_id';