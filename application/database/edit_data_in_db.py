import sqlite3 as sql

def read_data(name):
    # Make a connection to the SQLite DB
    dbCon = sql.connect("database.db")
    dbCon.row_factory = sql.Row
    cur = dbCon.cursor()

    command = "SELECT id, name, phone FROM "+name+" WHERE "+name+".phone LIKE '5%'"
    try:
        cur.execute(command)
        print('1')
        data = [dict(x) for x in cur.fetchall()]
        for dd in data:
            print(dd)
    except Exception as e:
        print('problem:', e)
    finally:
        dbCon.close()

def edit_data(name):
    # Make a connection to the SQLite DB
    dbCon = sql.connect("database.db")
    dbCon.row_factory = sql.Row
    cur = dbCon.cursor()

    command = "UPDATE "+name+" SET phone = ('0' || phone) WHERE phone LIKE '5%'"
    try:
        cur.execute(command)
        dbCon.commit()
        print('edit done')
    except Exception as e:
        print(e)
    finally:
        dbCon.close()


table = 'workers'
# edit_data(table)
read_data(table)