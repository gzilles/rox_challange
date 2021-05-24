# External libraries
import boto3

# AWS Credentials
bucket = 'rox-challange-landing-zone-us-east-1'
region_name = 'us-east-1'
aws_access_key_id = #your AWS access key id
aws_secret_access_key = #your AWS secret access key

# Connection to S3 resource
s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
print('Connected to S3')

# Create bucket to upload files
if s3.Bucket(bucket ) in s3.buckets.all():
   s3.meta.client.create_bucket(Bucket=bucket )
   print(f'Bucket {bucket} created')
else:
   print(f'Bucket {bucket} is already created')


# Upload aws-lambda-layer-python file
s3.meta.client.upload_file('aws-lambda-layer-python/python.zip', bucket, 'Tools/aws-lambda-layer-python/python.zip')
print('File uploaded to Tools/aws-lambda-layer-python/python.zip') 

# Upload Person.Person.csv file
s3.meta.client.upload_file('csv_files/Person.Person.csv', bucket, 'Raw/Person/Person/Person.Person.csv')
print('File uploaded to Raw/Person/Person/Person.Person.csv')

# Upload Production.Product.csv file
s3.meta.client.upload_file('csv_files/Production.Product.csv', 'rox-challange-landing-zone-us-east-1', 'Raw/Production/Product/Production.Product.csv')
print('File uploaded to Raw/Production/Product/Production.Product.csv')

# Upload Sales.Customer.csv file
s3.meta.client.upload_file('csv_files/Sales.Customer.csv', 'rox-challange-landing-zone-us-east-1', 'Raw/Sales/Customer/Sales.Customer.csv')
print('File uploaded to Raw/Sales/Customer/Sales.Customer.csv')

# Upload Sales.SpecialOfferProduct.csv file
s3.meta.client.upload_file('csv_files/Sales.SpecialOfferProduct.csv', 'rox-challange-landing-zone-us-east-1', 'Raw/Sales/SpecialOfferProduct/Sales.SpecialOfferProduct.csv')
print('File uploaded to Raw/Sales/SpecialOfferProduct/Sales.SpecialOfferProduct.csv')

# Upload Sales.SalesOrderHeader.csv file
s3.meta.client.upload_file('csv_files/Sales.SalesOrderHeader.csv', 'rox-challange-landing-zone-us-east-1', 'Raw/Sales/SalesOrderHeader/Sales.SalesOrderHeader.csv')
print('File uploaded to Raw/Sales/SalesOrderHeader/Sales.SalesOrderHeader.csv')

# Upload Sales.SalesOrderDetail.csv file
s3.meta.client.upload_file('csv_files/Sales.SalesOrderDetail.csv', 'rox-challange-landing-zone-us-east-1', 'Raw/Sales/SalesOrderDetail/Sales.SalesOrderDetail.csv')
print('File uploaded to Raw/Sales/SalesOrderDetail/Sales.SalesOrderDetail.csv')

