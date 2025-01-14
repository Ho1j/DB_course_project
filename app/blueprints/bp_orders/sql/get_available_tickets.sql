SELECT
    s.available_tickets,
    s.schedule_id
FROM
    schedules s
JOIN
    flights f ON s.flight_id = f.flight_id
WHERE
    f.flight_number = '$flight_number'
    AND s.schedule_date = '$schedule_date';
