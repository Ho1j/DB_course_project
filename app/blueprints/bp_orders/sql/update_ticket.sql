UPDATE tickets
SET
    first_name = '$first_name',
    last_name = '$last_name',
    passport = '$passport',
    birth_date = '$birth_date',
    seat_number = '$seat_number',
    price = '$price',
    status = '$status'
WHERE ticket_id = '$ticket_id';
