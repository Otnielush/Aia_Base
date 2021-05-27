import sqlite3 as sql
import datetime
import os


ROOT_DIR = os.path.abspath(os.path.join( os.path.abspath(__file__), os.pardir, os.pardir))
DB_ROOT = os.path.join(ROOT_DIR, 'database','database.db')

from flask import render_template, request, render_template_string
from application.database.params import cols_j, read_tstamp, read_db_id
from .language import lang_select


def init_jobs(app):

    @app.route('/job_add_form')
    def job_add_form():
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'jobs')
        return render_template('jobs/job_add_form.html', data_cols=cols_j[1:-1], col_names=cols_names[1:-1],
                               b_names=button_names)

    @app.route('/job_edit_form/<int:id>')
    def job_edit_form(id):
        data = read_db_id('jobs', id)
        # Lang selector
        cols_names, button_names = lang_select(app.lang, 'jobs')
        return render_template('jobs/job_edit_form.html', data=data, data_cols=cols_j[0:-3], col_names=cols_names[0:-3],
                               b_names=button_names, id=id)


    @app.route('/j_del', methods=['POST'])
    def job_delete():
        try:
            idd = request.form.get('id')
            conn = sql.connect(DB_ROOT)
            command = 'DELETE FROM jobs WHERE id=?'
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


    @app.route('/job_update', methods=['PUT', 'POST'])
    def job_update():
        try:
            con = sql.connect(DB_ROOT)
            data = ()
            command = 'UPDATE jobs SET ('
            vals = '= ('
            for col in cols_j[:-3]:
                command += (col + ', ')
                vals += '?,'

                data += (request.form[col],)

            # date update
            command += ('date_update, ')
            vals += '?,'
            data += (datetime.datetime.now().timestamp(),)

            command = command[:-2] + ') ' + vals[:-1] + ') WHERE jobs.id = {}'.format(request.form['id'])

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


    @app.route('/job_add', methods=['POST'])
    def job_add():
        if request.method == 'POST':
            try:
                con = sql.connect(DB_ROOT)
                data = ()
                command = 'INSERT INTO jobs ('
                vals = 'VALUES ('
                for col in cols_j[1:-1]:
                    command += (col + ', ')
                    vals += '?,'
                    if col == 'name' and len(request.form['name']) < 1:
                        data += ('-',)
                        vals += '?,'
                    else:
                        data += (request.form[col],)

                command += ('date_update, ')
                vals += '?,'
                data += (datetime.datetime.now().timestamp(),)
                command = command[:-2] +') '+vals[:-1]+')'

                cur = con.cursor()
                cur.execute(command, data)
                con.commit()
                msg = "Record successfully added"

                # WhatsApp message
                if request.form['city']:
                    city = str(request.form['city'])
                else:
                    city = ''
                details = '\n*Детали:* {}'.format(request.form['details']) if request.form['details'] else ''
                if request.form['wage']:
                    wage = '\n*ЗП:* '+ str(request.form['wage'])
                else:
                    wage = ''
                wa_msg = '*Новая вакансия:* {}\n*Город:* {}{}{}'.format(request.form['name'], city,
                                                                 details, wage)
                app.whatsapp.new_job_msg(wa_msg)


            except Exception as ex:
                con.rollback()
                msg = "error in insert operation"
                # print('record not added:', ex)

            finally:
                con.close()
                return render_template('result.html', msg=msg)



    @app.route('/jobs', methods=['POST', 'GET'])
    def jobs():
        rows = [0,1,2,3, 4, -1]
        con = sql.connect(DB_ROOT)
        con.row_factory = sql.Row

        if request.method == 'GET':
            cur = con.cursor()
            cur.execute("SELECT " + ', '.join(cols_j[rows]) + " FROM jobs ORDER BY date_update DESC")
            data = [dict(x) for x in cur.fetchall()]


        elif request.method == 'POST':
            search_word = request.form['q']
            search_text = [1, 2, 3, 5, 7, 9]
            search_nums = [0, 4, 8]
            search_date = [9]

            if search_word:
                query_1 = "SELECT " + ', '.join(cols_j[rows]) + " FROM jobs WHERE "
                search_word = search_word.replace(',', '')
                search_word = search_word.split(' ')
                search_cols = search_text + search_nums
                query_2 = " OR ".join(["{0} LIKE '%{1}%'".format(cols_j[c], w) for w in search_word for c in search_cols])

                cur = con.cursor()
                cur.execute(query_1+query_2 +' ORDER BY date_update DESC')
                data = [dict(x) for x in cur.fetchall()]
            else:
                cur = con.cursor()
                cur.execute("SELECT " + ', '.join(cols_j[rows]) + " FROM jobs ORDER BY date_update DESC")
                data = [dict(x) for x in cur.fetchall()]


        if len(data) > 0:
            for dd in data:
                dd['date_update'] = read_tstamp(dd['date_update'])

        con.close()
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'jobs')
        return render_template('jobs/jobs.html', data=data, data_cols=cols_j[rows], col_names=cols_names[rows],
                               b_names=button_names)


    @app.route('/j/<int:id>')
    def job_full(id):
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'jobs')
        data = read_db_id('jobs', id)
        return render_template('jobs/job_full.html', data=data, data_cols=cols_j, col_names=cols_names, b_names=button_names)

    return app


