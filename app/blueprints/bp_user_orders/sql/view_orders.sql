SELECT
        o.id AS order_id,
        o.booking_date,
        t.ticket_id,
        t.schedule_id,
        t.passport,
        t.first_name,
        t.last_name,
        t.birth_date,
        t.seat_number,
        t.price,
        t.status
    FROM orders o
    LEFT JOIN tickets t ON o.id = t.order_id
    WHERE o.user_id = '$user_id'
    ORDER BY o.booking_date DESC, t.ticket_id;