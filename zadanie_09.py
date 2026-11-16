import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
customers = pd.DataFrame([(1,'Jan','Warszawa'),(2,'Anna','Krakow'),(3,'Piotr','Gdansk'),(4,'Maria','Wroclaw')],columns=['customer_id','name','city'])
orders = pd.DataFrame([(101,1,250.),(102,1,500.),(103,2,120.),(104,3,300.)],columns=['order_id','customer_id','amount'])
customers.to_sql('customers',conn,index=False)
orders.to_sql('orders',conn,index=False)
items=pd.DataFrame([(101,'Laptop',1,3500),(101,'Mysz',2,50),(102,'Monitor',1,1200),(103,'Kabel',3,25),(104,'Tablet',1,1800)],columns=['order_id','product','quantity','price'])
items.to_sql('order_items',conn,index=False)
conn.execute('ALTER TABLE orders ADD COLUMN order_date TEXT')
conn.execute("UPDATE orders SET order_date='2024-01-15'")

print(pd.read_sql_query('''SELECT c.name,o.order_date,i.product,i.price,i.quantity FROM customers c JOIN orders o ON c.customer_id=o.customer_id JOIN order_items i ON o.order_id=i.order_id''',conn))
print(pd.read_sql_query('''SELECT o.order_id,SUM(i.quantity*i.price) AS wartosc FROM orders o JOIN order_items i ON o.order_id=i.order_id GROUP BY o.order_id ORDER BY wartosc DESC LIMIT 10''',conn))

conn.close()
