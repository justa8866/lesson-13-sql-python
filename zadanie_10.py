import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
sales=pd.DataFrame([('Elektronika',3500),('Akcesoria',200),('Elektronika',1200),('Dom',600),('Dom',700),('Akcesoria',900)],columns=['category','revenue'])
sales.to_sql('sales',conn,index=False)

print(pd.read_sql_query('''SELECT category,COUNT(*) AS transakcje,SUM(revenue) AS przychod,ROUND(AVG(revenue),2) AS srednia FROM sales GROUP BY category HAVING SUM(revenue)>1000 ORDER BY przychod DESC''',conn))

conn.close()
