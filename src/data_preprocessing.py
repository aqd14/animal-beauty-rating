#!/usr/bin/env python

import os
import os.path
import cv2
import random

TRAIN_TEXT_FILE = 'train.txt'
VALIDATION_TEXT_FILE = 'validation.txt'
IMAGE_DIR = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data')

IMAGE_SIZE = 100

'''
Labels

bird: 0
cat: 1
cow: 2
dog: 3
frog: 4
horse: 5
'''

animal_labels = {'bird': '0', 'cat': '1', 'cow': '2', 'dog': '3', 'frog': '4', 'horse': '5'}

def create_label(animal_type):
    train_file_writer = open(TRAIN_TEXT_FILE, 'a')
    validation_file_writer = open(VALIDATION_TEXT_FILE, 'a')

    data_file_path = os.path.join(IMAGE_DIR, animal_type)
    filenames = os.listdir(data_file_path)

    training_size = 0.8 * len(filenames)
    validation_size = 0.2 * len(filenames)
    random.shuffle(filenames)
    for img_num, filename in enumerate(filenames):
        if img_num < training_size:
            train_file_writer.write(filename + ' ' + animal_labels[animal_type] + '\n')
        else:
            validation_file_writer.write(filename + ' ' + animal_labels[animal_type] + '\n')

    train_file_writer.close()
    validation_file_writer.close()

def resize_images(image_size, img):
    '''
    we need to keep in mind aspect ratio so the image does
    not look skewed or distorted -- therefore, we calculate
    the ratio of the new image to the old image
    :param animal_type: folder
    '''
    '''
    r = float(image_size) / img.shape[1]
    dim = (image_size, int(img.shape[0] * r))
    '''
    # perform the actual resizing of the image and show it
    return cv2.resize(img, (image_size, image_size), interpolation=cv2.INTER_CUBIC)

def transform_histogram_equalization(img):
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
    return img

def preprocessing(animal_type, image_size):
    '''
    Preprocessing images to prepare for training and testing
    '''
    animal_dir = os.path.join(IMAGE_DIR, animal_type)
    filenames = os.listdir(animal_dir)
    for num, filename in enumerate(filenames):
        print('[{}] Processing image {}'.format(num, filename))
        img = cv2.imread(os.path.join(animal_dir, filename), cv2.IMREAD_COLOR)
        img = resize_images(image_size, img)
        img = transform_histogram_equalization(img)
        cv2.imwrite(os.path.join(animal_dir, filename), img)
        print('Done!\n\n')

def main():
    animal_types = ['bird', 'cat', 'cow', 'dog', 'frog', 'horse']
    for animal_type in animal_types:
        # create_label(animal_type)
        preprocessing(animal_type, IMAGE_SIZE)

# if __name__ == '__main__':
#   main()
img = cv2.imread('bird.jpg', cv2.IMREAD_COLOR)
img = resize_images(256, img)
cv2.imwrite('resized_bird.jpg', img)
img = transform_histogram_equalization(img)
cv2.imwrite('histogram_bird.jpg', img)

