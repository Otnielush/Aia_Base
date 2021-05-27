import sqlite3
from params import cols_w, col_types_w, cols_c, col_types_c, cols_j, col_types_j


def _create_table(connection, name, columns, column_types):
    command = 'CREATE TABLE ' + name + ' ('
    for i in range(len(columns)):
        command += (columns[i] + ' ' + column_types[i] + ', ')
    command = command[:-2] + ')'
    connection.execute(command)
    print('table ' +name+ ' created')

def _copy_table(connection, name, new_table_name, columns):
    command = 'INSERT INTO ' + new_table_name + ' ('
    columns_t = ', '.join(columns)
    command = command + columns_t +') SELECT ' + columns_t +' FROM ' + name

    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    print('Table copied')


def _del_table(connection, name):
    command = "DROP TABLE IF EXISTS " + name
    connection.execute(command)
    print('Table', name, 'deleted')


def rebuild_table(name, columns, col_types):
    # Make a connection to the SQLite DB
    dbCon = sqlite3.connect("database.db")

    new_name = name+'_2'
    _create_table(dbCon, new_name, columns, col_types)
    _copy_table(dbCon, name, new_name, columns)
    _del_table(dbCon, name)

    command = 'ALTER TABLE '+new_name+' RENAME TO '+name
    dbCon.execute(command)
    dbCon.close()
    print('Rebuild done')



table = 'workers'
rebuild_table(table, cols_w, col_types_w)



