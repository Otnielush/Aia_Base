import sqlite3 as sql
import datetime
import os

ROOT_DIR = os.path.abspath(os.path.join( os.path.abspath(__file__), os.pardir, os.pardir))
DB_ROOT = os.path.join(ROOT_DIR, 'database','database.db')

from flask import render_template, request, render_template_string
from application.database.params import cols_c, read_tstamp, read_db_id, button_names_c, cols_c_rus
from .language import lang_select


def init_clients(app):
    @app.route('/client_add_form')
    def client_add_form():
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'clients')
        return render_template('clients/client_add_form.html', data_cols=cols_c[1:-1], col_names=cols_names[1:-1], b_names=button_names)


    @app.route('/client_edit_form/<int:id>')
    def client_edit_form(id):
        data = read_db_id('clients', id)
        # Lang selector
        cols_names, button_names = lang_select(app.lang, 'clients')
        return render_template('clients/client_edit_form.html', data=data, data_cols=cols_c[0:-1],
                               col_names=cols_names[0:-1], b_names=button_names, id=id)

    @app.route('/c_del', methods=['POST'])
    def client_delete():
        try:
            idd = request.form.get('id')
            conn = sql.connect(DB_ROOT)
            command = 'DELETE FROM clients WHERE id=?'
            cur = conn.cursor()
            cur.execute(command, (idd,))
            conn.commit()
            msg = "ID: -{}- deleted from database".format(idd)
        except Exception as ex:
            conn.rollback()
            msg = "error in delete operation"
            print('record not deleted:', ex)
        finally:
            conn.close()
            return render_template('result.html', msg=msg)


    @app.route('/client_update', methods=['PUT', 'POST'])
    def client_update():
        try:
            con = sql.connect(DB_ROOT)
            data = ()
            command = 'UPDATE clients SET ('
            vals = '= ('
            for col in cols_c[:-1]:
                command += (col + ', ')
                vals += '?,'
                data += (request.form[col],)

            command = command[:-2] + ') ' + vals[:-1] + ') WHERE clients.id = {}'.format(request.form['id'])

            cur = con.cursor()
            cur.execute(command, data)
            con.commit()
            msg = "id: {}. Record successfully updated".format(request.form['id'])
        except Exception as ex:
            con.rollback()
            msg = "error in update operation"
            print('record not updated:', ex)

        finally:
            con.close()
            return render_template('result.html', msg=msg)



    @app.route('/client_add', methods=['POST'])
    def client_add():
        if request.method == 'POST':
            try:
                con = sql.connect(DB_ROOT)
                data = ()
                command = 'INSERT INTO clients ('
                vals = 'VALUES ('
                for col in cols_c[1:-1]:
                    command += (col + ', ')
                    vals += '?,'

                    if col == 'name':
                        if len(request.form['name']) < 1:
                            data += ('-',)
                        else:
                            data += (request.form[col],)
                    else:
                        data += (request.form[col],)


                command = command[:-2] + ') ' + vals[:-1] + ')'
                # print(data)
                # print(command)

                cur = con.cursor()
                cur.execute(command, data)
                con.commit()
                msg = "Record successfully added"
            except Exception as ex:
                con.rollback()
                msg = "error in insert operation"
                print('record not added:', ex)

            finally:
                con.close()
                return render_template('result.html', msg=msg)



    @app.route('/clients', methods=['POST', 'GET'])
    def clients():
        rows = [0,1,3,4,16]
        con = sql.connect(DB_ROOT)
        con.row_factory = sql.Row

        if request.method == 'GET':
            cur = con.cursor()
            cur.execute("SELECT " + ', '.join(cols_c[rows]) + " FROM clients ORDER BY name ASC")
            data = [dict(x) for x in cur.fetchall()]

        elif request.method == 'POST':
            search_word = request.form['q']
            search_text = [1,3,4,5,7,8,12,13,14,15]
            search_nums = [0,2,6,9,10,11,16,17]

            if search_word:
                query_1 = "SELECT " + ', '.join(cols_c[rows]) + " FROM clients WHERE "
                search_word = search_word.replace(',', '')
                search_word = search_word.split(' ')
                search_cols = search_text + search_nums
                query_2 = " OR ".join(["{0} LIKE '%{1}%'".format(cols_c[c], w) for w in search_word for c in search_cols])

                cur = con.cursor()

                cur.execute(query_1+query_2+' ORDER BY name ASC')
                data = [dict(x) for x in cur.fetchall()]
            else:
                cur = con.cursor()
                cur.execute("SELECT " + ', '.join(cols_c[rows]) + " FROM clients ORDER BY name ASC")
                data = [dict(x) for x in cur.fetchall()]


        con.close()
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'clients')
        return render_template('clients/clients.html', data=data, data_cols=list(cols_c[rows]), col_names=list(cols_names[rows]),
                               b_names=button_names)


    @app.route('/c/<int:id>')
    def client_full(id):
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'clients')
        data = read_db_id('clients', id)
        return render_template('clients/client_full.html', data=data, data_cols=cols_c[:-1], col_names=cols_names[:-1], b_names=button_names)

    return app
