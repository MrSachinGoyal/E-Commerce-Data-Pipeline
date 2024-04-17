# E-Commerce-Data-Pipeline

## Overview
This project involves building a event-driven data ingestion and transformation pipeline focusing on e-commerce transactional data. This pipeline is using AWS services such as S3, Lambda, Glue, Redshift, and SNS, EventBridge to ingest, transform, validate, and insert data into Amazon Redshift for analytical purposes.

## Architecture
![AltText](https://github.com/MrSachinGoyal/E-Commerce-Data-Pipeline/blob/master/architecture.png)

## Prerequisites
- **Programming Language**: Python 3.11 or higher
- **Amazon Web Services (AWS) Account**:An active AWS account with the necessary permissions to create and manage services.
- **AWS Services**:
  - S3
  - Lambda
  - EventBridge Rule
  - Glue
  - Redshift
  - SNS
- Note: Ensure that appropriate IAM roles and permissions are assigned to access and manage the AWS services mentioned above.

## Workflow of the Project
- **Data Generation and Upload:**
   - Mock data generator(python script) produce daily e-commerce transaction files.
   - These files are uploaded to an S3 bucket.

- **Lambda Trigger for Glue Crawler:**
   - The S3 file upload event triggers a Lambda function specifically designed to initiate an AWS Glue crawler.

- **AWS Glue Crawler Execution:**
   - The Glue crawler automatically scans and catalogs the data stored in the designated S3 bucket, extracting metadata essential for subsequent analysis.

- **EventBridge Rule for Glue Job Trigger:**
   - An EventBridge rule is configured to detect changes in the state of the Glue crawler.
   - Upon detection of a state change, the EventBridge rule activates a Lambda function, which serves to invoke a Glue job responsible for data transformation.

- **Glue Job Transformation:**
   - The Glue job executes a series of transformations on the data, including:
     - **Join Operations:** Enriching transactional data by merging it with the dimensional data from dim_products and dim_customers tables, using product_id and customer_id as keys.
     - **Data Validation:** Implementing validation logic to filter out transactions containing invalid customer_id or product_id values, ensuring integrity.
     - **Additional Transformations:** Calculating the total transaction amount by multiplying quantity and price, and categorizing transactions into different classes based on their monetary value, such as "Small", "Medium", or "Large".
- **Data Loading into Redshift:**
   - Preloaded dimension tables for products and customers are created within Amazon Redshift.
   - Transformed data from the Glue job is inserted into the target fact table already created in Amazon Redshift, facilitating analytical queries.
    
- **EventBridge Rule for Job Status Notification:**
   - Another EventBridge rule is configured to monitor changes in the state of the AWS Glue job.
   - Upon state change detection, this rule activates an SNS topic, triggering notification regarding the job's status, whether it succeeded or failed.

- **SNS Notification:**
   - Users subscribed to the SNS topic receive email notifications detailing the outcome of the Glue job, ensuring stakeholders are promptly informed about the success or failure of the data transformation process.

## Key Learnings:
- **Event-Driven Architecture**: Implementing an event-driven data pipeline allows for efficient handling of data ingestion and transformation tasks, ensuring scalability and responsiveness to changes in data sources.
- **AWS Services Integration**: Utilizing various AWS services such as S3, Lambda, Glue, Redshift, EventBridge, and SNS enables seamless orchestration of data workflows, from ingestion to analytics, within a cloud environment.
- **Data Validation and Integrity**: Incorporating data validation logic within the Glue job ensures the integrity of the analytical dataset by filtering out invalid or inconsistent data, enhancing the reliability of insights derived from the data.
- **Dimensional Modeling**: Adopting dimensional modeling principles for structuring dimension and fact tables in Redshift facilitates efficient data loading and query performance, enabling faster analytics and reporting capabilities.
