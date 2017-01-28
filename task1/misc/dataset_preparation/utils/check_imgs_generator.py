from __future__ import print_function, division

import os
import cv2
import xml.etree.cElementTree as ET
import random

def mk_dirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def get_random_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

class Check_imgs_generator:
    def __init__(self):
        self.bboxes = {}

    def drawBoxes(self, srcImgPath, srcAnnPath, resImgPath):
        img = cv2.imread(srcImgPath)

        tree = ET.ElementTree(file=srcAnnPath)
        for etObject in tree.iterfind('object'):  # or XMLPath: object/foo/bar
            name = etObject.findall('name')[0].text
            if not name in self.bboxes:
                self.bboxes[name] = [get_random_color(), 0]
            else:
                self.bboxes[name][1] += 1

            etBBox = etObject.findall('bndbox')[0]
            xmin = int(etBBox.findall('xmin')[0].text)
            ymin = int(etBBox.findall('ymin')[0].text)
            xmax = int(etBBox.findall('xmax')[0].text)
            ymax = int(etBBox.findall('ymax')[0].text)

            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=self.bboxes[name][0], thickness=1, lineType=8)
            cv2.imwrite(resImgPath, img)

    def print_draw_statistics(self):
        for bbox_name in self.bboxes:
            print('bbox "%s": used %d times, has (%s) color' % (bbox_name, self.bboxes[bbox_name][1], ','.join(map(str, self.bboxes[bbox_name][0]))))


    def generate_check_imgs(self, output, parts):
        resImgDir = os.path.join(output, 'JPEGImages')
        resAnnDir = os.path.join(output, 'Annotations')
        resImsetDir = os.path.join(output, 'ImageSets', 'Main')
        resCheckImgsDir = os.path.join(output, 'Check')

        mk_dirs(resCheckImgsDir)

        for part in parts:
            parth_path = os.path.join(resImsetDir, part + '.txt')
            if not os.path.isfile(parth_path):
                print('No txt file for part "%s". Skipping part.' % (part))
                continue
            part_files = filter(None, map(str.strip, open(parth_path, 'r').readlines()))
            for part_file in part_files:
                img_path = os.path.join(resImgDir, part_file + '.jpg')
                if not os.path.isfile(img_path):
                    print('No img for %s. Skipping img.' % (part_file))
                    continue
                annotation_path = os.path.join(resAnnDir, part_file + '.xml')
                if not os.path.isfile(annotation_path):
                    print('No annotation for %s. Skipping annotation.' % (part_file))
                    continue
                check_img_path = os.path.join(resCheckImgsDir, part_file + '.jpg')
                self.drawBoxes(img_path, annotation_path, check_img_path)
        self.print_draw_statistics()