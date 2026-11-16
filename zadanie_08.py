import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
rng=np.random.default_rng(42)
pd.DataFrame({'id':np.arange(10000),'value':rng.integers(0,1000,10000)}).to_sql('measurements',conn,index=False)

query='SELECT * FROM measurements WHERE value = 777'
def benchmark():
    times=[]
    for _ in range(5):
        start=time.perf_counter(); pd.read_sql_query(query,conn); times.append(time.perf_counter()-start)
    return sum(times)/len(times)
print('BEZ INDEKSU:',pd.read_sql_query('EXPLAIN QUERY PLAN '+query,conn).to_string(index=False))
a=benchmark()
conn.execute('CREATE INDEX idx_value ON measurements(value)')
print('Z INDEKSEM:',pd.read_sql_query('EXPLAIN QUERY PLAN '+query,conn).to_string(index=False))
b=benchmark()
print(f'Bez: {a*1000:.3f} ms, z: {b*1000:.3f} ms, przyspieszenie: {a/b:.2f}x')

conn.close()
