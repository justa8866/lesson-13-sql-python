import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(14)
customers=pd.DataFrame({'customer_id':range(1,101),'registration_date':(pd.Timestamp('2024-01-01')+pd.to_timedelta(rng.integers(0,180,100),unit='D')).strftime('%Y-%m-%d')})
orders=[]
for cid,reg in customers.itertuples(index=False):
    for _ in range(int(rng.integers(0,8))):
        orders.append((cid,(pd.Timestamp(reg)+pd.to_timedelta(int(rng.integers(0,180)),unit='D')).strftime('%Y-%m-%d'),float(rng.integers(30,1000))))
customers.to_sql('customers',conn,index=False)
pd.DataFrame(orders,columns=['customer_id','order_date','amount']).to_sql('orders',conn,index=False)

cohorts="""SELECT strftime('%Y-%m',c.registration_date) AS cohort,COUNT(DISTINCT c.customer_id) AS customers,COUNT(o.customer_id) AS orders,ROUND(COALESCE(SUM(o.amount),0),2) AS revenue,ROUND(COALESCE(SUM(o.amount),0)/COUNT(DISTINCT c.customer_id),2) AS ltv FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id GROUP BY cohort ORDER BY cohort"""
print(pd.read_sql_query(cohorts,conn).to_string(index=False))
query="""SELECT strftime('%Y-%m',c.registration_date) AS cohort, (CAST(strftime('%Y',o.order_date) AS INTEGER)-CAST(strftime('%Y',c.registration_date) AS INTEGER))*12+CAST(strftime('%m',o.order_date) AS INTEGER)-CAST(strftime('%m',c.registration_date) AS INTEGER) AS month_offset, SUM(o.amount) AS revenue FROM customers c JOIN orders o ON c.customer_id=o.customer_id GROUP BY cohort,month_offset"""
df=pd.read_sql_query(query,conn)
pivot=df.pivot(index='cohort',columns='month_offset',values='revenue').fillna(0)
print('\nPivot kohort:');print(pivot.to_string())
positive=pivot.to_numpy(); positive=positive[positive>0]
thresholds=np.quantile(positive,[.25,.5,.75]) if len(positive) else [0,0,0]
print('\nHeatmapa (., ░, ▒, ▓, █):')
for cohort,row in pivot.iterrows():
    symbols=['.' if v==0 else '░' if v<=thresholds[0] else '▒' if v<=thresholds[1] else '▓' if v<=thresholds[2] else '█' for v in row]
    print(cohort,' '.join(symbols))

conn.close()
