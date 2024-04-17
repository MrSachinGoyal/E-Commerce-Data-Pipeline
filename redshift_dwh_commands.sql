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

COPY ecommerce_transactions.dim_products
FROM 's3://bucket_name/dims/products.csv'
IAM_ROLE 'mention role associated with redshift'
DELIMITER ','
IGNOREHEADER 1
FORMAT CSV
REGION 'us-east-1';

COPY ecommerce_transactions.dim_customers
FROM 's3://bucket_name/dims/customers.csv'
IAM_ROLE 'mention role associated with redshift'
DELIMITER ','
IGNOREHEADER 1
FORMAT CSV
REGION 'us-east-1';

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
