from database.params import db_search, read_db_id, cols_w

for col in cols_w:
    data = db_search('workers', col, '0544777746')
# data = db_search('workers', 'id', '1')
#     data = read_db_id('workers', data[0]['id'])

    print(data)