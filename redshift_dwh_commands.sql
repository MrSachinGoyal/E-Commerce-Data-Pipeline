-- create schema
CREATE SCHEMA IF NOT EXISTS ecommerce_transactions;

-- create tables and load data into the tables
CREATE TABLE IF NOT EXISTS ecommerce_transactions.dim_products (
    product_id VARCHAR(50) ENCODE lzo,
    product_name VARCHAR(50) ENCODE lzo,
    category VARCHAR(50) ENCODE lzo,
    price DECIMAL(10, 2) ENCODE delta,
    supplier_id VARCHAR(50) ENCODE lzo
);

CREATE TABLE IF NOT EXISTS ecommerce_transactions.dim_customers (
    customer_id VARCHAR(50) ENCODE lzo,
    first_name VARCHAR(50) ENCODE lzo,
    last_name VARCHAR(50) ENCODE lzo,
    email VARCHAR(255) ENCODE lzo,
    membership level (10) ENCODE lzo
);

INSERT INTO ecommerce_transactions.dim_customers (customer_id, first_name, last_name, email, membership_level) VALUES
('C12345', 'John', 'Doe', 'john.doe@example.com', 'Gold'),
('C12346', 'Alice', 'Smith', 'alice.smith@example.com', 'Silver'),
('C12347', 'Michael', 'Johnson', 'michael.johnson@example.com', 'Bronze'),
('C12348', 'Emily', 'Brown', 'emily.brown@example.com', 'Gold'),
('C12349', 'Daniel', 'Williams', 'daniel.williams@example.com', 'Silver'),
('C12350', 'Sarah', 'Jones', 'sarah.jones@example.com', 'Bronze'),
('C12351', 'David', 'Martinez', 'david.martinez@example.com', 'Gold'),
('C12352', 'Jessica', 'Garcia', 'jessica.garcia@example.com', 'Silver'),
('C12353', 'James', 'Lopez', 'james.lopez@example.com', 'Bronze'),
('C12354', 'Emma', 'Hernandez', 'emma.hernandez@example.com', 'Gold');

INSERT INTO ecommerce_transactions.dim_products (product_id, product_name, category, price, supplier_id) VALUES
('P12345', 'Widget A', 'Gadgets', 29.99, 'S123'),
('P12346', 'Widget B', 'Electronics', 49.99, 'S124'),
('P12347', 'Widget C', 'Tools', 39.99, 'S125'),
('P12348', 'Widget D', 'Home Appliances', 99.99, 'S126'),
('P12349', 'Widget E', 'Gadgets', 19.99, 'S127'),
('P12350', 'Widget F', 'Electronics', 59.99, 'S128'),
('P12351', 'Widget G', 'Tools', 24.99, 'S129'),
('P12352', 'Widget H', 'Home Appliances', 34.99, 'S130'),
('P12353', 'Widget I', 'Gadgets', 79.99, 'S131'),
('P12354', 'Widget J', 'Electronics', 14.99, 'S132'),
('P12355', 'Widget K', 'Tools', 44.99, 'S133'),
('P12356', 'Widget L', 'Home Appliances', 69.99, 'S134'),
('P12357', 'Widget M', 'Gadgets', 29.99, 'S135'),
('P12358', 'Widget N', 'Electronics', 129.99, 'S136'),
('P12359', 'Widget O', 'Tools', 34.99, 'S137'),
('P12360', 'Widget P', 'Home Appliances', 79.99, 'S138'),
('P12361', 'Widget Q', 'Gadgets', 19.99, 'S139'),
('P12362', 'Widget R', 'Electronics', 24.99, 'S140'),
('P12363', 'Widget S', 'Tools', 89.99, 'S141'),
('P12364', 'Widget T', 'Home Appliances', 9.99, 'S142');

CREATE TABLE IF NOT EXISTS ecommerce_transactions.fact_trnx_data (
    transaction_id VARCHAR(255) ENCODE lzo,
    customer_id VARCHAR(255) ENCODE lzo,
    customer_email VARCHAR(255) ENCODE lzo
    product_id VARCHAR(255) ENCODE lzo,
    product_name VARCHAR(255) ENCODE lzo,
    quantity INT ENCODE lzo,     
    supplier_id VARCHAR(255) ENCODE lzo,
    price DECIMAL(10, 2) ENCODE lzo,  
    transaction_date DATE ENCODE bytedict, 
    transaction_type VARCHAR(255) ENCODE lzo,
    payment_type VARCHAR(255) ENCODE lzo,
    status VARCHAR(55) ENCODE lzo
)
DISTSTYLE KEY
DISTKEY (payment_type)
SORTKEY (transaction_id);
