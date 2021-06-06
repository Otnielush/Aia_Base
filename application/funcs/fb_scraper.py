from facebook_scraper import get_posts, get_group_info
import re
import os
import sqlite3 as sql
import datetime
from time import sleep

ROOT_DIR = os.path.abspath(os.path.join( os.path.abspath(__file__), os.pardir, os.pardir))
DB_ROOT = os.path.join(ROOT_DIR, 'database','facebook.db')

from flask import render_template, request, redirect
from application.database.params import cols_fb_work, read_tstamp, insert_to_db
from .language import lang_select

groups = ['groups/2211822782398855/', 'groups/2026455020772994/', 'groups/845200752357548/', 'groups/1740604889358330/',
 'groups/338423746281737/', 'groups/874688095898939/', 'groups/1582217401814407/', 'groups/382456881949463/',
 'groups/1890930314468568/', 'groups/1771965776387013/', 'groups/1014264832048605/', 'groups/309047892893889',
 'groups/655176181267328/', 'groups/1199935466721864/', 'groups/954727157912378/', 'groups/449533238580169',
 'groups/588658644615604/', 'groups/385948635085856/', 'groups/drushim.hadera/', 'groups/339190266829/',
 'groups/1018383334921121/', 'groups/1901145279916413/', 'groups/1615308748781246/', 'groups/avodot']


def init_fb_scraper(app):
    app.fb_scrab_time = datetime.datetime(2021, 5, 31)

    @app.route("/fb_scrap", methods=["GET"])
    def fb_scrap():
        fb_delay = datetime.datetime.now() - app.fb_scrab_time
        if fb_delay.total_seconds() < 7200:  # 2 hours
            return redirect('fb_work_posts')


        data = []
        scraper_options = {"comments": False, "reactors": True, "allow_extra_requests": False, "posts_per_page": 80}
        for group in groups:
            for post in get_posts(group, pages=1, options=scraper_options):
                searcher = []
                try:
                    if bool(re.search(r'מחפש* עבודה', post['text'])) or bool(re.search(r'ищу* работу', post['text'])):
                        # print(post['text'][:20], '\n', post['post_url'])
                        for col in cols_fb_work[1:-1]:
                            if col == 'time':
                                searcher.append(post[col].timestamp())
                            elif col == 'group_name':
                                pass
                                searcher.append(get_group_info(group.split('/')[1])['name'])
                            else:
                                searcher.append(post[col])
                        searcher.append(0)
                        data.append(searcher)
                except:
                    pass
            sleep(0.5)
        if len(data) > 0:
            # print('len',len(data))
            insert_to_db('post_work', cols_fb_work[1:], data, DB_ROOT)
        app.fb_scrab_time = datetime.datetime.now()

        return redirect('/fb_work_posts')


    @app.route("/fb_work_posts")
    def fb_work_posts():
        columns = [0,1,3,4,5,6,7]
        con = sql.connect(DB_ROOT)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT " + ', '.join(cols_fb_work) + " FROM post_work ORDER BY processed ASC, time DESC")
        data = [dict(x) for x in cur.fetchall()]

        if len(data) > 0:
            for dd in data:
                dd['time'] = read_tstamp(dd['time'])

        con.close()
        # Language selector
        cols_names, button_names = lang_select(app.lang, 'workers')
        fb_delay = datetime.datetime.now() - app.fb_scrab_time
        if fb_delay.total_seconds() > 7200:  # 2 hours
            fb_delay = True
        else: fb_delay = False
        return render_template('facebook/work_posts.html', data=data, data_cols=list(cols_fb_work[columns]),
                               col_names=list(cols_fb_work[columns]), b_names=button_names, fb_delay=fb_delay)

    # change check status to record
    @app.route('/fb_searcher_check/<int:id>/<int:val>/')
    def fb_searcher_check(id, val):
        try:
            con = sql.connect(DB_ROOT)
            command = f'UPDATE post_work SET processed = {val} WHERE post_work.id = {id}'
            cur = con.cursor()
            cur.execute(command)
            con.commit()

        except Exception as ex:
            con.rollback()
            print('record not updated:', ex)

        finally:
            con.close()
            return redirect('/fb_work_posts')

    return app

