# *-* coding: utf-8 *-*

from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from dmodel.dbhelper import get_db, query_db, insert_db
from datetime import datetime
from functools import wraps


# master 蓝图
master = Blueprint('master', __name__)


# 通用校验登录状态方法
def login_required(func):
    '''
    校验登录状态
    '''
    @wraps(func)
    def wrapper():
        if not session.get('login_status'):
            return redirect(url_for('master.sign_in'))
        return func()
    return wrapper


# 登录页面
@master.route('/signin/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if not (username and password):
            flash('登录信息有误')
            return redirect(url_for('master.sign_in'))
        r = query_db("select * from Users where username=? and password=?",
                     (username, password),
                     one=True)
        if not r:
            flash('帐号或密码有误')
            return redirect(url_for('master.sign_in'))
        session['login_status'] = True
        return redirect(url_for('master.admin_home'))
    # return current_app.config['IMG_SAVED_PATH']
    return render_template('admin/signin.html')


# 注册页
@master.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        phone = request.form.get('phone', None)
        createdtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not (username and password):
            flash('登录昵称或密码不能为空')
            return redirect(url_for('master.sign_up'))
        else:
            r = query_db('select * from Users where username=?',
                         (username,),
                         one=True)
            if r:
                flash('帐号已存在')
                return redirect(url_for('master.sign_up'))
        r = insert_db("insert into Users(username, password, email, phone, createdtime) values(?,?,?,?,?)",
                      (username, password, email, phone, createdtime)
                      )
        if not r:
            flash('注册信息有误，请重新填写')
            return redirect(url_for('master.sign_up'))
        session['login_status'] = True
        return redirect(url_for('master.admin_home'))
    return render_template('admin/signup.html')


# 注销登录
@master.route('/signout/')
def sign_out():
    session.pop('login_status', None)
    return redirect(url_for('master.sign_in'))


# 后台管理首页-需要登录
@master.route('/home/', methods=['GET'])
@login_required
def admin_home():
    issue_lists = query_db("select Issues.title, Issues.customer, Issues.contact, Issues.createdtime, IssueStatus.status \
                            from Issues LEFT JOIN IssueStatus ON Issues.statusid=IssueStatus.id")
    return render_template('admin/home.html', issue_lists=issue_lists)


# 后台管理 Issue 状态增加-需登录
@master.route('/issue/status', methods=['GET', 'POST'])
@login_required
def issue_status():
    if request.method == 'POST':
        status = request.form.get('status', None)
        remark = request.form.get('remark', None)
        createdtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not (status and remark):
            flash('信息填写不完整')
            return redirect(url_for('master.issue_status'))
        r = query_db("select status from IssueStatus where status=?", [
                     status], one=True)
        if r:
            flash('该状态已存在')
            return redirect(url_for('master.issue_status'))
        rv = insert_db("insert into IssueStatus(status, remark, createdtime) values (?,?,?)",
                       (status, remark, createdtime)
                       )
        if not rv:
            flash('执行异常')
            return redirect(url_for('master.issue_status'))
        flash('添加成功')
        return redirect(url_for('master.issue_status'))
    return render_template('admin/issuestatus.html')


# 查看所有的问题状态-需登录
@master.route('/issue/status/lists')
@login_required
def issue_status_lists():
    status_lists = query_db(
        "select status, remark, createdtime, editedtime from IssueStatus")
    return render_template('admin/statuslist.html', status_lists=status_lists)
