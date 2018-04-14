# *-* coding: utf-8 *-*

import os

config_root_path = os.path.split(os.path.abspath(__name__))[0]


class DebugTest:
    '''
    开发调试使用的配置类
    '''
    DEBUG = True
    SECRET_KEY = 'debugtest'
    DATABASE_URL = os.path.join(config_root_path, r'dmodel/niffler.db')
    IMG_SAVED_PATH = os.path.join(config_root_path, 'imgs')
    IMG_ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png')
