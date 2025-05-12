CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE Manager (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fio VARCHAR(100) NOT NULL,
    login VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    contacts TEXT,
    role VARCHAR(50) NOT NULL,
    bonus NUMERIC
);

CREATE TABLE Client (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fio VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE
);

CREATE TABLE Interaction (
    manager_id UUID REFERENCES Manager(id) ON DELETE CASCADE,
    client_id UUID REFERENCES Client(id) ON DELETE CASCADE,
    PRIMARY KEY (manager_id, client_id)
);

CREATE TABLE InteractionHistory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES Client(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    type VARCHAR(50),
    details TEXT
);

CREATE TABLE Order_ (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES Client(id) ON DELETE SET NULL,
    creation_date DATE NOT NULL,
    status VARCHAR(50),
    total NUMERIC
);

CREATE TABLE OrderHistory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES Order_(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total NUMERIC
);

CREATE TABLE Product (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    price NUMERIC NOT NULL,
    stock INT
);

CREATE TABLE Category (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL
);

CREATE TABLE ProductCategory (
    product_id UUID REFERENCES Product(id) ON DELETE CASCADE,
    category_id UUID REFERENCES Category(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);

CREATE TABLE OrderProduct (
    order_id UUID REFERENCES Order_(id) ON DELETE CASCADE,
    product_id UUID REFERENCES Product(id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);
