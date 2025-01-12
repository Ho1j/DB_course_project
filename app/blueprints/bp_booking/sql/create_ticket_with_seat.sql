INSERT INTO tickets (
    order_id,
    schedule_id,
    passport,
    first_name,
    last_name,
    birth_date,
    seat_number,
    price,
    status
)
VALUES (
    '$order_id',
    '$schedule_id',
    '$passport',
    '$first_name',
    '$last_name',
    '$birth_date',
    '$seat_number',
    (SELECT f.ticket_price
     FROM flights f
     JOIN schedules s ON f.flight_id = s.flight_id
     WHERE s.schedule_id = '$schedule_id'),
    '$status'
);
