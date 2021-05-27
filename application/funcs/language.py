import os
ROOT_DIR = os.path.abspath(os.path.join( os.path.abspath(__file__), os.pardir, os.pardir))
from application.database.params import (cols_j, cols_j_rus, button_names_j,
                                    cols_w, cols_w_rus, button_names_w,
                                    cols_c, cols_c_rus, button_names_c)

# input app.lang
def lang_select(lang, base='workers'):
    # base selector
    if base == 'workers':
        cols_rus = cols_w_rus
        cols_heb = 0
        cols_eng = cols_w
        buttons = button_names_w
    elif base == 'jobs':
        cols_rus = cols_j_rus
        cols_heb = 0
        cols_eng = cols_j
        buttons = button_names_j
    elif base == 'clients':
        cols_rus = cols_c_rus
        cols_heb = 0
        cols_eng = cols_c
        buttons = button_names_c
    else:
        cols_rus = cols_w_rus
        cols_heb = 0
        cols_eng = cols_w
        buttons = button_names_w

    # Language selector
    if lang == 'rus':
        cols_names = cols_rus
        button_names = buttons['rus']
    elif lang == 'heb':
        cols_names = cols_heb
        button_names = buttons['heb']
    else:
        cols_names = cols_eng
        button_names = buttons['eng']
    return cols_names, button_names