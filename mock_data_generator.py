import pandas as pd
import boto3
import datetime
from datetime import timedelta
import random
import string

# Read customer and product data from CSV files
customer_df = pd.read_csv(r'customers.csv')
product_df = pd.read_csv(r'products.csv')

# Extract customer IDs, product IDs, and product prices
customer_ids = customer_df['customer_id'].to_list()
product_ids = product_df['product_id'].to_list()
product_prices = product_df['price'].to_list()
product_price_list = list(zip(product_ids, product_prices))

# Define payment types
payment_types = ["Cash on Delivery", "Credit Card", "Debit Card"]

# Function to generate transaction data
def generate_transaction_data():
    transaction_id = f"TXN{''.join(random.choices(string.digits, k=8))}"
    customer_id = random.choice(customer_ids)
    product_id, price = random.choice(product_price_list)
    quantity = random.randint(1, 10)
    transaction_date = datetime.datetime.now().date() + timedelta(days=4)
    payment_type = random.choice(payment_types)
    status = 'Completed'

    return {
        "transaction_id" : transaction_id,
        "customer_id" : customer_id,
        "product_id" : product_id,
        "quantity" : quantity,
        "price" : price,
        "transaction_date" : transaction_date,
        "payment_type" : payment_type,
        'status' : status
    }

data = []
current_date = datetime.datetime.now().date() + timedelta(days=4)

# Generate transaction data for 100 transactions
for i in range(100):
    transaction = generate_transaction_data()
    data.append(transaction)

# Create DataFrame from generated data
transaction_df = pd.DataFrame(data, columns=['transaction_id', 'customer_id', 'product_id', 'quantity', 'price', 'transaction_date', 'payment_type', 'status'])

# Save DataFrame to CSV file
transaction_df.to_csv(f"C:/Users/User/Desktop/aws_bootcamp/transaction_{current_date}.csv", index=False)

# Function to upload file to S3 bucket
def upload_to_s3():
    year = current_date.year
    month = current_date.month
    day = current_date.day

    s3_client = boto3.client('s3')
    bucket_name = 'ecommerce-data-transactions'
    file_name = f'transaction_{current_date}.csv'
    file_path = f"transactions/year={year}/month={month}/day={day}/{file_name}"

    # Upload file to S3 bucket
    s3_client.upload_file(f'{file_name}', bucket_name, file_path)

    return f'File Upload to S3 {bucket_name} successfully'

# Upload file to S3 bucket and print result
result = upload_to_s3()
print(result)
