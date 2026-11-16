import sqlite3
import pandas as pd
import numpy as np
import time

conn = sqlite3.connect(':memory:')
employees=pd.DataFrame([(1,'Dyrektor',None),(2,'Anna',1),(3,'Jan',1),(4,'Piotr',2),(5,'Maria',2),(6,'Ola',3)],columns=['employee_id','name','manager_id'])
employees.to_sql('employees',conn,index=False)

print(pd.read_sql_query('''SELECT e1.name AS employee,e2.name AS manager FROM employees e1 LEFT JOIN employees e2 ON e1.manager_id=e2.employee_id''',conn))
print(pd.read_sql_query('''SELECT * FROM employees WHERE manager_id IS NULL''',conn))
print(pd.read_sql_query('''SELECT m.name AS manager,COUNT(e.employee_id) AS subordinates FROM employees m JOIN employees e ON e.manager_id=m.employee_id GROUP BY m.employee_id,m.name ORDER BY subordinates DESC''',conn))

conn.close()
