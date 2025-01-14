SELECT
    *
FROM
    destinations_report
WHERE
    period = '$report_month_full'
ORDER BY
    total_flights DESC;
