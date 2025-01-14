SELECT
        o.id AS order_id,
        o.email,
        o.booking_date,
        t.ticket_id,
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
        t.status
    FROM orders o
    LEFT JOIN tickets t ON o.id = t.order_id
    LEFT JOIN schedules s ON t.schedule_id = s.schedule_id
    LEFT JOIN flights f ON f.flight_id = s.flight_id
    WHERE t.status = 'booked'
    ORDER BY o.booking_date DESC, t.ticket_id;