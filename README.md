# rox_challange

Este projeto propõe uma infraestrutura na nuvem para análise de dados da empresa fictícia Rollerbike que requisitou nossos serviços de engenharia de dados para otimizar esse processo. Nele vamos trabalhar os conceitos de:

- Modelagem conceitual dos dados
- Criação da infraestrutura necessária
- Criação de um processo de ETL para importar os dados para o banco de dados
- Desenvolvimento de SCRIPT para análise de dados
- Criação de um relatório em qualquer ferramenta de visualização de dados

Escolhemos a plataforma de serviços na nuvem AWS para criar a infraestrutura necessária por oferecer o melhor custo-benefício das soluções utilizadas. O banco de dados escolhido foi o MySQL 8.0.2 que é oferecido de graça durante 12 meses na Amazon RDS Free Tier. A cada mês são oferecidas 750 horas do Amazon RDS em uma instância Single-AZ db.t2.micro com 20GB de armazenamento e backup automático, o que atende perfeitamente as nossas necessidades.

IMAGE

Após uma análise inicial das tabelas a serem importadas para o banco e com base no diagrama de modelagem de dados enviado pelo cliente, foi decidida a criação das databases Production, Sales e Person com as respectivas tabelas, colunas, chaves primárias e chaves estrangeiras.

```
CREATE DATABASE IF NOT EXISTS Production
```
```
CREATE DATABASE IF NOT EXISTS Person
```
```
CREATE DATABASE IF NOT EXISTS Sales
```
```
CREATE TABLE IF NOT EXISTS Production.Product
(
ProductID INT(3) NOT NULL,
Name VARCHAR(32),
ProductNumber VARCHAR(10),
MakeFlag INT(1),
FinishedGoodsFlag INT(1),
Color VARCHAR(12),
SafetyStockLevel INT(4),
ReorderPoint INT(3),
StandardCost FLOAT(9),
ListPrice FLOAT(7),
Size VARCHAR(3),
SizeUnitMeasureCode VARCHAR(3),
WeightUnitMeasureCode VARCHAR(3),
Weight FLOAT(6),
DaysToManufacture INT(1),
ProductLine VARCHAR(3),
Class VARCHAR(3),
Style VARCHAR(3),
ProductSubcategoryID INT(4),
ProductModelID INT(5),
SellStartDate DATE,
SellEndDate DATE,
DiscontinuedDate DATE,
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (ProductID)
)
```
```
CREATE TABLE IF NOT EXISTS Person.Person
(
BusinessEntityID INT(5),
PersonType VARCHAR(2),
NameStyle INT(1),
Title VARCHAR(4),
FirstName VARCHAR(4),
MiddleName VARCHAR(16),
LastName VARCHAR(22),
Suffix VARCHAR(3),
EmailPromotion INT(1),
AdditionalContactInfo VARCHAR(1611),
Demographics VARCHAR(623),
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY(BusinessEntityID)
)
```
```
CREATE TABLE IF NOT EXISTS Sales.Customer
(
CustomerID INT(5) NOT NULL,
PersonID INT(7),
StoreID INT(6),
TerritoryID INT(2),
AccountNumber VARCHAR(10),
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (CustomerID)
FOREIGN KEY (PersonID) REFERENCES Person.Person(BusinessEntityID)
)
```
```
CREATE TABLE IF NOT EXISTS Sales.SalesOrderHeader
(
SalesOrderID INT(5),
RevisionNumber INT(1),
OrderDate DATE,
DueDate DATE,
ShipDate DATE,
Status INT(1),
OnlineOrderFlag INT(1),
SalesOrderNumber VARCHAR(7),
PurchaseOrderNumber VARCHAR(13),
AccountNumber VARCHAR(14),
CustomerID INT(5),
SalesPersonID INT(5),
TerritoryID INT(2),
BillToAddressID INT(5),
ShipToAddressID INT(5),
ShipMethodID INT(1),
CreditCardID INT(7),
CreditCardApprovalCode VARCHAR(15),
CurrencyRateID INT(7),
SubTotal FLOAT,
TaxAmt FLOAT,
Freight FLOAT,
TotalDue FLOAT,
Comment VARCHAR(3),
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (SalesOrderID),
FOREIGN KEY (CustomerID) REFERENCES Sales.Customer(CustomerID)
)
```
```
CREATE TABLE IF NOT EXISTS Sales.SpecialOfferProduct
(
SpecialOfferID INT(2) NOT NULL,
ProductID INT(3) NOT NULL,
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (SpecialOfferID, ProductID),
FOREIGN KEY (ProductID) REFERENCES Production.Product(ProductID)
)
```
```
CREATE TABLE IF NOT EXISTS Sales.SalesOrderDetail
(
SalesOrderID INT(5),
SalesOrderDetailID INT(6) ,
CarrierTrackingNumber VARCHAR(12),
OrderQty INT(2),
ProductID INT(3),
SpecialOfferID INT(2),
UnitPrice FLOAT,
UnitPriceDiscount FLOAT,
LineTotal FLOAT,
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (SalesOrderID, SalesOrderDetailID),
FOREIGN KEY (SalesOrderID) REFERENCES Sales.SalesOrderHeader(SalesOrderID),
FOREIGN KEY (SpecialOfferID) REFERENCES Sales.SpecialOfferProduct(SpecialOfferID),
FOREIGN KEY (ProductID) REFERENCES Production.Product(ProductID)
)
```

A modelagem do banco de dados ficou desenhada da seguinte forma depois da criação dos databases e tabelas.

IMAGE

Foi criado um bucket no Amazon S3 chamado rox-challange-landing-zone-us-east-1 para receber os seguintes arquivos que serão importados para as tabelas do banco:

- Sales.SpecialOfferProduct.csv
- Production.Product.csv
- Sales.SalesOrderHeader.csv
- Sales.Customer.csv
- Person.Person.csv
- Sales.SalesOrderDetail.csv

Foram criadas funções Lamba para cada arquivo, assim quando ele for criado dentro da sua respectiva pasta dentro do S3, a função será executada através de uma trigger do S3 e arquivo será lido, manipulado e ingerido na tabela correta.

IMAGE

O código executado pela função lambda é o seguinte:

```
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
    
    # Return json status
    return {
        'statusCode': 200,
        'body': json.dumps('Upload compleated')
    }
```

O layer é uma camada com os pacotes adicionais necessários para execução do nosso script Python. Os nossos pacotes serão copiados para a pasta X no bucket e pode ser selecionado na hora criação.
IMAGE

## Análise de dados

Com base na solução implantada responda aos seguintes questionamentos:

1. Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes

````
SELECT SalesOrderID as id, 
COUNT(*) AS qtd 
FROM Sales.SalesOrderDetail as sod
GROUP BY SalesOrderID
HAVING qtd >= 3
````

2. Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture).

```
SELECT * FROM(
  SELECT p.DaysToManufacture AS dtm,
         ROW_NUMBER() OVER(PARTITION BY p.DaysToManufacture ORDER BY sum(sod.OrderQty) DESC) as pos,
         p.Name as name,
         sum(sod.OrderQty) AS qtd
  FROM Sales.SpecialOfferProduct AS sop 
  INNER JOIN Production.Products AS p ON sop.ProductID = p.ProductID
  INNER JOIN Sales.SalesOrderDetail AS sod ON sop.SpecialOfferID = sod.SalesOrderDetailID
  GROUP BY name
  ) as by_pos
WHERE pos <= 3
```

3. Escreva uma query ligando as tabelas Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem de pedidos efetuados.

```
SELECT c.CustomerID as id, 
       CONCAT(p.FirstName, ' ', p.LastName) as name, 
       COUNT(*) AS qtd 
FROM Sales.SalesOrderHeader as soh
INNER JOIN	Sales.Customer as c ON soh.CustomerID = c.CustomerID
INNER JOIN Person.Person as p ON c.PersonID = p.BusinessEntityID 
GROUP BY c.PersonID
ORDER BY qtd DESC
```

4. Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e OrderDate.

```
SELECT sod.ProductID as id, 
       p.Name as name,
       sum(OrderQty) OVER(PARTITION BY sod.ProductID) AS qtd_id,
       soh.OrderDate,  
       sum(OrderQty) OVER(PARTITION BY soh.OrderDate) AS qtd_OrderDate
FROM Sales.SalesOrderDetail AS sod
INNER JOIN Sales.SalesOrderHeader as soh ON sod.SalesOrderID  = soh.SalesOrderID 
INNER JOIN Production.Products AS p ON sod.ProductID = p.ProductID 
GROUP BY sod.ProductID, soh.OrderDate
ORDER BY soh.OrderDate
```

5. Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabela Sales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido decrescente.

```
SELECT SalesOrderID, DATE(OrderDate), TotalDue 
FROM SalesOrderHeader AS soh 
WHERE DATE(OrderDate) BETWEEN DATE('2011-09-01') AND DATE('2011-09-30') AND TotalDue > 1.000
ORDER BY TotalDue DESC
```
