import os
import glob
import random
import numpy as np

import cv2

import caffe
from caffe.proto import caffe_pb2
import lmdb

CWD = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
animal_labels = {'bird': '0', 'cat': '1', 'cow': '2', 'dog': '3', 'frog': '4', 'horse': '5'}

train_lmdb = os.path.join(CWD, 'input', 'train_lmdb')
validation_lmdb = os.path.join(CWD, 'input', 'validation_lmdb')

# os.system('rm -rf  ' + train_lmdb)
# os.system('rm -rf  ' + validation_lmdb)


# find all images to create database
train_data = [img for img in glob.glob(os.path.join(CWD, "data", "**", "*jpg"))]
random.shuffle(train_data)

'''
# prepare dictionary mapping between training, validation images type
train_map = {}
with open(os.path.join(CWD, "input", "train.txt")) as train_file:
    for line in train_file:
        content = line.split()
        train_map[content[0]] = content[1]

val_map = {}
with open(os.path.join(CWD, "input", "validation.txt")) as val_file:
    for line in val_file:
        content = line.split()
        val_map[content[0]] = content[1]
'''

def get_label(filename):
    label = -1
    if 'bird' in filename:
        label = 0
    elif 'cat' in filename:
        label = 1
    elif 'cow' in filename:
        label = 2
    elif 'dog' in filename:
        label = 3
    elif 'frog' in filename:
        label = 4
    elif 'horse' in filename:
        label = 5
    return label

def make_datum(image, label):
    #image is numpy.ndarray format. BGR instead of RGB
    img = cv2.imread(image)
    h, w = img.shape[:2]
    return caffe_pb2.Datum(
        channels=3,
        width=w,
        height=h,
        label=label,
        data=np.rollaxis(img, 2).tostring())

def create_lmdb(data_type):
    if data_type == 'train':
        in_db = lmdb.open(train_lmdb, map_size=int(1e9))
        # data_map = train_map
    elif data_type == 'validation':
        in_db = lmdb.open(validation_lmdb, map_size=int(1e9))
        # data_map = val_map
    else:
        raise ValueError

    with in_db.begin(write=True) as in_txn:
        for in_idx, img_path in enumerate(train_data):
            if data_type == 'train' and in_idx % 6 == 0:
                print('[{}] Ignore image {}'.format(data_type, img_path))
                continue
            elif data_type == 'validation' and in_idx % 6 != 0:
                print('[{}] Ignore image {}'.format(data_type, img_path))
                continue
            filename = os.path.basename(img_path)
            # if filename in data_map:
            label = get_label(filename)
            datum = make_datum(img_path, label)
            in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
            print '[{}] {:0>5d}'.format(data_type, in_idx) + ':' + img_path
            # else:
            #     print('Something wrong with file {}'.format(filename))
            #     continue
    in_db.close()


DATA_TYPE = ['train', 'validation']
for dt in DATA_TYPE:
    create_lmdb(dt)

# in_db = lmdb.open(train_lmdb, map_size=int(1e9))

# with in_db.begin(write=True) as in_txn:
#     for in_idx, img_path in enumerate(train_data):
#         if in_idx % 6 == 0:
#             continue
#         filename = os.path.basename(img_path)
#         # if filename in data_map:
#         label = get_label(filename)
#         datum = make_datum(img_path, label)
#         in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
#         print '{:0>5d}'.format(in_idx) + ':' + img_path
#         # else:
#         #     print('Something wrong with file {}'.format(filename))
#         #     continue
# in_db.close()


# in_db = lmdb.open(validation_lmdb, map_size=int(1e9))

# with in_db.begin(write=True) as in_txn:
#     for in_idx, img_path in enumerate(train_data):
#         if in_idx % 6 != 0:
#             continue
#         filename = os.path.basename(img_path)
#         # if filename in data_map:
#         label = get_label(filename)
#         datum = make_datum(img_path, label)
#         in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
#         print '{:0>5d}'.format(in_idx) + ':' + img_path
#         # else:
#         #     print('Something wrong with file {}'.format(filename))
#         #     continue
# in_db.close()