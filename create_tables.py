# External libraries
import mysql.connector


# MySQL DB Credentials
username = # your MySQL username
password = # your MySQL password
rds_endpoint = "rollerbike-mysql-db.croygqtawxvm.us-east-1.rds.amazonaws.com"
port='3306'


# Create database Person from SQL script file
with open('scripts/create_db_Person.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created database Person')


# Create database Production from SQL script file
with open('scripts/create_db_Production.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created database Production')


# Create database Sales from SQL script file
with open('scripts/create_db_Sales.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created database Sales')


# Create table Product from SQL script file
with open('scripts/create_table_Product.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created table Product')


# Create table Person from SQL script file
with open('scripts/create_table_Person.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created table Person')


# Create table Customer from SQL script file
with open('scripts/create_table_Customer.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created table Customer')


# Create table SalesOrderHeader from SQL script file
with open('scripts/create_table_SalesOrderHeader.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created table SalesOrderHeader')


# Create table SpecialOfferProduct from SQL script file
with open('scripts/create_table_SpecialOfferProduct.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created table SpecialOfferProduct')


# Create table SalesOrderDetail from SQL script file
with open('scripts/create_table_Sales.SalesOrderDetail.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Created table Sales.SalesOrderDetail')














