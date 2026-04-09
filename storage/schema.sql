-- Customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    customer_id INT,
    amount FLOAT,
    timestamp TIMESTAMP,
    fraud_flag BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);