SELECT
    *
FROM
    flights_revenue_report
WHERE
    period = '$report_month_full'
ORDER BY
    total_revenue DESC;
