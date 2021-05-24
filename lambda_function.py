# External libraries
import json
import csv
import boto3
import mysql.connector

def lambda_handler(event, context):

    # MySQL DB Credentials
    username = # your MySQL username
    password = # your MySQL password
    rds_endpoint = "rollerbike-mysql-db.croygqtawxvm.us-east-1.rds.amazonaws.com"
    port='3306'
    
    # AWS Credentials
    aws_access_key_id = #your AWS access key id
    aws_secret_access_key = #your AWS secret access key
    region_name = 'us-east-1'
    
    # Get Bucket, key, db, table variables from S3 trigger event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    db, table, _ = key.split('/')[-1].split('.')
    
    # Connection to S3 client
    s3_client = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    print('Connnected to S3')
    
    # Download file from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    csv_reader = response['Body'].read().decode('utf-8-sig').split('\n')
    
    print('Downloaded file from S3')
    
    # Create a list of rows with dict of values
    results = []
    for row in csv.DictReader(csv_reader, delimiter=';'):
        results.append(row.values())
    
    # Count many values per row
    var = ''
    for i in range(len(results[0])):
          var += '%s,'
    
    # Connect to MySQL
    connection = mysql.connector.connect(host=host,
                                         database=db,
                                         port=port,
                                         user=user,
                                         passwd=passwd)
    
    print('Connnected to MySQL')
    
    # Create query string
    query = f"insert into {table} values({var[:-1]})"
    
    # Insert values into table
    cursor = connection.cursor()
    cursor.executemany(mysql_insert, results)
    connection.commit()
    
    # Print results
    print(f'From {len(results)} records loaded')
    cur.execute(f"select count(*) from {table}")
    print ("Total records inserted: "+ str(cur.fetchall()[0]))
    conn.commit()
    
    # Return json status message
    return {
        'statusCode': 200,
        'body': json.dumps('Upload compleated')
    }