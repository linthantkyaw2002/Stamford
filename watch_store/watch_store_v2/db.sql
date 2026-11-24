CREATE DATABASE IF NOT EXISTS watch_store;
USE watch_store;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  brand VARCHAR(60) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  image VARCHAR(255) NOT NULL
);

INSERT INTO products (name, brand, price, image) VALUES
('Aventus Steel Chrono', 'Rolex', 1299.00, 'images/watch1.png'),
('Midnight Diver', 'Omega', 999.00, 'images/watch2.png'),
('Heritage Classic', 'Tissot', 349.00, 'images/watch3.png'),
('Carbon GMT Pro', 'Tag Heuer', 1899.00, 'images/watch4.png'),
('Sakura Limited', 'Seiko', 449.00, 'images/watch5.png'),
('Monaco Racing', 'Tag Heuer', 2199.00, 'images/watch6.png'),
('Oceanic 300M', 'Omega', 1199.00, 'images/watch7.png'),
('Luxe Minimal Leather', 'Tissot', 289.00, 'images/watch8.png'),
('Shadow Skeleton', 'Fossil', 259.00, 'images/watch9.png'),
('Prestige Day-Date', 'Rolex', 8999.00, 'images/watch10.png');

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL,
  address TEXT NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);
