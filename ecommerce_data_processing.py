import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame
import re


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node data source customers
datasourcecustomers_node1713102851374 = glueContext.create_dynamic_frame.from_catalog(
    database="ecomm-data-metadata-db",
    table_name="customers_csv",
    transformation_ctx="datasourcecustomers_node1713102851374",
)

# Script generated for node data source products
datasourceproducts_node1713103323322 = glueContext.create_dynamic_frame.from_catalog(
    database="ecomm-data-metadata-db",
    table_name="products_csv",
    transformation_ctx="datasourceproducts_node1713103323322",
)

# Script generated for node transactions data source
transactionsdatasource_node1713102493949 = (
    glueContext.create_dynamic_frame.from_catalog(
        database="ecomm-data-metadata-db",
        table_name="transactions",
        transformation_ctx="transactionsdatasource_node1713102493949",
    )
)

# Script generated for node derive column - transaction_type
SqlQuery306 = """
select *,
case when price*quantity <= 100 THEN 'low'
when price*quantity > 100 and price*quantity <= 500 then 'medium'
else 'high' end as transaction_type
from myDataSource
"""
derivecolumntransaction_type_node1713102564394 = sparkSqlQuery(
    glueContext,
    query=SqlQuery306,
    mapping={"myDataSource": transactionsdatasource_node1713102493949},
    transformation_ctx="derivecolumntransaction_type_node1713102564394",
)

# Script generated for node Join between tranx_data and customers
Joinbetweentranx_dataandcustomers_node1713102925567 = Join.apply(
    frame1=derivecolumntransaction_type_node1713102564394,
    frame2=datasourcecustomers_node1713102851374,
    keys1=["customer_id"],
    keys2=["customer_id"],
    transformation_ctx="Joinbetweentranx_dataandcustomers_node1713102925567",
)

# Script generated for node Join between products and tranx_customer
Joinbetweenproductsandtranx_customer_node1713103363392 = Join.apply(
    frame1=datasourceproducts_node1713103323322,
    frame2=Joinbetweentranx_dataandcustomers_node1713102925567,
    keys1=["product_id"],
    keys2=["product_id"],
    transformation_ctx="Joinbetweenproductsandtranx_customer_node1713103363392",
)

# Script generated for node Select Fields
SelectFields_node1713106035505 = SelectFields.apply(
    frame=Joinbetweenproductsandtranx_customer_node1713103363392,
    paths=[
        "customer_id",
        "transaction_id",
        "email",
        "product_id",
        "product_name",
        "supplier_id",
        "quantity",
        "price",
        "transaction_date",
        "transaction_type",
        "status",
        "payment_type",
    ],
    transformation_ctx="SelectFields_node1713106035505",
)

# Script generated for node Filter
Filter_node1713106870461 = Filter.apply(
    frame=SelectFields_node1713106035505,
    f=lambda row: (
        bool(re.match("^C[\d]+", row["customer_id"]))
        and bool(re.match("^P[\d]+", row["product_id"]))
    ),
    transformation_ctx="Filter_node1713106870461",
)

# Script generated for node Rename Field
RenameField_node1713107785991 = RenameField.apply(
    frame=Filter_node1713106870461,
    old_name="email",
    new_name="customer_email",
    transformation_ctx="RenameField_node1713107785991",
)

# Script generated for node Change Schema
ChangeSchema_node1713107958055 = ApplyMapping.apply(
    frame=RenameField_node1713107785991,
    mappings=[
        ("product_id", "string", "product_id", "string"),
        ("product_name", "string", "product_name", "string"),
        ("price", "double", "price", "decimal"),
        ("supplier_id", "string", "supplier_id", "string"),
        ("transaction_id", "string", "transaction_id", "string"),
        ("customer_id", "string", "customer_id", "string"),
        ("quantity", "long", "quantity", "int"),
        ("transaction_date", "string", "transaction_date", "date"),
        ("payment_type", "string", "payment_type", "string"),
        ("status", "string", "status", "string"),
        ("transaction_type", "string", "transaction_type", "string"),
        ("customer_email", "string", "customer_email", "string"),
    ],
    transformation_ctx="ChangeSchema_node1713107958055",
)

# Script generated for node fact tranx table - target
facttranxtabletarget_node1713108043719 = glueContext.write_dynamic_frame.from_catalog(
    frame=ChangeSchema_node1713107958055,
    database="ecomm-data-metadata-db",
    table_name="dev_ecommerce_transactions_fact_trnx_data",
    redshift_tmp_dir=args["TempDir"],
    transformation_ctx="facttranxtabletarget_node1713108043719",
)

job.commit()
