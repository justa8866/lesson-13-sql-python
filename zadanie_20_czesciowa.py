import sqlite3
import pandas as pd
import numpy as np
import time

conn=sqlite3.connect(':memory:')
rng=np.random.default_rng(20)
rows=500000
batch=50000
conn.execute('CREATE TABLE production (id INTEGER,category TEXT,amount INTEGER)')
for offset in range(0,rows,batch):
    data=pd.DataFrame({'id':np.arange(offset,offset+batch),'category':rng.choice(['A','B','C','D','E'],batch),'amount':rng.integers(1,1001,batch)})
    data.to_sql('production',conn,if_exists='append',index=False)

# Strategia: czesciowa
conn.execute("CREATE INDEX idx_category ON production(category)")
def run():
    raw=pd.read_sql_query("SELECT * FROM production WHERE category='A'",conn)
    result=raw.groupby('category',as_index=False)['amount'].sum().head(5)
    return raw,result,"SELECT * FROM production WHERE category='A'"
durations=[]
for _ in range(3):
    start=time.perf_counter();raw,result,query=run();durations.append(time.perf_counter()-start)
print('Wynik:',result.to_string(index=False))
print('Czas sredni (ms):',round(sum(durations)/3*1000,2))
print('Pamiec (KB):',round(raw.memory_usage(deep=True).sum()/1024,2))
print('Pobrane wiersze:',len(raw))
print('Plan:',pd.read_sql_query('EXPLAIN QUERY PLAN '+query,conn).to_string(index=False))

conn.close()
