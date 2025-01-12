SELECT
    schedule_id,
    f.flight_number,
    dep_airport.airport_name AS departure_airport,
    dep_airport.city AS departure_city,
    dep_airport.country AS departure_country,
    s.schedule_date AS departure_date,
    f.departure_time AS departure_time,
    arr_airport.airport_name AS arrival_airport,
    arr_airport.city AS arrival_city,
    arr_airport.country AS arrival_country,
    f.ticket_price,
    f.arrival_time AS arrival_time
FROM
    flights f
JOIN
    schedules s ON f.flight_id = s.flight_id
JOIN
    airports dep_airport ON f.departure_airport_id = dep_airport.airport_id
JOIN
    airports arr_airport ON f.arrival_airport_id = arr_airport.airport_id
WHERE
    dep_airport.city = '$departure_city'
    AND arr_airport.city = '$arrival_city'  -- Город прилёта
    AND s.schedule_date = '$flight_date'; -- Дата рейса
