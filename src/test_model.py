import os
import glob
import cv2
import caffe
import lmdb
import numpy as np
from caffe.proto import caffe_pb2

# caffe.set_model_cpu() 

#Size of images
IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100

CWD = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
MODEL_DIR = os.path.join(CWD, 'model')
INPUT_DIR = os.path.join(CWD, 'input')



'''
Image processing helper function
'''

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img


'''
Reading mean image, caffe model and its weights 
'''
#Read mean image
mean_blob = caffe_pb2.BlobProto()
with open(os.path.join(INPUT_DIR, 'mean.binaryproto')) as f:
    mean_blob.ParseFromString(bytes(f.read()))
mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width))


#Read model architecture and trained model's weights
net = caffe.Net(os.path.join(MODEL_DIR, 'caffenet_deploy.prototxt'),
                os.path.join(MODEL_DIR, 'snapshot', 'caffe_model_1_iter_5000.caffemodel'),
                caffe.TEST)

#Define image transformers
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', mean_array)
transformer.set_transpose('data', (2,0,1))

'''
Making predicitions
'''
#Reading image paths

animal_labels = {'bird': '0', 'cat': '1', 'cow': '2', 'dog': '3', 'frog': '4', 'horse': '5'}

for animal in animal_labels.key():

    test_img_paths = [img for img in glob.glob(os.path.join(CWD, "test", animal, "*jpg"))]

    #Making predictions
    test_ids = []
    preds = []
    for img_id, img_path in enumerate(test_img_paths):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
        
        net.blobs['data'].data[...] = transformer.preprocess('data', img)
        out = net.forward()
        pred_probas = out['prob']

        test_ids = test_ids + [img_id]
        preds = preds + [pred_probas.argmax()]

        print img_path
        print pred_probas.argmax()
        print '-------'

    '''
    Making submission file
    '''
    with open(os.path.join(CWD, 'test', animal + '_submission_model.csv'),"w") as f:
        f.write("id,label\n")
        for i in range(len(test_ids)):
            f.write(str(test_ids[i])+","+str(preds[i])+"\n")
    f.close()