import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
titanic=pd.DataFrame([('female',1,1,38,71.28),('female',1,1,35,53.1),('female',1,0,30,60),('male',3,0,22,7.25),('male',3,0,28,8.05),('male',3,1,19,10)],columns=['sex','pclass','survived','age','fare'])
titanic.to_sql('titanic',conn,index=False)

query="""SELECT CASE WHEN sex='female' THEN 'Kobiety 1 klasa ocalale' ELSE 'Mezczyzni 3 klasa nieocalali' END AS grupa,COUNT(*) AS liczba,ROUND(AVG(age),2) AS avg_age,ROUND(AVG(fare),2) AS avg_fare FROM titanic WHERE (sex='female' AND pclass=1 AND survived=1) OR (sex='male' AND pclass=3 AND survived=0) GROUP BY sex ORDER BY sex"""
result=pd.read_sql_query(query,conn)
print(result.to_string(index=False))
for row in result.itertuples(): print(f'{row.grupa}: {"█"*int(row.avg_fare/5)} ({row.avg_fare:.2f} PLN)')

conn.close()
