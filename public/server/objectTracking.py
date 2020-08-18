import cv2
import csv
import numpy as np
import predict
import webbrowser
import os
import mysql.connector

from getFeatures import getFeatures
from estimateAllTranslation import estimateAllTranslation
from applyGeometricTransformation import applyGeometricTransformation
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image

import xml.etree.ElementTree as ET

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def objectTracking(rawVideo,length,fn,sid,draw_bb=False, play_realtime=False, save_to_file=False):
    # initialize
    print('========= Object tracking')
    
    # create the file structure
    annotation = ET.Element('annotation')
    folder = ET.SubElement(annotation, 'folder')
    filename = ET.SubElement(annotation, 'filename')
    folder.text = 'not available'
    filename.text = 'not available'
    source = ET.SubElement(annotation, 'source')
    typ = ET.SubElement(source, 'type')
    sourceImage = ET.SubElement(source, 'sourceImage')
    sourceAnnotation = ET.SubElement(source, 'sourceAnnotation')
    typ.text = 'video'
    sourceImage.text = 'vatic frames'
    sourceAnnotation.text = 'vatic'
    
    n_frame = length-10
    count=0
    frames = np.empty((n_frame,),dtype=np.ndarray)
    frames_draw = np.empty((n_frame,),dtype=np.ndarray)
    bboxs = np.empty((n_frame,),dtype=np.ndarray)
    print(bboxs.shape)
    for frame_idx in range(n_frame):
        _, frames[frame_idx] = rawVideo.read()
        if frames[frame_idx] is None:
            break
        cv2.imwrite( "/var/www/html/data/Video_Frames/frame%d.png" % count, frames[frame_idx])     # save frame as JPEG file
        count=count+1
    n_frame=count
    print("n frame count = " , n_frame)
    
    count=0
    count1=0
    out=[]
    for frame_idx in range(0,n_frame-10,10):
        print("== frame_idx = " + str(frame_idx))
        filename= "/var/www/html/data/Video_Frames/frame%d.png" % frame_idx
        labels,pixels = predict.return_pixels(filename)
        n_object= len(pixels)
        print(n_object)
        print(len(labels))
        bboxs[frame_idx] = np.empty((n_object,4,2), dtype=float)
        for o in range(0,n_object):
            print("object #", o)

            xmn=pixels[o][0]
            xmx=pixels[o][1]
            ymn=pixels[o][2]
            ymx=pixels[o][3]

            im = Image.open(filename) 
            region = im.crop((xmn, ymn, xmx, ymx))
            region.save("/var/www/html/data/Object_Store/"+fn+"/sentence_%s"%sid+"/frame_%d"%frame_idx+"_object_%d"%o+".png")
            object_path="/var/www/html/data/Object_Store/"+fn+"/sentence_%s"%sid+"/frame_%d"%frame_idx+"_object_%d"%o+".png"
            file=open("/var/www/html/data/Object_Store/object_annotations.csv","a+")
            wrtr= csv.writer(file)
            wrtr.writerow([object_path,labels[o]])
            file.close()

            bboxs[frame_idx][o,:,:] = np.array([[xmn,ymn],[xmx,ymn],[xmn,ymx],[xmx,ymx]]).astype(float)

            conn = mysql.connector.connect(
              host="db",
              user="webtool",
              password="webtool",
              database="webtool_db"
            )
            v=1
            
            mySql_insert_query = "INSERT INTO objectmm (name, startFrame, endFrame, status, idAnnotationSetMM) VALUES ('frame%d_"%frame_idx+"object%d_"%o+labels[o]+"',%d"%frame_idx+",%d"%(frame_idx+9)+",%d"%v+",%d"%1+")"
            print(mySql_insert_query)
            cursor = conn.cursor()
            cursor.execute(mySql_insert_query)
            conn.commit()
            print(cursor.rowcount, "Record inserted successfully into ObjectMM table")
            cursor.close()
            conn.close()
    
        out.append(cv2.VideoWriter('/var/www/html/data/Output/output.mp4',cv2.VideoWriter_fourcc(*'mp4v'),1,(frames[frame_idx].shape[1],frames[frame_idx].shape[0])))

        print("End objects generation")

        startXs,startYs = getFeatures(cv2.cvtColor(frames[frame_idx],cv2.COLOR_RGB2GRAY),bboxs[frame_idx],use_shi=False)
        if startXs.all()==-1 and startYs.all()==-1:
            continue
        else:
            for i in range(frame_idx+1,frame_idx+10):
                print('Processing Frame',i)
                newXs, newYs = estimateAllTranslation(startXs, startYs, frames[i-1], frames[i])
                Xs, Ys ,bboxs[i] = applyGeometricTransformation(startXs, startYs, newXs, newYs, bboxs[i-1])

                print(bboxs[i])

                # update coordinates
                startXs = Xs
                startYs = Ys

                # update feature points as required
                n_features_left = np.sum(Xs!=-1)
                print('# of Features: %d'%n_features_left)
                if (n_features_left > 0) and (n_features_left < 15):
                    print('Generate New Features')
                    startXs,startYs = getFeatures(cv2.cvtColor(frames[i],cv2.COLOR_RGB2GRAY),bboxs[i])

                # draw bounding box and visualize feature point for each object
                frames_draw[i] = frames[i].copy()
                for j in range(0,n_object):
                    (xmin, ymin, boxw, boxh) = cv2.boundingRect(bboxs[i][j,:,:].astype(int))
                    frames_draw[i] = cv2.rectangle(frames_draw[i], (xmin,ymin), (xmin+boxw,ymin+boxh), (255,0,0), 2)
                    for k in range(startXs.shape[0]):
                        frames_draw[i] = cv2.circle(frames_draw[i], (int(startXs[k,j]),int(startYs[k,j])),3,(0,0,255),thickness=2)

                # imshow if to play the result in real time
                if play_realtime:
                    cv2.imshow("win",frames_draw[i])
                    cv2.waitKey(10)
                out[count].write(frames_draw[i])

            cv2.destroyAllWindows()
            out[count].release()
            count=count+1
            new = 2
            url = "http://docker.internal.host:8600/server/track_objects.php"
            print("ending " + url)
            webbrowser.open(url,new=new)


            # loop the resulting video (for debugging purpose only)
            # while 1:
            #     for i in range(1,n_frame):
            #         cv2.imshow("win",frames_draw[i])
            #         cv2.waitKey(50)
            
    count1=0
    for frame_idx in range(0,n_frame-10,10):
        filename= "/var/www/html/data/Video_Frames/frame%d.png" % frame_idx
        labels,pixels = predict.return_pixels1(filename)
                
        n_object= len(pixels)
        
        for o in range(0,n_object):

            obj = ET.SubElement(annotation,'object')
            name = ET.SubElement(obj, 'name')
            moving = ET.SubElement(obj, 'moving')
            action = ET.SubElement(obj, 'action')
            verified = ET.SubElement(obj, 'verified')
            id1 = ET.SubElement(obj, 'id')
            createdFrame = ET.SubElement(obj, 'createdFrame')
            startFrame = ET.SubElement(obj, 'startFrame')
            endFrame = ET.SubElement(obj, 'endFrame')
            name.text=labels[o]
            moving.text='true'
            verified.text='0'

            count1=count1+1
            
            id1.text=str(count1)
            createdFrame.text='0'
            startFrame.text= str(frame_idx)
            endFrame.text= str(frame_idx+10)

            for j in range(frame_idx,frame_idx+10):

                if bboxs[j][o][0,0]<0:
                    bboxs[j][o][0,0]=0.0
                if bboxs[j][o][0,1]<0:
                    bboxs[j][o][0,1]=0.0
                if bboxs[j][o][1,0]<0:
                    bboxs[j][o][1,0]=0.0
                if bboxs[j][o][1,1]<0:
                    bboxs[j][o][1,1]=0.0
                if bboxs[j][o][2,0]<0:
                    bboxs[j][o][2,0]=0.0
                if bboxs[j][o][2,1]<0:
                    bboxs[j][o][2,1]=0.0
                if bboxs[j][o][3,0]<0:
                    bboxs[j][o][3,0]=0.0
                if bboxs[j][o][3,1]<0:
                    bboxs[j][o][3,1]=0.0
                
                if math.isnan(bboxs[j][o][3,0]) or math.isnan(bboxs[j][o][3,1]) or math.isnan(bboxs[j][o][2,0]) or math.isnan(bboxs[j][o][2,1]) or math.isnan(bboxs[j][o][1,0]) or math.isnan(bboxs[j][o][1,1]) or math.isnan(bboxs[j][o][0,0]) or math.isnan(bboxs[j][o][0,1]):
                    break
                polygon= ET.SubElement(obj, 'polygon')
                t= ET.SubElement(polygon,'t')
                t.text= str(j)
                pt= ET.SubElement(polygon,'pt')
                x= ET.SubElement(pt,'x')
                y= ET.SubElement(pt,'y')
                l= ET.SubElement(pt,'l')
                x.text=str(int(bboxs[j][o][0,0]))
                y.text=str(int(bboxs[j][o][0,1]))
                if j==frame_idx:
                    l.text='1'
                else:
                    l.text='0'
                pt= ET.SubElement(polygon,'pt')
                x= ET.SubElement(pt,'x')
                y= ET.SubElement(pt,'y')
                l= ET.SubElement(pt,'l')
                x.text=str(int(bboxs[j][o][2,0]))
                y.text=str(int(bboxs[j][o][2,1]))
                if j==frame_idx:
                    l.text='1'
                else:
                    l.text='0'
                pt= ET.SubElement(polygon,'pt')
                x= ET.SubElement(pt,'x')
                y= ET.SubElement(pt,'y')
                l= ET.SubElement(pt,'l')
                x.text=str(int(bboxs[j][o][3,0]))
                y.text=str(int(bboxs[j][o][3,1]))
                if j==frame_idx:
                    l.text='1'
                else:
                    l.text='0'
                pt= ET.SubElement(polygon,'pt')
                x= ET.SubElement(pt,'x')
                y= ET.SubElement(pt,'y')
                l= ET.SubElement(pt,'l')
                x.text=str(int(bboxs[j][o][1,0]))
                y.text=str(int(bboxs[j][o][1,1]))
                if j==frame_idx:
                    l.text='1'
                else:
                    l.text='0'

    # create a new XML file with the results
    indent(annotation)
    mydata = ET.tostring(annotation)
    myfile = open("/var/www/html/data/annotations.xml", "wb")
    myfile.write(mydata)

def objectTracking1(rawVideo,length,fn,draw_bb=False, play_realtime=False, save_to_file=False):
    # initialize
    n_frame = length-10
    count=0
    frames = np.empty((n_frame,),dtype=np.ndarray)
    frames_draw = np.empty((n_frame,),dtype=np.ndarray)
    bboxs = np.empty((n_frame,),dtype=np.ndarray)
    print(bboxs.shape)
    for frame_idx in range(n_frame):
        _, frames[frame_idx] = rawVideo.read()
        cv2.imwrite( "/var/www/html/data/Video_Frames/frame%d.png" % count, frames[frame_idx])     # save frame as JPEG file
        count=count+1

    count=0
    out=[]
    for frame_idx in range(0,n_frame-10,10):
        labels=[]
        n_object = int(input("Number of objects to track:"))
        bboxs[frame_idx] = np.empty((n_object,4,2), dtype=float)
        for o in range(0,n_object):
            (xmin, ymin, boxw, boxh) = cv2.selectROI("Select Object %d"%(o),frames[frame_idx])
            cv2.destroyWindow("Select Object %d"%(o))
            bboxs[frame_idx][o,:,:] = np.array([[xmin,ymin],[xmin+boxw,ymin],[xmin,ymin+boxh],[xmin+boxw,ymin+boxh]]).astype(float)
            filename= "/var/www/html/data/Video_Frames/frame%d.png" % frame_idx
            im = Image.open(filename) 
            region = im.crop((xmin, ymin, xmin+boxw, ymin+boxh))
            region.save("/var/www/html/data/Object_Store/frame_%d"%frame_idx+"_object_%d"%o+".png")
            object_path="/var/www/html/data/Object_Store/frame_%d"%frame_idx+"_object_%d"%o+".png"
            file=open("/var/www/html/data/Object_Store/object_annotations.csv","a+")
            wrtr= csv.writer(file)
            label=input("Enter object label")
            labels.append(label)
            wrtr.writerow([object_path,labels[o]])
            file.close()

        out.append(cv2.VideoWriter('/var/www/html/data/Output/output.mp4',cv2.VideoWriter_fourcc(*'mp4v'),1,(frames[frame_idx].shape[1],frames[frame_idx].shape[0])))

        v=1
            
        mySql_insert_query = "INSERT INTO objectmm (name, startFrame, endFrame, status, idAnnotationSetMM) VALUES ('frame%d_"%frame_idx+"object%d_"%o+labels[o]+"',%d"%frame_idx+",%d"%(frame_idx+9)+",%d"%v+",%d"%1+")"
        print(mySql_insert_query)
        cursor = conn.cursor()
        cursor.execute(mySql_insert_query)
        conn.commit()
        print(cursor.rowcount, "Record inserted successfully into ObjectMM table")
        cursor.close()
        conn.close()

        startXs,startYs = getFeatures(cv2.cvtColor(frames[frame_idx],cv2.COLOR_RGB2GRAY),bboxs[frame_idx],use_shi=False)
        if startXs.all()==-1 and startYs.all()==-1:
            continue
        else:
            for i in range(frame_idx+1,frame_idx+10):
                print('Processing Frame',i)
                newXs, newYs = estimateAllTranslation(startXs, startYs, frames[i-1], frames[i])
                Xs, Ys ,bboxs[i] = applyGeometricTransformation(startXs, startYs, newXs, newYs, bboxs[i-1])
                
                # update coordinates
                startXs = Xs
                startYs = Ys

                # update feature points as required
                n_features_left = np.sum(Xs!=-1)
                print('# of Features: %d'%n_features_left)
                if (n_features_left > 0) and (n_features_left < 15):
                    print('Generate New Features')
                    startXs,startYs = getFeatures(cv2.cvtColor(frames[i],cv2.COLOR_RGB2GRAY),bboxs[i])

                # draw bounding box and visualize feature point for each object
                frames_draw[i] = frames[i].copy()
                for j in range(0,n_object):
                    (xmin, ymin, boxw, boxh) = cv2.boundingRect(bboxs[i][j,:,:].astype(int))
                    frames_draw[i] = cv2.rectangle(frames_draw[i], (xmin,ymin), (xmin+boxw,ymin+boxh), (255,0,0), 2)
                    for k in range(startXs.shape[0]):
                        frames_draw[i] = cv2.circle(frames_draw[i], (int(startXs[k,j]),int(startYs[k,j])),3,(0,0,255),thickness=2)
                
                # imshow if to play the result in real time
                if play_realtime:
                    cv2.imshow("win",frames_draw[i])
                    cv2.waitKey(10)
                out[count].write(frames_draw[i])
            
            out[count].release()

            new = 2
            url = "http://charon.local:8600/server/track_objects.php"
            webbrowser.open(url,new=new)


            # loop the resulting video (for debugging purpose only)
            # while 1:
            #     for i in range(1,n_frame):
            #         cv2.imshow("win",frames_draw[i])
            #         cv2.waitKey(50)

def detect_and_track(filename,start_time,end_time,val=0):
    print('========= Detect and Tracking')
    arr1=start_time.split('.')
    arr2=end_time.split('.')
    st= int(arr1[0])
    et= int(arr2[0])+1
    targetname = "/var/www/html/data/Output/test.mp4"
    ffmpeg_extract_subclip(filename, st, et, targetname)
    cap = cv2.VideoCapture(targetname)
    arr=filename.split('/')
    fn_arr=arr[2].split('.')
    fn=fn_arr[0]
    print(fn)
    length= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if val==0:
        objectTracking(cap,length,fn,draw_bb=True,play_realtime=False,save_to_file=True)
    if val==1:
        objectTracking1(cap,length,fn,draw_bb=True,play_realtime=False,save_to_file=True)
    cap.release()

#detect_and_track("Video_Store/full/2bfb129dea9d7d149b79b7bbc96f9d4eb037f8bd.mp4","10.00","20.00",0)
