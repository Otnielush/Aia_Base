import sqlite3 as sql
import datetime
import os
import pandas as pd
import numpy as np


ROOT_DIR = os.path.abspath(os.path.join( os.path.abspath(__file__), os.pardir, os.pardir))
DB_ROOT = os.path.join(ROOT_DIR, 'database','database.db')

from flask import render_template, request, make_response, jsonify
from application.database.params import (
    cols_w, read_tstamp, read_db_id, db_search, search_text_w, search_nums_w)
from .language import lang_select

def init_workers(app):
    @app.route('/')
    def home():
        return render_template('home.html')
        # return render_template_string('''<html><body><h1>Hii world</h1></body></html>''')

    @app.route('/worker_add_form')
    def worker_add_form():
        try:
            q_val = None
            q_val = request.args['q']
        except: pass

        # Language selector
        cols_names, button_names = lang_select(app.lang, 'workers')
        return render_template('workers/worker_add_form.html', data_cols=cols_w[1:-2], col_names=cols_names[1:-2],
                               b_names=button_names, q=q_val)

    @app.route('/worker_edit_form/<int:id>')
    def worker_edit_form(id):
        try:
            q_val = None
            q_val = request.args['q']
        except: pass

        data = read_db_id('workers', id)
        # Lang selector
        cols_names, button_names = lang_select(app.lang, 'workers')
        return render_template('workers/worker_edit_form.html', data=data, data_cols=cols_w[0:-2],
                               col_names=cols_names[0:-2], q=q_val,
                               b_names=button_names, id=id)

    @app.route('/w_del', methods=['POST'])
    def worker_delete():
        try:
            idd = request.form.get('id')
            conn = sql.connect(DB_ROOT)
            command = 'DELETE FROM workers WHERE id=?'
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
            # Lang selector
            _, button_names = lang_select(app.lang, 'workers')
            return render_template('result.html', msg=msg, b_names=button_names, autolink='/workers')

    @app.route('/worker_update', methods=['PUT', 'POST'])
    def worker_update():
        try:
            con = sql.connect(DB_ROOT)
            data = ()
            command = 'UPDATE workers SET ('
            vals = '= ('
            for col in cols_w[:-2]:
                command += (col + ', ')
                vals += '?,'
                data += (request.form[col],)

            # date update
            command += ('date_update, ')
            vals += '?,'
            data += (datetime.datetime.now().timestamp(),)

            command = command[:-2] + ') ' + vals[:-1] + ') WHERE workers.id = {}'.format(request.form['id'])
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
            # Lang selector
            cols_names, button_names = lang_select(app.lang, 'workers')
            return render_template('result.html', b_names=button_names, msg=msg)

    @app.route('/worker_add', methods=['POST'])
    def worker_add():
        whatsapp_send = False
        # Lang selector
        _, button_names = lang_select(app.lang, 'workers')
        if request.method == 'POST':
            # duplicate check
            phone = request.form['phone']
            if len(phone) > 0:
                ids = db_search('workers', 'phone', phone)
                if len(ids) > 0:
                    msg = "Record already exist"
                    return render_template('result.html', b_names=button_names, msg=msg, autolink='/w/' + str(ids[0]),
                                           delay_time=2)
            # duplicate check by name, lastname
            names = db_search('workers', 'name', request.form['name'])
            if len(request.form['lastname']) > 0:
                l_names = db_search('workers', 'lastname', request.form['lastname'])
            else:
                l_names = []
            ids = np.intersect1d(names, l_names)
            if len(ids) > 0:
                msg = "Record already exist"
                return render_template('result.html', b_names=button_names, msg=msg, autolink='/w/' + str(ids[0]),
                                       delay_time=2)

            try:
                con = sql.connect(DB_ROOT)
                data = ()
                command = 'INSERT INTO workers ('
                vals = 'VALUES ('
                for col in cols_w[1:]:
                    command += (col + ', ')
                    vals += '?,'
                    if col in ['date_create', 'date_update']:
                        data += (datetime.datetime.now().timestamp(),)
                    elif col == 'name':
                        if len(request.form['name']) < 1:
                            data += ('-',)
                        else:
                            data += (request.form[col],)
                    else:
                        data += (request.form[col],)

                command = command[:-2] + ') ' + vals[:-1] + ')'
                # print(len(cols_w[1:]))
                # print(command)
                # print(data)
                cur = con.cursor()
                cur.execute(command, data)
                con.commit()
                msg = "Record successfully added"
                # WhatsApp message
                if whatsapp_send:
                    try:
                        if request.form['whatsapp']:
                            if str(request.form['whatsapp'])[0] == '+':
                                phone = str(request.form['whatsapp'])
                            elif str(request.form['whatsapp'])[0:2] == '05':
                                phone = '+972' + str(request.form['whatsapp'])[1:]
                            elif str(request.form['whatsapp'])[0] == '5':
                                phone = '+972' + str(request.form['whatsapp'])
                            else:
                                phone = ''

                            if phone:
                                phone = '\nwa.me/' + phone
                        elif request.form['phone']:
                            if str(request.form['phone'])[0] == '+':
                                phone = str(request.form['phone'])
                            elif str(request.form['phone'])[0:2] == '05':
                                phone = '+972' + str(request.form['phone'])[1:]
                            elif str(request.form['phone'])[0] == '5':
                                phone = '+972' + str(request.form['phone'])
                            else:
                                phone = ''
                        else:
                            phone = ''

                        if request.form['age']:
                            age = ', ' + str(request.form['age']) + ' ??????'
                        else:
                            age = ''
                        if request.form['city']:
                            city = ', ' + str(request.form['city'])
                        else:
                            city = ''
                        if request.form['look_for']:
                            look_for = '\n*????????:* ' + str(request.form['look_for'])
                        else:
                            look_for = ''
                        wa_msg = '*?????????? ????????????:*\n{} {}{}{}{}{}'.format(request.form['name'],
                                                                         request.form['lastname'], age, city,
                                                                         phone, look_for)

                        app.whatsapp.new_worker_msg(wa_msg)
                    except:
                        print('Whatsapp message not sended')

            except Exception as ex:
                con.rollback()
                msg = "error in insert operation"
                print('record not added:', ex)

            finally:
                con.close()
                return render_template('result.html', msg=msg, b_names=button_names, autolink='/workers')

    @app.route('/workers', methods=['POST', 'GET'])
    def workers():
        rows = [0, 1, 2, 5, 3, 11, 12, 13, 17, 20, 22]  # to show on page
        con = sql.connect(DB_ROOT)
        con.row_factory = sql.Row

        try:
            q_val = None
            q_val = request.args['q']
        except: pass

        if request.method == 'GET' and not q_val:
            cur = con.cursor()
            cur.execute("SELECT " + ', '.join(cols_w[rows]) + " FROM workers ORDER BY date_update DESC")
            data = [dict(x) for x in cur.fetchall()]

        elif request.method == 'POST' or q_val:
            if request.method == 'POST':
                # print(f"{q_val = }")
                search_word = request.form['q']
                if q_val and len(search_word) > 0:
                    search_word = q_val +',' + search_word
                q_val = search_word
            else:
                search_word = q_val

            # TODO search column (column: query)
            if search_word:
                cur = con.cursor()
                query_1 = "SELECT " + ', '.join(cols_w[rows]) + " FROM workers WHERE "
                search_word = search_word.rstrip().lstrip()
                search_word = search_word.split(',')
                # if search_word[0][0] in ['??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??', '??']:
                search_cols = search_text_w + search_nums_w

                query_3 = []
                for w in search_word:
                    query_2 = " OR ".join(["{0} LIKE '%{1}%'".format(cols_w[c], w.rstrip().lstrip()) for c in search_cols])
                    query_3.append("("+query_2+")")

                if len(query_3) > 1:
                    query_2 = " AND ".join(query_3)
                # print(f"{query_2 = }")

                # result
                cur.execute(query_1 + query_2 + ' ORDER BY date_update DESC')
                data = [dict(x) for x in cur.fetchall()]
            else:
                cur = con.cursor()
                cur.execute("SELECT " + ', '.join(cols_w[rows]) + " FROM workers ORDER BY date_update DESC")
                data = [dict(x) for x in cur.fetchall()]

        if len(data) > 0:
            for dd in data:
                # dd['date_create'] = datetime.datetime.fromtimestamp(float(dd['date_create'])).strftime("%d-%m-%Y, %H:%M")
                dd['date_update'] = read_tstamp(dd['date_update'])
                # dd['date_born'] = datetime.datetime.fromtimestamp(float(dd['date_born'])).strftime("%d-%m-%Y")
                dd['name'] = dd['name'] + ' ' + dd['lastname']

        rows.remove(2)  # rem last name
        rows.remove(17)  # rem working

        con.close()

        # Language selector
        cols_names, button_names = lang_select(app.lang, 'workers')
        return render_template('workers/workers.html', data=data, data_cols=list(cols_w[rows]),
                               col_names=list(cols_names[rows]), q=q_val,
                               b_names=button_names, next=request.url)

    # TODO ?????? ???????????? ?? ???????? ?????????????? ?????????? ?????? ?????? ?????????????????? ?? ????????????????????

    @app.route('/w/<int:id>')
    def worker_full(id):
        try:
            q_val = None
            q_val = request.args['q']
        except: pass
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'workers')
        data = read_db_id('workers', id)
        if len(data) < 1:
            msg = 'Id not found'
            return render_template('result.html', msg=msg, b_names=button_names, autolink='/workers')
        return render_template('workers/worker_full.html', data=data, data_cols=cols_w, col_names=cols_names,
                               b_names=button_names, q=q_val)



    @app.route("/workers_api", methods=['GET'])
    def workers_api():
        if request.method != 'GET':
            return make_response('Malformed request', 400)
        my_dict = {'key': 'dictionary value'}
        headers = {"Content-Type": "application/json"}
        return make_response(jsonify(my_dict), 200, headers)



    return app
