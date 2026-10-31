--Total Events

SELECT
    COUNT(*) AS total_events
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`;


--Total Customers and Sessions

SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT session_id) AS total_sessions
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`;

--Total Events by Type

SELECT
    event_type,
    COUNT(*) AS event_count
FROM `shopstream-realtime-analytics.shopstream_realtime.events_raw`
GROUP BY event_type
ORDER BY event_count DESC;