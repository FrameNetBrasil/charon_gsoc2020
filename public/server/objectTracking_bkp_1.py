import cv2
import csv
import numpy as np
import predict
import webbrowser
import os
import mysql.connector
import configparser
import math

from getFeatures import getFeatures
from estimateAllTranslation import estimateAllTranslation
from applyGeometricTransformation import applyGeometricTransformation
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image

import xml.etree.ElementTree as ET

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())
DATA_PATH = config.get("charon", "dataPath")


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def objectTracking(frames_path, objects_path, startFrame, endFrame, idSentence, draw_bb=True, play_realtime=False, save_to_file=True):
    # initialize
    print('========= Object tracking')

    # create the VATIC xml file structure
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

    #get the frames array
    frames = []
    # n_frame (relative)
    n_frame = endFrame - startFrame + 1;
    for frame_idx in range(n_frame):
        actual_idx = frame_idx + startFrame
        frames[frame_idx] = cv2.imread(frames_path + "/frame%d.png" % actual_idx)

    count = 0
    count1 = 0
    out = []
    for frame_idx in range(0, n_frame - 10, 10):
        actual_idx = frame_idx + startFrame
        print("== frame_idx = ", frame_idx)
        print("== actual_idx = ", actual_idx)
        filename = frames_path + "/frame%d.png" % actual_idx
        labels, pixels = predict.return_pixels(filename)
        n_object = len(pixels)
        print(n_object)
        print(len(labels))
        bboxs[frame_idx] = np.empty((n_object, 4, 2), dtype=float)
        for o in range(0, n_object):
            print("object #", o)

            xmn = pixels[o][0]
            xmx = pixels[o][1]
            ymn = pixels[o][2]
            ymx = pixels[o][3]

            im = Image.open(filename)
            region = im.crop((xmn, ymn, xmx, ymx))

            object_path = objects_path + "/sentence_%s" % idSentence + "/frame_%d" % actual_idx + "_object_%d" % o + ".png"
            region.save(object_path)

            # CSV objects files
            #file = open(objects_path + "/object_annotations.csv", "a+")
            #wrtr = csv.writer(file)
            #wrtr.writerow([object_path, labels[o]])
            #file.close()

            bboxs[frame_idx][o, :, :] = np.array([[xmn, ymn], [xmx, ymn], [xmn, ymx], [xmx, ymx]]).astype(float)

    # output video
    # out.append(cv2.VideoWriter(DATA_PATH + "Output/output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 1,
    #                           (frames[frame_idx].shape[1], frames[frame_idx].shape[0])))

    print("End objects generation")

"""
        startXs, startYs = getFeatures(cv2.cvtColor(frames[frame_idx], cv2.COLOR_RGB2GRAY), bboxs[frame_idx],
                                       use_shi=False)
        if startXs.all() == -1 and startYs.all() == -1:
            continue
        else:
            for i in range(frame_idx + 1, frame_idx + 10):
                print('Processing Frame', i)
                newXs, newYs = estimateAllTranslation(startXs, startYs, frames[i - 1], frames[i])
                Xs, Ys, bboxs[i] = applyGeometricTransformation(startXs, startYs, newXs, newYs, bboxs[i - 1])

                print(bboxs[i])

                # update coordinates
                startXs = Xs
                startYs = Ys

                # update feature points as required
                n_features_left = np.sum(Xs != -1)
                print('# of Features: %d' % n_features_left)
                if (n_features_left > 0) and (n_features_left < 15):
                    print('Generate New Features')
                    startXs, startYs = getFeatures(cv2.cvtColor(frames[i], cv2.COLOR_RGB2GRAY), bboxs[i])

                # draw bounding box and visualize feature point for each object
                frames_draw[i] = frames[i].copy()
                for j in range(0, n_object):
                    (xmin, ymin, boxw, boxh) = cv2.boundingRect(bboxs[i][j, :, :].astype(int))
                    frames_draw[i] = cv2.rectangle(frames_draw[i], (xmin, ymin), (xmin + boxw, ymin + boxh),
                                                   (255, 0, 0), 2)
                    for k in range(startXs.shape[0]):
                        frames_draw[i] = cv2.circle(frames_draw[i], (int(startXs[k, j]), int(startYs[k, j])), 3,
                                                    (0, 0, 255), thickness=2)

                # imshow if to play the result in real time
                if play_realtime:
                    cv2.imshow("win", frames_draw[i])
                    cv2.waitKey(10)
                out[count].write(frames_draw[i])

            cv2.destroyAllWindows()
            out[count].release()
            print("Ending", count)
            count = count + 1
            new = 2
"""

    count1 = 0
    for frame_idx in range(0, n_frame - 10, 10):
        filename = DATA_PATH + "Video_Frames/frame%d.png" % frame_idx
        print(filename)
        labels, pixels = predict.return_pixels1(filename)

        n_object = len(pixels)

        for o in range(0, n_object):

            obj = ET.SubElement(annotation, 'object')
            name = ET.SubElement(obj, 'name')
            moving = ET.SubElement(obj, 'moving')
            action = ET.SubElement(obj, 'action')
            verified = ET.SubElement(obj, 'verified')
            id1 = ET.SubElement(obj, 'id')
            createdFrame = ET.SubElement(obj, 'createdFrame')
            startFrame = ET.SubElement(obj, 'startFrame')
            endFrame = ET.SubElement(obj, 'endFrame')
            name.text = labels[o]
            moving.text = 'true'
            verified.text = '0'

            count1 = count1 + 1

            id1.text = str(count1)
            createdFrame.text = '0'
            startFrame.text = str(frame_idx)
            endFrame.text = str(frame_idx + 10)

            for j in range(frame_idx, frame_idx + 10):

                if bboxs[j][o][0, 0] < 0:
                    bboxs[j][o][0, 0] = 0.0
                if bboxs[j][o][0, 1] < 0:
                    bboxs[j][o][0, 1] = 0.0
                if bboxs[j][o][1, 0] < 0:
                    bboxs[j][o][1, 0] = 0.0
                if bboxs[j][o][1, 1] < 0:
                    bboxs[j][o][1, 1] = 0.0
                if bboxs[j][o][2, 0] < 0:
                    bboxs[j][o][2, 0] = 0.0
                if bboxs[j][o][2, 1] < 0:
                    bboxs[j][o][2, 1] = 0.0
                if bboxs[j][o][3, 0] < 0:
                    bboxs[j][o][3, 0] = 0.0
                if bboxs[j][o][3, 1] < 0:
                    bboxs[j][o][3, 1] = 0.0

                if math.isnan(bboxs[j][o][3, 0]) or math.isnan(bboxs[j][o][3, 1]) or math.isnan(
                        bboxs[j][o][2, 0]) or math.isnan(bboxs[j][o][2, 1]) or math.isnan(
                    bboxs[j][o][1, 0]) or math.isnan(bboxs[j][o][1, 1]) or math.isnan(
                    bboxs[j][o][0, 0]) or math.isnan(bboxs[j][o][0, 1]):
                    break
                polygon = ET.SubElement(obj, 'polygon')
                t = ET.SubElement(polygon, 't')
                t.text = str(j)
                pt = ET.SubElement(polygon, 'pt')
                x = ET.SubElement(pt, 'x')
                y = ET.SubElement(pt, 'y')
                l = ET.SubElement(pt, 'l')
                x.text = str(int(bboxs[j][o][0, 0]))
                y.text = str(int(bboxs[j][o][0, 1]))
                if j == frame_idx:
                    l.text = '1'
                else:
                    l.text = '0'
                pt = ET.SubElement(polygon, 'pt')
                x = ET.SubElement(pt, 'x')
                y = ET.SubElement(pt, 'y')
                l = ET.SubElement(pt, 'l')
                x.text = str(int(bboxs[j][o][2, 0]))
                y.text = str(int(bboxs[j][o][2, 1]))
                if j == frame_idx:
                    l.text = '1'
                else:
                    l.text = '0'
                pt = ET.SubElement(polygon, 'pt')
                x = ET.SubElement(pt, 'x')
                y = ET.SubElement(pt, 'y')
                l = ET.SubElement(pt, 'l')
                x.text = str(int(bboxs[j][o][3, 0]))
                y.text = str(int(bboxs[j][o][3, 1]))
                if j == frame_idx:
                    l.text = '1'
                else:
                    l.text = '0'
                pt = ET.SubElement(polygon, 'pt')
                x = ET.SubElement(pt, 'x')
                y = ET.SubElement(pt, 'y')
                l = ET.SubElement(pt, 'l')
                x.text = str(int(bboxs[j][o][1, 0]))
                y.text = str(int(bboxs[j][o][1, 1]))
                if j == frame_idx:
                    l.text = '1'
                else:
                    l.text = '0'

            print("Ending count1", count1)

    # create a new XML file with the results
    indent(annotation)
    mydata = ET.tostring(annotation)
    print(DATA_PATH + "Object_Store/" + fn + ".xml")
    myfile = open(DATA_PATH + "Object_Store/" + fn + ".xml", "wb")
    myfile.write(mydata)
    return "/Object_Store/" + fn + ".xml"

def writeFrames(videoCap, length, path):
    print('========= write frames path = ', path)
    #n_frame = length - 10
    count = 0
    #frames = np.empty((n_frame,), dtype=np.ndarray)
    #print(frames.shape)
    success = True
    while success:
        videoCap.set(cv2.CAP_PROP_POS_MSEC, (count * 40))  # added this line
        success, image = videoCap.read()
        #print('Read a new frame: ', success)
        if success:
            cv2.imwrite(path + "/frame%d.jpg" % count, image)  # save frame as JPEG file
            count = count + 1
    print("n frame count = ", count)

def generate_frames(filename, path):
    print('========= Generating frames')
    print("capturing video ", filename)
    videoCap = cv2.VideoCapture(filename)
    success, image = videoCap.read()
    if success:
        # cap.set(cv2.CAP_PROP_FPS, 25)
        length = int(videoCap.get(cv2.CAP_PROP_FRAME_COUNT))
        writeFrames(videoCap, length, path)
    else :
        print("error reading videocap")
    videoCap.release()
    print("ended generate frames")
    return length

def detect_and_track(frames_path, objects_path, start_time, end_time, idSentence):
    print('========= Detect and Tracking')
    print(frames_path)
    print(start_time)
    print(end_time)

    startTimeSplit = start_time.split('.')
    endTimeSplit = end_time.split('.')
    startTimeMiliseconds = (int(startTimeSplit[0]) * 1000) + int(startTimeSplit[1]);
    endTimeMiliseconds = (int(endTimeSplit[0]) * 1000) + int(endTimeSplit[1]);

    print("start time (ms) = ", startTimeMiliseconds)
    print("end time (ms) = ", endTimeMiliseconds)

    # (25fps) - one frame at each 40ms
    startFrame = int(startTimeMiliseconds / 40)
    endFrame = int(endTimeMiliseconds / 40)

    vatic = objectTracking(frames_path, objects_path, startFrame, endFrame, idSentence, draw_bb=True, play_realtime=False, save_to_file=True)
    print("ended detect and track ", vatic)
    return vatic

# detect_and_track("Video_Store/full/2bfb129dea9d7d149b79b7bbc96f9d4eb037f8bd.mp4","10.00","20.00",0)
