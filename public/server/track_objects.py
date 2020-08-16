from flask import Flask,render_template,request
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

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

PATH_TO_VIDEO_DIR = config.get("charon", "dataPath") + 'Video_Store/full/'
print(PATH_TO_VIDEO_DIR)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route('/track',methods=['GET','POST'])
def track():
   fnames=os.listdir(PATH_TO_VIDEO_DIR)
   fnames=sorted(fnames)
   filename=fnames[0]
   start_time=request.form['start_time']
   end_time=request.form['end_time']
   print(PATH_TO_VIDEO_DIR)
   video_path=os.path.join(PATH_TO_VIDEO_DIR,filename)
   print(video_path)
   v=0
   #extract video clip from timestamps
   objectTracking.detect_and_track(video_path,start_time,end_time,v)

   val=input("Enter yes if satisfied with detected objects and no to create and track own objects...")
   if val=="no":
      v=1
      objectTracking.detect_and_track(video_path,start_time,end_time,v)
   return 'ok'

if __name__=='__main__':
    app.run(debug=False, host='0.0.0.0')


