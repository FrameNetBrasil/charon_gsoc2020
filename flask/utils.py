import numpy as np
import gzip
import pickle
import os
import glob
import time
import cv2
import datetime
import pandas as pd
from collections import Counter, defaultdict
import random
import shutil
import operator
from PIL import Image
import platform
import json

ROOT_PATH = '../input/'
OUTPUT_PATH = ROOT_PATH + 'charon-output/'
DATASET_PATH= ROOT_PATH

def save_in_file(arr, file_name):
    pickle.dump(arr, gzip.open(file_name, 'wb+', compresslevel=3))


def load_from_file(file_name):
    return pickle.load(gzip.open(file_name, 'rb'))


def save_in_file_fast(arr, file_name):
    pickle.dump(arr, open(file_name, 'wb'))


def load_from_file_fast(file_name):
    return pickle.load(open(file_name, 'rb'))


def show_image(im, name='image'):
    cv2.imshow(name, im.astype(np.uint8))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_resized_image(P, w=1000, h=1000):
    res = cv2.resize(P.astype(np.uint8), (w, h), interpolation=cv2.INTER_CUBIC)
    show_image(res)


def get_date_string():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")


def sort_dict_by_values(a, reverse=True):
    sorted_x = sorted(a.items(), key=operator.itemgetter(1), reverse=reverse)
    return sorted_x


def value_counts_for_list(lst):
    a = dict(Counter(lst))
    a = sort_dict_by_values(a, True)
    return a

def get_description_for_labels():
    out = open('./class-descriptions-boxable.csv')
    lines = out.readlines()
    ret_1, ret_2 = dict(), dict()
    for l in lines:
        arr = l.strip().split(',')
        ret_1[arr[0]] = arr[1]
        ret_2[arr[1]] = arr[0]
    return ret_1, ret_2

def read_single_image(path):
    use_pyvips = False
    try:
        if not use_pyvips:
            img = np.array(Image.open(path))
        else:
            # Much faster in case you have pyvips installed (uncomment import pyvips in top of file)
            img = pyvips.Image.new_from_file(path, access='sequential')
            img = np.ndarray(buffer=img.write_to_memory(),
                         dtype=np.uint8,
                         shape=[img.height, img.width, img.bands])
    except:
        try:
            img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        except:
            print('Fail')
            return None

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    if img.shape[2] == 2:
        img = img[:, :, :1]

    if img.shape[2] == 1:
        img = np.concatenate((img, img, img), axis=2)

    if img.shape[2] > 3:
        img = img[:, :, :3]

    return img


def read_image_bgr_fast(path):
    img2 = read_single_image(path)
    img2 = img2[:, :, ::-1]
    return img2


def random_intensity_change1(img, min_change=-20, max_change=20, separate_channel=True):
    img = img.astype(np.float32)
    delta = random.randint(min_change, max_change)
    for j in range(3):
        if separate_channel:
            delta = random.randint(min_change, max_change)
        img[:, :, j] += delta
    img[img < 0] = 0
    img[img > 255] = 255
    return img.astype(np.uint8)
