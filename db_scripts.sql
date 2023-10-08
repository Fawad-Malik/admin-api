-- Insert data into 'categories' table
INSERT INTO categories (category_id, category_name)
VALUES
    (1, 'Electronics'),
    (2, 'Clothing'),
    (3, 'Home and Garden');

-- Insert data into 'products' table
INSERT INTO products (product_id, product_name, product_description, product_price, category_id)
VALUES
    (1, 'Smartphone', 'High-end smartphone', 799.99, 1),
    (2, 'Laptop', 'Powerful laptop', 1299.99, 1),
    (3, 'T-shirt', 'Cotton T-shirt', 19.99, 2),
    (4, 'Jeans', 'Slim-fit jeans', 39.99, 2),
    (5, 'Garden Hose', '50 ft garden hose', 29.99, 3);

-- Insert data into 'inventories' table
INSERT INTO inventories (inventory_id, product_id, product_quantity)
VALUES
    (1, 1, 100),
    (2, 2, 50),
    (3, 3, 200),
    (4, 4, 75),
    (5, 5, 150);

-- Insert data into 'sales' table
INSERT INTO sales (sale_id, sale_price, sale_time, sale_date)
VALUES
    (1, 999.99, '2023-10-06 10:00:00', '2023-10-06'),
    (2, 1499.99, '2023-10-07 14:30:00', '2023-10-07'),
    (3, 29.99, '2023-10-08 09:15:00', '2023-10-08');

-- Insert data into 'sale_products' table
INSERT INTO sale_products (product_id, sale_id, quantity)
VALUES
    (1, 1, 2),
    (2, 1, 1),
    (3, 2, 5),
    (4, 3, 3),
    (5, 3, 10);

-- Insert data into 'inventory_logs' table
INSERT INTO inventory_logs (id, inventory_id, previous_quantity, new_quantity, updated_on)
VALUES
    (1, 1, 100, 90, '2023-10-06 10:30:00'),
    (2, 2, 50, 45, '2023-10-07 15:00:00'),
    (3, 3, 200, 195, '2023-10-08 09:30:00'),
    (4, 4, 75, 73, '2023-10-09 11:45:00'),
    (5, 5, 150, 140, '2023-10-09 14:20:00');