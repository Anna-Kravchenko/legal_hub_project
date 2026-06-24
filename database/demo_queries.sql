SELECT 
    clients.name AS "Клієнт",
    services.name AS "Послуга",
    l1.name || ' → ' || l2.name AS "Мови",
    orders.status AS "Статус",
    orders.created_at AS "Дата"
FROM orders
JOIN clients ON orders.client_id = clients.id
JOIN services ON orders.service_id = services.id
JOIN languages l1 ON orders.source_language_id = l1.id
JOIN languages l2 ON orders.target_language_id = l2.id;