SELECT
    o.id AS order_id,
    o.email,
    o.booking_date AS booking_date,
    f.flight_number,
    s.schedule_date,
    f.departure_time,
    f.arrival_time,
    t.passport,
    t.first_name,
    t.last_name,
    t.birth_date,
    t.seat_number,
    t.price,
    t.status,
    t.ticket_id AS ticket_id
FROM orders o
LEFT JOIN tickets t ON o.id = t.order_id
LEFT JOIN schedules s ON t.schedule_id = s.schedule_id
LEFT JOIN flights f ON f.flight_id = s.flight_id
WHERE o.email = '$email'

UNION ALL

SELECT
    o.id AS order_id,
    o.email,
    o.booking_date AS booking_date,
    f.flight_number,
    s.schedule_date,
    f.departure_time,
    f.arrival_time,
    t.passport,
    t.first_name,
    t.last_name,
    t.birth_date,
    t.seat_number,
    t.price,
    t.status,
    t.ticket_id AS ticket_id
FROM orders o
LEFT JOIN canceled_tickets t ON o.id = t.order_id
LEFT JOIN schedules s ON t.schedule_id = s.schedule_id
LEFT JOIN flights f ON f.flight_id = s.flight_id
WHERE o.email = '$email'

ORDER BY order_id DESC, ticket_id;
