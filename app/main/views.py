import os
from datetime import time, datetime

from flask import render_template, request, session, redirect, Response
from . import main
from .. import db
from ..models import *

@main.route('/')
def index_views():
    files = os.listdir('./app/static/upload/')
    type_video = ['mpeg','mpg','dat','avi','mov','asf','wmv','flv','f4v','rmvb','mp4']
    type_imgs = ['bmp','jpg','jpeg','png','pcd','psd','dxf','tiff','pcx','gif']
    type_word = ['log','doc','docx','txt','pdf','wps','wpt','dot','rtf','dotx','docm','dotm','xls','xlt','xltx','xltm','xlsx','xlsm','xml','html','htm','mhtml','mht','txt','csv','chm','wdl','ppt'
]
    type_audio = ['wav','mp3','mp3pro','midi','wma','mp4','md','cda','sacd','quicktime','vqf','dvdaudio','realaudio','voc','au','aiff','amiga','mac','s48','aac']
    video = []
    imgs = []
    words = []
    audio = []
    pc_wares = []
    android = []
    apple = []
    other = []
    for f in files:
        if f.split('.')[-1].lower() in type_video:
            video.append(f.split('.')[0])
        elif f.split('.')[-1].lower() in type_imgs:
            imgs.append(f.split('.')[0])
        elif f.split('.')[-1].lower() in type_word:
            words.append(f.split('.')[0])
        elif f.split('.')[-1].lower() in type_audio:
            audio.append(f.split('.')[0])
        elif f.split('.')[-1].lower() == 'ipa':
            apple.append(f.split('.')[0])
        elif f.split('.')[-1].lower() == 'apk':
            android.append(f.split('.')[0])
        elif f.split('.')[-1].lower() == 'exe' or 'dmp':
            pc_wares.append(f.split('.')[0])
        else:
            other.append(f)
    if 'uid' in session and 'uname' in session:
        user = User.query.filter_by(ID=session.get('uid')).first()
    video = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), video)
    imgs = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), imgs)
    words = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), words)
    other = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), other)
    audio = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), audio)
    apple = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), apple)
    pc_wares = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), pc_wares)
    android = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), android)
    return render_template('index.html',params=locals())

@main.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    def send_chunk():
        store_path = '../app/static/upload/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')

@main.route('/file/upload', methods=['POST'])
def upload_part():
    task = request.form.get('task_id')
    chunk = request.form.get('chunk', 0)
    filename = '%s%s' % (task, chunk)

    upload_file = request.files['file']
    upload_file.save('./app/static/upload/%s' % filename)
    return render_template('release.html')

@main.route('/file/merge', methods=['GET'])
def upload_success():
    target_filename = request.args.get('filename')
    task = request.args.get('task_id')
    chunk = 0
    with open('./app/static/upload/%s' % target_filename, 'wb') as target_file:
        while True:
            try:
                filename = './app/static/upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')
                target_file.write(source_file.read())
                source_file.close()
            except IOError:
                break

            chunk += 1
            os.remove(filename)

    return render_template('release.html')

@main.route('/release',methods=['GET'])
def release_views():
    if request.method == 'GET':
        return render_template('release.html')

@main.route('/login',methods=['POST','GET'])
def login_views():
    if request.method == 'GET':
        if 'uid' in session and 'uname' in session:
            user = User.query.filter_by(ID=session.get('uid')).first()
            return redirect('/')
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(loginname=username,upwd=password).first()
    if user:
        session['uid'] = user.ID
        session['uname'] = user.uname
        return redirect('/')
    else:
        errMsg = '用户名或密码错误'
        return render_template('login.html',errMsg=errMsg)

@main.route('/logout')
def logout_views():
    if 'uid' in session and 'uname' in session:
        del session['uid']
        del session['uname']
    return redirect('/')

@main.route('/register',methods=['POST','GET'])
def register_views():
    if request.method == 'GET':
        return render_template('register.html')
    loginname = request.form['loginname']
    username = request.form['username']
    password = request.form['password']
    user = User(loginname,username,password)
    db.session.add(user)
    db.session.commit()
    session['uname'] = user.uname
    session['uid'] = user.ID
    return redirect('/')

