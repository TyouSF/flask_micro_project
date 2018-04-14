# *-* coding: utf-8 *-*

from flask import Flask, render_template, g
import config
from views import master, publicview
from dmodel.dbhelper import init_db


app = Flask(__name__)

# 加载配置文件
app.config.from_object(config.DebugTest)


# 根据上下文回话关闭数据库连接
@app.teardown_appcontext
def close_db(error):
    '''
    程序实例销毁时，自动关闭数据库连接
    '''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# 管理员 master 蓝图
app.register_blueprint(master.master, url_prefix='/admin')

# 公共页 public 蓝图
app.register_blueprint(publicview.public_view, url_prefix='/public')


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run()
