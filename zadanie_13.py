import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(13)
dates=pd.to_datetime('2024-01-01')+pd.to_timedelta(rng.integers(0,366,1000),unit='D')
sales=pd.DataFrame({'sale_id':range(1,1001),'product':rng.choice(['Laptop','Mysz','Monitor'],1000),'category':rng.choice(['Elektronika','Akcesoria'],1000),'sale_date':dates.strftime('%Y-%m-%d'),'revenue':rng.integers(50,2001,1000)})
sales.to_sql('sales',conn,index=False)

monthly="SELECT strftime('%Y-%m',sale_date) AS month, SUM(revenue) AS revenue,COUNT(*) AS transactions,ROUND(AVG(revenue),2) AS avg_transaction FROM sales GROUP BY month ORDER BY month"
df=pd.read_sql_query(monthly,conn)
print(df.to_string(index=False))
for row in df.itertuples(): print(row.month,'█'*int(row.revenue/500))
print('Miesiace powyzej sredniej:')
print(pd.read_sql_query('''SELECT strftime('%Y-%m',sale_date) AS month,SUM(revenue) AS revenue FROM sales GROUP BY month HAVING SUM(revenue) > (SELECT AVG(m_rev) FROM (SELECT SUM(revenue) AS m_rev FROM sales GROUP BY strftime('%Y-%m',sale_date))) ORDER BY revenue DESC''',conn))

conn.close()
