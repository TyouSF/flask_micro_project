# *_* codinf: utf-8 *_*
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from datetime import datetime
from dmodel.dbhelper import insert_db, get_db, query_db
import os
from werkzeug.utils import secure_filename  # 校验图片名


public_view = Blueprint('public_view', __name__)


# 存储图片方法
def save_img(imgfile):
    if not os.path.exists(current_app.config['IMG_SAVED_PATH']):
        os.mkdir(current_app.config['IMG_SAVED_PATH'])
    imgfile.filename = datetime.timestamp(datetime.now())
    return imgfile.filename


# 校验图片格式方法
def allowed_img(filename):
    if filename == '':
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['IMG_ALLOWED_EXTENSIONS']


# 公共提交问题页面
@public_view.route('/issue/submit/', methods=['GET', 'POST'])
def issue_submit():
    status_lists = query_db("select id, status, remark from IssueStatus")
    if request.method == 'POST':
        title = request.form.get('title', None)
        intro = request.form.get('intro', None)
        customer = request.form.get('customer', None)
        contact = request.form.get('contact', None)
        statusid = 1    # 新提交问题，默认状态均为 1 Open
        createdtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'imgfile' in request.files:
            imgfile = request.files['imgfile']
            filename = secure_filename(imgfile.filename)
            if imgfile and allowed_img(imgfile.filename):
                flash('图片格式正确')
                return redirect(url_for('public_view.issue_submit'))
            else:
                imgfile.name = save_img(imgfile)
                flash(imgfile.filename)
                return redirect(url_for('public_view.issue_submit'))
        if not (title and intro and customer and contact):
            flash('请填写所有必填项')
            return redirect(url_for('public_view.issue_submit'))
        r = insert_db("insert into Issues(title, intro, customer, contact, statusid, createdtime) values (?,?,?,?,?,?)",
                      (title, intro, customer, contact, statusid, createdtime)
                      )
        if not r:
            flash('出了点小状况，提交失败，请重试')
            return redirect(url_for('public_view.issue_submit'))
        flash('问题已成功提交')
        return redirect(url_for('public_view.issue_submit'))
    return render_template('public/issuesubmit.html', status_lists=status_lists)
