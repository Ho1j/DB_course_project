SELECT
    DATE_FORMAT(period, '%Y-%m') AS report_month,
    COUNT(*) AS report_count
FROM
    $report_type
GROUP BY
    report_month
ORDER BY
    report_month DESC;
