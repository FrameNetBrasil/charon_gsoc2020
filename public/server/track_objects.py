#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import objectTracking
import sys
import time
import webbrowser
from PIL import Image
import os
import configparser
import io
import shutil
import urllib.request

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

DATA_PATH = config.get("charon", "dataPath")

PATH_TO_VIDEO_DIR =  DATA_PATH + 'Video_Store/full/'
print(PATH_TO_VIDEO_DIR)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return jsonify('hello')

@app.route('/frames', methods=['GET', 'POST'])
def frames():
    url_video = request.json['url_video']
    print(url_video)
    filename = PATH_TO_VIDEO_DIR + url_video.split('/')[-1]
    print(filename)

    with urllib.request.urlopen(url_video) as data:
        with open(filename, "wb") as out:
            shutil.copyfileobj(data, out)

    sha1 = url_video.split('/')[-1].split('.')[-2]
    print(sha1)
    os.chdir(DATA_PATH + 'Video_Frames')
    if os.path.isdir(sha1) == True:
        shutil.rmtree(sha1)
    os.mkdir(sha1)
    os.chdir(DATA_PATH + 'Video_Frames')

    frames = objectTracking.generate_frames(filename, DATA_PATH + 'Video_Frames/' + sha1)

    response = jsonify({"frames": frames})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/track', methods=['GET', 'POST'])
def track():
    url_video = request.json['url_video']
    print(url_video)
    sha1 = url_video.split('/')[-1].split('.')[-2]
    print(sha1)
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    idSentence = request.json['idSentence']

    # extract video clip from timestamps
    os.chdir(DATA_PATH + 'Object_Store')
    if os.path.isdir(sha1) == False:
        os.mkdir(sha1)
    os.chdir(sha1)
    if os.path.isdir("sentence_" + idSentence) == True:
        shutil.rmtree("sentence_" + idSentence)
    os.mkdir("sentence_" + idSentence)
    os.chdir(DATA_PATH + 'Object_Store')

    frames_path = DATA_PATH + 'Video_Frames/' + sha1
    objects_path = DATA_PATH + 'Object_Store/' + sha1
    vatic = objectTracking.detect_and_track(frames_path, objects_path, start_time, end_time, idSentence)
    response = jsonify({"sha1": sha1, "vatic": vatic})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
