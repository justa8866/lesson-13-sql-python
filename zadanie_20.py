import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(20)
rows=500000
batch=50000
conn.execute('CREATE TABLE production (id INTEGER,category TEXT,amount INTEGER)')
for offset in range(0,rows,batch):
    data=pd.DataFrame({'id':np.arange(offset,offset+batch),'category':rng.choice(['A','B','C','D','E'],batch),'amount':rng.integers(1,1001,batch)})
    data.to_sql('production',conn,if_exists='append',index=False)

def strategy(mode):
    if mode=='Nieoptymalna':
        query='SELECT * FROM production'
        raw=pd.read_sql_query(query,conn)
        result=raw.loc[raw.category=='A'].groupby('category',as_index=False)['amount'].sum().head(5)
    elif mode=='Czesciowa':
        query="SELECT * FROM production WHERE category='A'"
        raw=pd.read_sql_query(query,conn)
        result=raw.groupby('category',as_index=False)['amount'].sum().head(5)
    else:
        query="SELECT category,SUM(amount) AS amount FROM production WHERE category='A' GROUP BY category ORDER BY amount DESC LIMIT 5"
        raw=pd.read_sql_query(query,conn)
        result=raw
    return raw,result,query
report=[]
for mode in ['Nieoptymalna','Czesciowa','Optymalna']:
    if mode=='Czesciowa':conn.execute('CREATE INDEX idx_category ON production(category)')
    durations=[]
    for _ in range(3):
        start=time.perf_counter();raw,result,query=strategy(mode);durations.append(time.perf_counter()-start)
    seconds=sum(durations)/3
    memory=raw.memory_usage(deep=True).sum()
    report.append({'strategia':mode,'czas_ms':seconds*1000,'pamiec_KB':memory/1024,'wiersze':len(raw),'proxy_energia':seconds*memory})
    print('\n',mode,'wynik:\n',result.to_string(index=False))
    print('Plan:\n',pd.read_sql_query('EXPLAIN QUERY PLAN '+query,conn).to_string(index=False))
df=pd.DataFrame(report)
print('\nPOROWNANIE:\n',df.to_string(index=False))
for row in df.itertuples():
    print(row.strategia,'czas:', '█'*max(1,int(row.czas_ms/10)),'pamiec:', '█'*max(1,int(row.pamiec_KB/500)))
a,b=report[0],report[-1]
for label,key in [('Czas','czas_ms'),('Transfer/pamiec','pamiec_KB'),('Proxy energii','proxy_energia')]:
    print(f'{label}: oszczednosc {(1-b[key]/a[key])*100:.2f}%')
print('Wniosek: filtrowanie, agregacja i LIMIT w SQL ograniczaja transfer; indeks moze przyspieszyc filtrowanie, ale nalezy mierzyc wyniki.')

conn.close()
