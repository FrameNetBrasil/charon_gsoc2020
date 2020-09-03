from flask import Flask,render_template,request,jsonify
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
   paths = [os.path.join(PATH_TO_VIDEO_DIR, basename) for basename in fnames]
   filename=max(paths, key=os.path.getctime)
   print(filename)
   fn=filename.split(".")
   f=fn[0].split("/")
   start_time=request.json['start_time']
   end_time=request.json['end_time']
   sid=request.json['sid']
   sid=str(int(sid)-1)
   print(PATH_TO_VIDEO_DIR)
   video_path=filename
   print(video_path)
   v=0
   
   #extract video clip from timestamps
   origdir= config.get("charon", "dataPath")  
   os.chdir(origdir +'Object_Store')
   if os.path.isdir(f[len(f)-1])==False:
      os.mkdir(f[len(f)-1])
   os.chdir(f[len(f)-1])
   if os.path.isdir("sentence_"+sid)==True:
      shutil.rmtree("sentence_"+sid)
   os.mkdir("sentence_"+sid)
   os.chdir(origdir)
   
   #objectTracking.detect_and_track(video_path,sid,start_time,end_time,v)
   objectTracking.detect_and_track(video_path,start_time,end_time, sid)

   #val=input("Enter yes if satisfied with detected objects and no to create and track own objects...")
   #if val=="no":
      #v=1
      #objectTracking.detect_and_track(video_path,start_time,end_time,v)
   return jsonify("See detected objects at /server/display_objects.php and tracking at /server/track_objects.php")

if __name__=='__main__':
    app.run(debug=False, host='0.0.0.0')


