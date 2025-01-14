INSERT INTO canceled_tickets (
    ticket_id,
    order_id,
    schedule_id,
    passport,
    first_name,
    last_name,
    birth_date,
    seat_number,
    price
)
SELECT
    ticket_id,
    order_id,
    schedule_id,
    passport,
    first_name,
    last_name,
    birth_date,
    seat_number,
    price
FROM tickets
WHERE ticket_id = '$ticket_id';
