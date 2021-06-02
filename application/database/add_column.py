import sqlite3




# Retrieve the SQL statment for the tables and check the schema
# masterQuery = "select * from sqlite_master"
#
# cur.execute(masterQuery)
#
# tableList = cur.fetchall()
#
# for table in tableList:
#     print("Database Object Type: %s" % (table[0]))
#
#     print("Database Object Name: %s" % (table[1]))
#
#     print("Table Name: %s" % (table[2]))
#
#     print("Root page: %s" % (table[3]))
#
#     print("**SQL Statement**: %s" % (table[4]))


def db_add_column(db_file, table, column_name, column_type):
    # Make a connection to the SQLite DB
    dbCon = sqlite3.connect(db_file)
    # Obtain a Cursor object to execute SQL statements
    cur = dbCon.cursor()
    # Add a new column to student table
    addColumn = "ALTER TABLE {} ADD COLUMN {} {}".format(table, column_name, column_type)
    cur.execute(addColumn)
    # close the database connection
    dbCon.close()
    print('Column', column_name, 'added')

if __name__ == '__main__':
    db_add_column('facebook.db','post_work', 'group_name', 'TEXT')