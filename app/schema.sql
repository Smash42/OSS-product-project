DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO products (product_id, name, description, price) VALUES
(1, 'Packers Jersey', 'Green Bay Packers Home Jersey #10, Jordan Love', 15499),
(2, 'Mechanical Keyboard', 'RGB backlit mechanical keyboard with blue switches and durable keycaps.', 7999),
(3, 'Bose Headphones', 'On ear headphones with noise cancelling, hear through, and bluetooth technology', 21099),
(4, '4K Monitor', '27-inch 4K UHD monitor with ultra-thin bezels and HDR support.', 29999),
(5, 'Duke NFL Football', 'The official football of the NFL', 15999);