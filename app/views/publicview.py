# *_* codinf: utf-8 *_*
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from datetime import datetime
from dmodel.dbhelper import insert_db, get_db, query_db
import os
from werkzeug.utils import secure_filename  # 校验图片名


public_view = Blueprint('public_view', __name__)


# 重命名图片名：以时间戳命名
def new_imgfile_name(imgfile):
    if '.' in secure_filename(imgfile.filename):
        extension = secure_filename(imgfile.filename).rsplit('.', 1)[1]
    else:
        extension = secure_filename(imgfile.filename)
    new_filename = str(datetime.now().timestamp()) + '.' + extension
    return new_filename


# 保存图片方法
def save_img(imgfile, filename):
    if not os.path.exists(current_app.config['IMG_SAVED_PATH']):
        os.mkdir(current_app.config['IMG_SAVED_PATH'])
    imgfile.save(os.path.join(current_app.config['IMG_SAVED_PATH'], filename))
    return True


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
        imgurl = False  # 未添加图片是，图片路径默认 Fasle
        if 'imgfile' in request.files:
            imgfile = request.files['imgfile']
            if imgfile.filename == '':
                flash('未正确选择图片')
                return redirect(url_for('public_view.issue_submit'))
            if imgfile and allowed_img(filename=imgfile.filename):
                imgurl = new_filename = new_imgfile_name(imgfile)
            else:
                flash('图片格式不符')
                return redirect(url_for('public_view.issue_submit'))
        if not (title and intro and customer and contact):
            flash('请填写所有必填项')
            return redirect(url_for('public_view.issue_submit'))
        if imgurl:
            r = insert_db("insert into Issues(title, intro, customer, contact, statusid, imgurl, createdtime) values (?,?,?,?,?,?,?)",
                          (title, intro, customer, contact,
                           statusid, imgurl, createdtime)
                          )
            save_img(imgfile=imgfile, filename=new_filename)
        else:
            r = insert_db("insert into Issues(title, intro, customer, contact, statusid, createdtime) values (?,?,?,?,?,?)",
                          (title, intro, customer, contact, statusid, createdtime)
                          )
        if not r:
            flash('出了点小状况，提交失败，请重试')
            return redirect(url_for('public_view.issue_submit'))
        flash('问题已成功提交')
        return redirect(url_for('public_view.issue_submit'))
    return render_template('public/issuesubmit.html', status_lists=status_lists)
