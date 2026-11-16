import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
customers = pd.DataFrame([(1,'Jan','Warszawa'),(2,'Anna','Krakow'),(3,'Piotr','Gdansk'),(4,'Maria','Wroclaw')],columns=['customer_id','name','city'])
orders = pd.DataFrame([(101,1,250.),(102,1,500.),(103,2,120.),(104,3,300.)],columns=['order_id','customer_id','amount'])
customers.to_sql('customers',conn,index=False)
orders.to_sql('orders',conn,index=False)

print(pd.read_sql_query('''SELECT customer_id,COUNT(*) AS liczba,SUM(amount) AS suma,ROUND(AVG(amount),2) AS srednia FROM orders GROUP BY customer_id''',conn))

conn.close()
