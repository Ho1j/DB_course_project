SELECT
    *
FROM
    cashiers_sales_report
WHERE
    period = '$report_month_full'
ORDER BY
    total_sales DESC;
