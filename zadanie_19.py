import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(19)
sales=pd.DataFrame({'date':np.repeat(pd.date_range('2024-01-01',periods=12,freq='MS').strftime('%Y-%m'),20),'category':rng.choice(['A','B'],240),'revenue':rng.integers(50,1500,240)})
sales.to_sql('sales',conn,index=False)

query="""SELECT date AS month,SUM(CASE WHEN category='A' THEN revenue ELSE 0 END) AS cat_A,SUM(CASE WHEN category='B' THEN revenue ELSE 0 END) AS cat_B FROM sales GROUP BY date ORDER BY date"""
df=pd.read_sql_query(query,conn);print(df.to_string(index=False))
for row in df.itertuples():
    print(row.month,'A:','█'*int(row.cat_A/500),f'{row.cat_A} PLN')
    print('       B:','█'*int(row.cat_B/500),f'{row.cat_B} PLN')

conn.close()
