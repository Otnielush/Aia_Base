import sqlite3
import pandas as pd

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * from workers", con)

# Verify that result of SQL query is stored in the dataframe
print(df.head())

con.close()

df.to_csv( 'workers_db.csv', encoding='utf-8-sig',index=None)