DROP TABLE IF EXISTS role_permissions;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;


CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name TEXT NOT NULL,
    is_critic INTEGER NOT NULL DEFAULT 0 CHECK(is_critic IN (0,1)),
    email TEXT NOT NULL,
    passhash TEXT NOT NULL,
    role INTEGER DEFAULT 2
);

CREATE TABLE roles (
    roleid INTEGER PRIMARY KEY, 
    name TEXT NOT NULL,
    description TEXT NOT NULL
);


CREATE TABLE permissions (
    permissionid INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    description TEXT NOT NULL
);

CREATE TABLE role_permissions (
    roleid INTEGER,
    permissionid INTEGER,
    PRIMARY KEY (roleid, permissionid)
);

INSERT INTO roles (roleid, name, description) VALUES
(1, 'user', 'Users have no permissions'),
(2, 'moderator', 'Moderator can edit products');

INSERT INTO permissions(permissionid, name, description) VALUES
(1, 'product.edit', 'Can edit products'),
(2, 'product.delete', 'Can delete products'),
(3, 'product.add', 'Can add new products');

INSERT INTO role_permissions(roleid, permissionid) VALUES
(2, 1), (2, 2), (2, 3);

INSERT INTO products (product_id, name, description, price) VALUES
(1, 'Packers Jersey', 'Green Bay Packers Home Jersey #10, Jordan Love', 15499),
(2, 'Mechanical Keyboard', 'RGB backlit mechanical keyboard with blue switches and durable keycaps.', 7999),
(3, 'Bose Headphones', 'On ear headphones with noise cancelling, hear through, and bluetooth technology', 21099),
(4, '4K Monitor', '27-inch 4K UHD monitor with ultra-thin bezels and HDR support.', 29999),
(5, 'Duke NFL Football', 'The official football of the NFL', 15999);