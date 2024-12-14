SELECT COUNT(*) AS count
FROM period_total_orders
WHERE period_start = '$date_start' AND period_end = '$date_end'