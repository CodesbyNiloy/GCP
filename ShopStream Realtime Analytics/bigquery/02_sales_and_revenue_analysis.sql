--Total order revenue

 SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
  AND order_id IS NOT NULL;

--Average Order Value(AOV)

  SELECT
    ROUND(
        SUM(total_amount) / COUNT(DISTINCT order_id), 2
    ) AS average_order_value
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
  AND order_id IS NOT NULL;

--Daily Revenue Trend

  SELECT
    DATE(event_timestamp) AS order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS daily_revenue
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
GROUP BY order_date
ORDER BY order_date;

--Monthly Revenue and Orders

SELECT
    FORMAT_DATE('%Y-%m', DATE(event_timestamp)) AS month,
    ROUND(SUM(total_amount), 2) AS monthly_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
GROUP BY month
ORDER BY month;