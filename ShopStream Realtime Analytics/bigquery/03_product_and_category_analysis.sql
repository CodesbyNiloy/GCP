--Top 10 best-selling products

SELECT
    product_id,
    product_name,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS product_revenue
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
GROUP BY product_id, product_name
ORDER BY units_sold DESC
LIMIT 10;


--Top 10 highest revenue-generating categories

SELECT
    category_id,
    category_name,
    ROUND(SUM(total_amount), 2) AS category_revenue,
    SUM(quantity) AS units_sold
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
GROUP BY category_id, category_name
ORDER BY category_revenue DESC;

--Average product selling price

SELECT
    product_name,
    ROUND(AVG(unit_price), 2) AS average_price,
    MAX(unit_price) AS highest_price,
    MIN(unit_price) AS lowest_price
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
WHERE event_type = 'order_placed'
GROUP BY product_name
ORDER BY average_price DESC;