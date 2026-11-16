import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(16)
customers=pd.DataFrame({'customer_id':np.arange(1,10001),'city':rng.choice(['Warszawa','Krakow','Gdansk'],10000)})
orders=pd.DataFrame({'order_id':np.arange(1,100001),'customer_id':rng.integers(1,10001,100000),'amount':rng.integers(10,2000,100000),'status':rng.choice(['paid','pending'],100000)})
customers.to_sql('customers',conn,index=False)
orders.to_sql('orders',conn,index=False)

query="""SELECT c.city,COUNT(*) AS orders_count,SUM(o.amount) AS revenue FROM orders o JOIN customers c ON o.customer_id=c.customer_id WHERE o.status='paid' AND o.amount>100 GROUP BY c.city HAVING COUNT(*)>100 ORDER BY revenue DESC"""
records=[];plans=[]
def measure(label):
    durations=[]
    for _ in range(3):
        start=time.perf_counter(); pd.read_sql_query(query,conn);durations.append(time.perf_counter()-start)
    duration=sum(durations)/3
    plan=pd.read_sql_query('EXPLAIN QUERY PLAN '+query,conn)
    plans.append((label,plan));records.append((label,duration))
measure('Bez indeksow')
for label,sql in [('idx_orders_customer','CREATE INDEX idx_orders_customer ON orders(customer_id)'),('idx_orders_status_amount','CREATE INDEX idx_orders_status_amount ON orders(status,amount)'),('idx_customers_id','CREATE INDEX idx_customers_id ON customers(customer_id)'),('idx_customers_city','CREATE INDEX idx_customers_city ON customers(city)')]:
    conn.execute(sql);measure(label)
baseline=records[0][1]
report=pd.DataFrame([{'indeks':label,'czas_ms':round(t*1000,3),'przyspieszenie':round(baseline/t,2)} for label,t in records])
print(report.to_string(index=False))
for label,plan in plans:print('\nPLAN:',label,'\n',plan.to_string(index=False))
for label,t in records:print(label,'█'*max(1,int(baseline/t)),f'{baseline/t:.2f}x')
changes=[(records[i-1][1]-records[i][1],records[i][0]) for i in range(1,len(records))]
print('Najwieksza poprawa po dodaniu:',max(changes)[1])

conn.close()
