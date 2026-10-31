--Countrywise Revenue

SELECT
    country,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
GROUP BY country
ORDER BY total_revenue DESC;