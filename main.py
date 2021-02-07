from flask import Flask, request, abort, render_template, send_file, Response, jsonify, make_response
from flask_cors import CORS
from flask_socketio import SocketIO
import threading
#import base64

#from face_detect import get_facepos
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
#app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
#app.config['UPLOAD_FOLDER'] = './tmp'
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
    return render_template('aioshaku.html')

@app.route('/oshaku')
def oshaku():
    #serve =  request.args.get('serve', default = 1, type = int)
    #aikotoba =  request.args.get('aikotoba', default = '')
    #return render_template('oshaku.html', apikey=SKYWAY_APIKEY, serve=serve, aikotoba=aikotoba)
    return render_template('aioshaku.html')

'''
@app.route("/ehon", methods=['GET'])
def ehon():
    return render_template('ehon.html')

@app.route("/api/face", methods=['POST'])
def face():
    img = request.files['image']
    name = img.filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    img.save(path)
    face_pos = get_facepos(path)
    return jsonify(face_pos)
'''

@app.route("/api/answer", methods=['POST'])
def answer():
    return jsonify({})


# Flaskを使用してサーバーを起動
if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    socketio.run(app, host="0.0.0.0", port=port)

