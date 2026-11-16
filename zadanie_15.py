import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(15)
sales=pd.DataFrame({'category':np.repeat(['Elektronika','Akcesoria'],60),'product':np.tile(np.repeat(['A','B','C','D','E','F'],10),2),'revenue':rng.integers(20,2000,120)})
sales.to_sql('sales',conn,index=False)

print(pd.read_sql_query('''WITH totals AS (SELECT category,product,SUM(revenue) AS revenue FROM sales GROUP BY category,product), ranked AS (SELECT category,product,revenue,RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS ranking,ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS row_num FROM totals) SELECT * FROM ranked WHERE row_num<=3 ORDER BY category,ranking''',conn))

conn.close()
