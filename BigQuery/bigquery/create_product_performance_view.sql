CREATE OR REPLACE VIEW
  `project-840baaf4-213b-416b-9ef.Ecommerce_Data.mart_product_performance`
AS
SELECT
    p.id AS product_id,
    p.title AS product_name,
    p.category,
    p.price AS listed_price,
    p.rating,
    p.stock,
    COALESCE(SUM(c.quantity), 0) AS units_in_carts,
    COUNT(DISTINCT c.cart_id) AS number_of_carts,
    ROUND(COALESCE(SUM(c.total), 0), 2) AS sample_cart_value,
    ROUND(COALESCE(SUM(c.discounted_total), 0), 2)
        AS discounted_cart_value,
    ROUND(COALESCE(SUM(c.total - c.discounted_total), 0), 2)
        AS estimated_cart_discount
FROM `project-840baaf4-213b-416b-9ef.Ecommerce_Data.raw_products` AS p
LEFT JOIN `project-840baaf4-213b-416b-9ef.Ecommerce_Data.raw_cart_items` AS c
    ON p.id = c.product_id
GROUP BY
    p.id, p.title, p.category, p.price, p.rating, p.stock;