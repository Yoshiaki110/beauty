from flask import Flask, request, abort, render_template, send_file, Response, jsonify, make_response
from flask_cors import CORS
from flask_socketio import SocketIO
import ftplib
import threading
import base64

from face_detect import get_facepos
import os
import json
import uuid
import time
import glob
import shutil
from zipfile import ZipFile


app = Flask(__name__)
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False     # jsonifyでのエラーを抑止するため
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = './tmp'
socketio = SocketIO(app, async_mode=None)
#postConfirm = True

# 環境変数取得
SKYWAY_APIKEY = os.environ["SKYWAY_APIKEY"]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adviser')
def adviser():
    return render_template('video.html', apikey=SKYWAY_APIKEY, peerid='adviser')

@app.route('/user')
def user():
    return render_template('video.html', apikey=SKYWAY_APIKEY, peerid='user')

@app.route('/enkaku')
def enkaku():
    #return render_template('enkaku.html')
    #return render_template('aioshaku.html')
    return render_template('mtg.html')

@app.route('/oshaku')
def oshaku():
    #serve =  request.args.get('serve', default = 1, type = int)
    #aikotoba =  request.args.get('aikotoba', default = '')
    #return render_template('oshaku.html', apikey=SKYWAY_APIKEY, serve=serve, aikotoba=aikotoba)
    #return render_template('aioshaku.html')
    return render_template('mtg.html')


@app.route("/ehon", methods=['GET'])
def ehon():
    return render_template('ehon.html')

@app.route("/api/face", methods=['POST'])
def face():
    print("** /api/face start")
    img = request.files['image']
    name = img.filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    img.save(path)
    face_pos = get_facepos(path)
    print(face_pos)
    print("** /api/face end")
    return jsonify(face_pos)


@app.route("/api/answer", methods=['POST'])
def answer():
    return jsonify({})

@app.route("/sendgrid/webhook", methods=['POST'])
def sendgrid_webhook():
    json_list = request.get_json()
    for data in json_list:
        dumped = dumps(data)
        print(dumped)
    return ""


# ブラウザからの画像のアップロード
@app.route('/ftp/put', methods=['POST'])
def ftp_put():
    server = request.form['server']
    if '' == server:
        return render_template("ftpresult.html", result='サーバ未指定', file_list=[])
    userid = request.form['userid']
    password = request.form['password']
    print(userid)
    ftp = ftplib.FTP(server)
    try:
        ftp.login(userid, password)
    except:
        return render_template("ftpresult.html", result='ログイン失敗（ログイン名、パスワードの誤り）', file_list=[])
    msg = 'リモートファイル一覧'
    if 'uploadFile' in request.files:
        file = request.files['uploadFile']
        fileName = file.filename
        if '' != fileName:
            tmpFileName = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + '.jpeg')
            file.save(tmpFileName)        
            ftp.set_pasv('true')
            with open(tmpFileName, "rb") as f:
                ftp.storbinary('STOR /' + fileName, f)
            msg = 'アップロード成功'
    file_list = ftp.nlst(".")
    
    return render_template("ftpresult.html", result=msg, file_list=file_list)


# Flaskを使用してサーバーを起動
if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    socketio.run(app, host="0.0.0.0", port=port)

