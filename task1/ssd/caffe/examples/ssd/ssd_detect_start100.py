# coding: utf-8

# # Detection with SSD

import numpy as np
import os
import sys
import caffe
from google.protobuf import text_format
from caffe.proto import caffe_pb2
import cv2
import argparse

COLORS = [(0, 0, 0), (0, 255, 255)]

CONFS = [1000000, 0.2]
MIN_CONF = min(CONFS)

if __name__ == '__main__':

    common_src_dir = '/root/data/cola_test'
    common_vis_dir = '/root/data/results/cola_test'
    labelmap_file = '/caffe/data/cola/labelmap_voc.prototxt'
    model_def = '/caffe/models/SSD_300x300_start100/deploy.prototxt'
    model_weights = '/caffe/models/SSD_300x300_start100/VGG_SSD_300x300_start100_iter_15000.caffemodel'
    image_resize = 300

    caffe_root = '/caffe'

    os.chdir(caffe_root)
    sys.path.insert(0, 'python')


    caffe.set_device(0)
    caffe.set_mode_gpu()

    # load PASCAL VOC labels
    file = open(labelmap_file, 'r')
    labelmap = caffe_pb2.LabelMap()
    text_format.Merge(str(file.read()), labelmap)

    def get_labelname(labelmap, labels):
        num_labels = len(labelmap.item)
        labelnames = []
        if type(labels) is not list:
            labels = [labels]
        for label in labels:
            found = False
            for i in xrange(0, num_labels):
                if label == labelmap.item[i].label:
                    found = True
                    labelnames.append(labelmap.item[i].display_name)
                    break
            assert found == True
        return labelnames

    # * Load the net in the test phase for inference, and configure input preprocessing.
    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)

    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', np.array([104,117,123])) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    # set net to batch size of 1
    net.blobs['data'].reshape(1,3,image_resize,image_resize)


    def processImg(net, curr_img_path, curr_vis_path, visualize):

        image = caffe.io.load_image(curr_img_path)

        transformed_image = transformer.preprocess('data', image)
        net.blobs['data'].data[...] = transformed_image

        # Forward pass.
        detections = net.forward()['detection_out']

        # Parse the outputs.
        det_label = detections[0,0,:,1]
        det_conf = detections[0,0,:,2]
        det_xmin = detections[0,0,:,3]
        det_ymin = detections[0,0,:,4]
        det_xmax = detections[0,0,:,5]
        det_ymax = detections[0,0,:,6]

        # Get detections with confidence higher than 0.6.
        top_indices = [i for i, conf in enumerate(det_conf) if conf >= MIN_CONF]

        top_conf = det_conf[top_indices]
        top_label_indices = det_label[top_indices].tolist()
        top_labels = get_labelname(labelmap, top_label_indices)
        top_xmin = det_xmin[top_indices]
        top_ymin = det_ymin[top_indices]
        top_xmax = det_xmax[top_indices]
        top_ymax = det_ymax[top_indices]

        if (visualize):
            qimage = cv2.imread(curr_img_path)

        #qimage = cv2.multiply(image, 255)

        for i in xrange(top_conf.shape[0]):
            xmin = int(round(top_xmin[i] * image.shape[1]))
            ymin = int(round(top_ymin[i] * image.shape[0]))
            xmax = int(round(top_xmax[i] * image.shape[1]))
            ymax = int(round(top_ymax[i] * image.shape[0]))
            score = top_conf[i]
            label = int(top_label_indices[i])
            label_name = top_labels[i]
            #coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1

            if CONFS[label] > score:
                continue

            if (visualize):
                color = COLORS[label]
                cv2.rectangle(qimage, (xmin, ymin), (xmax, ymax), color = color, thickness=2, lineType=8)
                font = cv2.FONT_HERSHEY_PLAIN
                text_to_img = '%s: %.2f'%(label_name, score)
                cv2.putText(qimage, text_to_img, (xmin, ymin - 5), font, 1, color, 2)

        if visualize:
            cv2.imwrite(curr_vis_path, qimage)




    for curr_src_dir, dirs, files in os.walk(common_src_dir):
        curr_vis_dir = curr_src_dir.replace(common_src_dir, common_vis_dir)
        if not os.path.exists(curr_vis_dir):
            os.makedirs(curr_vis_dir)
        print('Dir in process: ' + curr_src_dir + ' -> ' + curr_vis_dir)

        files.sort()

        for file in files:
            curr_img_path = os.path.join(curr_src_dir, file)
            curr_vis_path = os.path.join(curr_vis_dir, file)

            if ((not file.split('.')[-1] == 'png') and (not file.split('.')[-1] == 'jpg')) or (not os.path.isfile(curr_img_path)):
                continue
            print('File in process: ' + curr_img_path + ' -> ' + curr_vis_path)

            processImg(net, curr_img_path, curr_vis_path, True)


    print('FINISHED.')

