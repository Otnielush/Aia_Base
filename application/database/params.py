import numpy as np
import datetime

button_names_w = {'eng':
                    {'add': '+ Add new worker', 'edit': 'Edit', 'delete': 'delete', 'back_list': 'Back to workers',
                     'back_main': 'Back to homepage', 'search':'Search', 'submit':'Submit', 'title':'WORKER INFORMATION',
                     'single':'single', 'married':'married', 'divorced':'divorced', 'widowed':'widowed',
                     'working':'working', 'free':'free', 'prev':'< prev', 'next':'next >', 'page':'page',
                     1:'Yes', 0:'No', 'update':'update'},
                'rus':
                    {'add': '+ Новый работник', 'edit': 'Редактировать', 'delete': 'удалить', 'back_list': 'Назад к списку',
                     'back_main': 'Назад на главную', 'search':'Поиск', 'submit':'Подтвердить', 'title':'Информация о рабочем',
                     'single':'холост', 'married':'женат', 'divorced':'разведён', 'widowed':'вдовец',
                     'working':'работает', 'free':'без работы', 'prev':'< пред', 'next':'след >', 'page':'страница',
                     1:'Да', 0:'Нет', 'update':'обновить'},
                'heb':
                    {}}
button_names_j = {'eng':
                    {'add': '+ Add new job', 'edit': 'Edit', 'delete': 'delete', 'back_list': 'Back to jobs',
                     'back_main': 'Back to homepage', 'search':'Search', 'submit':'Submit', 'title':'JOB INFORMATION',
                     },
                'rus':
                    {'add': '+ Новая вакансия', 'edit': 'Редактировать', 'delete': 'удалить', 'back_list': 'Назад к списку',
                     'back_main': 'Назад на главную', 'search':'Поиск', 'submit':'Подтвердить', 'title':'Информация о вакансии',
                     },
                'heb':
                    {}}
button_names_c = {'eng':
                    {'add': '+ Add new client', 'edit': 'Edit', 'delete': 'delete', 'back_list': 'Back to clients',
                     'back_main': 'Back to homepage', 'search':'Search', 'submit':'Submit', 'title':'CLIENT INFORMATION',
                     'prev':'< prev', 'next':'next >', 'page':'page'},
                'rus':
                    {'add': '+ Новый клиент', 'edit': 'Редактировать', 'delete': 'удалить', 'back_list': 'Назад к списку',
                     'back_main': 'Назад на главную', 'search':'Поиск', 'submit':'Подтвердить', 'title':'Информация о клиенте',
                     'prev':'< пред', 'next':'след >', 'page':'страница'},
                'heb':
                    {}}


# DB WORKERS
cols_w = np.array(['id', 'name', 'lastname', 'teudat_zeut', 'driver',  # 0
                   'phone', 'phone2', 'email', 'whatsapp',  # 5
        'facebook','linkedin', 'look_for', 'experience', 'city','street','house_num','flat_num',  # 9
        'working','work_place','marital_status',  # 17
        'age','date_create','date_update'])  # 20
search_text_w = [1, 2, 7, 9, 10, 11, 12, 13, 14, 18, 19]
search_nums_w = [0, 3, 4, 5, 6, 8, 17, 20]

col_types_w = np.array(['INTEGER PRIMARY KEY', 'TEXT NOT NULL', 'TEXT', 'INTEGER DEFAULT 0', 'INTEGER DEFAULT 0',
                        'TEXT', 'TEXT', 'TEXT', 'TEXT',
             'TEXT','TEXT', 'TEXT', 'TEXT','TEXT','TEXT',"INTEGER", 'INTEGER',
             'INTEGER DEFAULT 0','INTEGER','TEXT',
             'INTEGER DEFAULT 0','TIMESTAMP NOT NULL','''TIMESTAMP NOT NULL, FOREIGN KEY (work_place) 
             REFERENCES clients (id) ON UPDATE CASCADE ON DELETE SET NULL'''])


cols_w_rus = np.array(['id', 'Имя', 'Фамилия', 'Теудат зэут', 'Водительские права',
                       'Телефон', 'Телефон 2', 'email', 'whatsapp',
        'facebook','linkedin','Ищет', 'Опыт работы', 'Город','Улица','Номер дома','Номер квартиры',
        'Работает сейчас?','Место работы','Семейное положение',
        'Возраст','Дата создания анкеты','Дата обновления анкеты'])

# DB CLIENTS
cols_c = np.array(['id', 'name', 'het_pey','occupation', 'city', 'street', 'house_num',
          'owner_name', 'owner_lastname', 'owner_teudat_zeut',
          'phone', 'phone2', 'contact_name', 'contact_name2',
          'email', 'email2',
            'workers_num', 'workers_num_our', 'workers_our'])

col_types_c = np.array(['INTEGER PRIMARY KEY', 'TEXT NOT NULL', 'TEXT','TEXT', 'TEXT', 'TEXT', 'INTEGER',
               'TEXT','TEXT','TEXT',
               'TEXT','TEXT','TEXT', 'TEXT',
             'TEXT','TEXT',
               'INTEGER', 'INTEGER','INTEGER'])

cols_c_rus = np.array(['id', 'Название', '№ хэт пэй', 'Род деятельности', 'Город', 'Улица', '№ дома',
          'Имя владельца', 'Фамилия владельца', '№ Т.З. владельца',
          'Телефон', 'Телефон 2', 'Имя контакта', 'Имя контакта 2',
          'email', 'email 2',
            'Кол-во рабочих', 'Кол-во наших рабочих', 'Наши работники'])

0,2,6,9,10,11,16,17
# DB JOBS
cols_j = np.array(['id', 'name', 'city', 'firm', 'wage', 'details', 'workers',
                    'contact_name', 'contact_tel', 'contact_email', 'date_update'])

col_types_j = np.array(['INTEGER PRIMARY KEY', 'TEXT NOT NULL', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT',
               'INTEGER', 'TEXT', 'TEXT', 'TEXT', '''TIMESTAMP NOT NULL, FOREIGN KEY (firm) 
             REFERENCES clients (id) ON UPDATE CASCADE ON DELETE SET NULL'''])

cols_j_rus = np.array(['id', 'Название', "Город", 'Фирма', 'Зарплата', 'Описание', 'Рабочии',
                    'Контакное лицо', 'Контактный телефон', 'Контактный email', 'Дата обновления'])

# FB jobs searchers posts
cols_fb_work = np.array(['id', 'username', 'user_id', 'group_name', 'time', 'text',
                         'post_url','processed'])
col_types_fb_work = np.array(['INTEGER PRIMARY KEY', 'TEXT', 'TEXT', 'INTEGER', 'TIMESTAMP', 'TEXT',
                              'TEXT NOT NULL UNIQUE', 'INTEGER DEFAULT 0'])



import os
import sqlite3 as sql
ROOT_DIR = os.path.abspath(os.path.join( os.path.abspath(__file__), os.pardir, os.pardir))
DB_ROOT = os.path.join(ROOT_DIR, 'database','database.db')

import datetime
def read_tstamp(stamp, date_only=False):
    try:
        if date_only:
            date =  datetime.datetime.fromtimestamp(float(stamp)).strftime("%d-%m-%Y")
        else:
            date = datetime.datetime.fromtimestamp(float(stamp)).strftime("%d-%m-%Y, %H:%M")
        return date
    except Exception as ex:
        print('Date not parsed from stamp:', ex)
        return "01-01-1900"

def read_db_id(db, id):
    command = 'SELECT * FROM {} WHERE id == {}'.format(db, id)
    con = sql.connect(DB_ROOT)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(command)

    data = [dict(x) for x in cur.fetchall()]
    if len(data) > 0:
        for dd in data:
            if 'date_update' in dd:
                dd['date_update'] = read_tstamp(dd['date_update'])
            if 'date_create' in dd:
                dd['date_create'] = read_tstamp(dd['date_create'])

    con.close()
    return data

def db_search(db, column, text):
    command = 'SELECT id FROM {} WHERE {} LIKE "%{}%"'.format(db, column, text)

    con = sql.connect(DB_ROOT)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(command)

    data = np.array([dict(x)['id'] for x in cur.fetchall()])
    con.close()
    return data

# databese name, columns names, list of data
def insert_to_db(db: str, cols: list, data: list, db_file=DB_ROOT):
    if 'id' in cols:
        cols = list(cols)
        cols.remove('id')
    
    command = 'INSERT OR IGNORE INTO {} ('.format(db) + ', '.join(cols) + ') '
    vals = 'VALUES ('+ '?,'*len(cols)
    command += vals[:-1]+')'
    
    if len(data[0]) != len(cols):
        msg = '''Информация не добавлена.
        Incorrect number of bindings supplied. The current statement uses {}, and there are {} supplied'''.format(len(cols), len(data[0]))
        print(msg)
        return msg
    
    insert_data = []
    if type(data[0]) == tuple:
        for dd in data:
            insert_data.append(dd)
    elif type(data[0]) == list:
        for dd in data:
            insert_data.append(tuple(dd))
    elif type(data[0]) == dict:
        for dd in data:
            tt = tuple()
            for col in cols:
                try:
                    if col in ['date_create', 'date_update']:
                        tt += (datetime.datetime.now().timestamp(),)
                    else:
                        tt += (dd[col],)
                except:
                    tt += ('',)
            insert_data.append(tt)
    
    con = sql.connect(db_file)
    cur = con.cursor()
    
    if len(insert_data) > 1:
        cur.executemany(command, insert_data)
    else:
        cur.execute(command, insert_data[0])
        
    con.commit()
    con.close()
    
    return 'Информация добавлена'
    

# cols_w = np.array(['id', 'name', 'lastname', 'teudat_zeut', 'driver',
#                    'phone', 'phone2', 'email', 'whatsapp',
#         'facebook','linkedin', 'look_for', 'experience', 'city','street','house_num','flat_num',
#         'cv','photo','working','work_place','marital_status','children_number',
#         'age','date_create','date_update'])
#
# col_types_w = np.array(['INTEGER PRIMARY KEY', 'TEXT NOT NULL', 'TEXT', 'INTEGER DEFAULT 0', 'INTEGER DEFAULT 0',
#                         'TEXT', 'TEXT', 'TEXT', 'TEXT',
#              'TEXT','TEXT', 'TEXT', 'TEXT','TEXT','TEXT',"INTEGER", 'INTEGER',
#              'BLOB','BLOB','INTEGER','INTEGER','TEXT','INTEGER',
#              'INTEGER','TIMESTAMP NOT NULL','''TIMESTAMP NOT NULL, FOREIGN KEY (work_place)
#              REFERENCES clients (id) ON UPDATE CASCADE ON DELETE SET NULL'''])

