import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(17)
customers=pd.DataFrame({'customer_id':range(1,101),'name':[f'Klient_{i}' for i in range(1,101)]})
orders=[]
for cid in customers.customer_id:
    for _ in range(int(rng.integers(0,13))):
        orders.append((cid,(pd.Timestamp('2024-12-31')-pd.to_timedelta(int(rng.integers(0,365)),unit='D')).strftime('%Y-%m-%d'),float(rng.integers(20,2000))))
customers.to_sql('customers',conn,index=False)
pd.DataFrame(orders,columns=['customer_id','order_date','amount']).to_sql('orders',conn,index=False)

query="""WITH rfm AS (SELECT c.customer_id,ROUND(julianday('2024-12-31')-julianday(MAX(o.order_date)),0) AS recency,COUNT(o.order_date) AS frequency,COALESCE(SUM(o.amount),0) AS monetary FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id GROUP BY c.customer_id), segmented AS (SELECT *,CASE WHEN frequency>=7 AND recency<=90 AND monetary>=4000 THEN 'VIP' WHEN frequency=0 OR recency>270 THEN 'Lost' WHEN recency>150 THEN 'At-risk' ELSE 'Regular' END AS segment FROM rfm) SELECT segment,COUNT(*) AS customers,ROUND(AVG(recency),2) AS avg_R,ROUND(AVG(frequency),2) AS avg_F,ROUND(AVG(monetary),2) AS avg_M FROM segmented GROUP BY segment ORDER BY customers DESC"""
df=pd.read_sql_query(query,conn)
print(df.to_string(index=False))
for row in df.itertuples():print(row.segment,'█'*row.customers,row.customers)

conn.close()
