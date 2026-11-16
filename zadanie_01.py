import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
products = pd.DataFrame([(1,'Laptop','Elektronika',3500,10),(2,'Mysz','Akcesoria',45,100),(3,'Monitor','Elektronika',1200,20),(4,'Klawiatura','Akcesoria',150,40),(5,'Kabel','Akcesoria',25,200),(6,'Telefon','Elektronika',2400,15),(7,'Tablet','Elektronika',1800,12),(8,'Etui','Akcesoria',35,30),(9,'Drukarka','Elektronika',600,8),(10,'Sluchawki','Akcesoria',250,50)], columns=['product_id','name','category','price','stock'])
products.to_sql('products', conn, index=False)

print(pd.read_sql_query('''SELECT * FROM products''',conn))
print(pd.read_sql_query('''SELECT name, price FROM products''',conn))

conn.close()
