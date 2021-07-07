import sqlite3

db_name = "database.db"

conn = sqlite3.connect(db_name)

print('opened database successfully')

from params import cols_w, col_types_w, cols_c, col_types_c, cols_j, col_types_j, cols_fb_work, col_types_fb_work

def create_table(connection, name, columns, column_types):
    command = 'CREATE TABLE ' + name + ' ('
    for i in range(len(columns)):
        command += (columns[i] + ' ' + column_types[i] + ', ')
    command = command[:-2] + ')'
    connection.execute(command)
    print('table ' +name+ ' created successfully')

try:
    create_table(conn, 'workers', cols_w, col_types_w)
except: pass
try:
    create_table(conn, 'clients', cols_c, col_types_c)
except: pass
try:
    create_table(conn, 'jobs', cols_j, col_types_j)
except: pass
conn.close()

db_name = "facebook.db"
conn = sqlite3.connect(db_name)

try:
    create_table(conn, 'post_work', cols_fb_work, col_types_fb_work)
except: pass


conn.close()
