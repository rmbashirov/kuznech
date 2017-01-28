from __future__ import division
import cv2
import numpy as np
import xml.etree.cElementTree as ET
import os



def mk_dirs(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

# converts VOC data to ssd train data
class Converter():
    def __init__(self, SSD_img_side, g):
        self.SSD_img_side = SSD_img_side
        self.g = g

    def convert(self, img, bboxes, dst_img_path, dst_ann_path):
        old_img_shape = img.shape
        img_scale_h = self.SSD_img_side / old_img_shape[0]
        img_scale_w = self.SSD_img_side / old_img_shape[1]

        img = cv2.resize(img, (self.SSD_img_side, self.SSD_img_side))

        etAnnot = ET.Element('annotation')
        ET.SubElement(etAnnot, 'folder').text = 'VOC2007'
        ET.SubElement(etAnnot, 'filename').text = os.path.basename(dst_img_path) # !!!!

        etSize = ET.SubElement(etAnnot, "size")
        ET.SubElement(etSize, 'width').text = str(self.SSD_img_side)
        ET.SubElement(etSize, 'height').text = str(self.SSD_img_side)
        ET.SubElement(etSize, 'depth').text = '3'

        ET.SubElement(etAnnot, 'segmented').text = '0'

        writtenObjCnt = 0
        for bbox in bboxes:
            xMin, yMin, xMax, yMax = bbox
            xMin = int(xMin * img_scale_w)
            xMax = int(xMax * img_scale_w)
            yMin = int(yMin * img_scale_h)
            yMax = int(yMax * img_scale_h)

            etObj = ET.SubElement(etAnnot, "object")
            ET.SubElement(etObj, 'name').text = 'coca_cola'
            ET.SubElement(etObj, 'pose').text = 'Unspecified'
            ET.SubElement(etObj, 'truncated').text = '1'  # can't determine
            ET.SubElement(etObj, 'difficult').text = '0'  # all is easy...

            etBBox = ET.SubElement(etObj, "bndbox")

            ET.SubElement(etBBox, 'xmin').text = str(xMin)
            ET.SubElement(etBBox, 'ymin').text = str(yMin)
            ET.SubElement(etBBox, 'xmax').text = str(xMax)
            ET.SubElement(etBBox, 'ymax').text = str(yMax)

            writtenObjCnt += 1

        if writtenObjCnt < 1:
            return False

        etTree = ET.ElementTree(etAnnot)
        etTree.write(dst_ann_path)
        cv2.imwrite(dst_img_path, img)

        return True

    

    def perform_conversion_part(self, part_name, img_paths, dst_path, curr_index):
        print 'Converting ', part_name
        res_img_dir = os.path.join(dst_path, 'JPEGImages')
        res_ann_dir = os.path.join(dst_path, 'Annotations')
        res_imset_dir = os.path.join(dst_path, 'ImageSets', 'Main')
        res_check_imgs_dir = os.path.join(dst_path, 'Check')

        mk_dirs(res_img_dir)
        mk_dirs(res_ann_dir)
        mk_dirs(res_imset_dir)
        mk_dirs(res_check_imgs_dir)
        
        converted_imgs = []
        for i, img_path in enumerate(img_paths):
            print '%d/%d' % (i + 1, len(img_paths))
            try:
                res_img, bboxes = self.g.paste_coca_colas(img_path)
                res_img_name_ending = '.jpg'
                res_img_name = '%06d' % curr_index + res_img_name_ending
                res_ann_name = '%06d' % curr_index + '.xml'
                dst_img_path = os.path.join(res_img_dir, res_img_name)
                dst_ann_path = os.path.join(res_ann_dir, res_ann_name)
                if self.convert(res_img, bboxes, dst_img_path, dst_ann_path):
                    converted_imgs.append(res_img_name[:-len(res_img_name_ending)])
                    curr_index += 1
            except ValueError as ex:
                print 'Could not convert', os.path.basename(img_path), ';', ex.args
                continue
        
        res_imset_path = os.path.join(res_imset_dir, part_name + '.txt')
        with open(res_imset_path, 'w') as f:
            for converted_img in converted_imgs:
                f.write('%s\n' % converted_img)
        return curr_index

    def perform_conversion(self, src_path, dst_path, max_imgs_cnt, test_size_percent = 10):
        img_paths = sorted(filter(lambda _: _.endswith('.jpg'), os.listdir(src_path)))
        if len(img_paths) > max_imgs_cnt:
            img_paths = img_paths[:max_imgs_cnt]
        img_paths = map(lambda _: os.path.join(src_path, _), img_paths)
        test_size = int(len(img_paths) * test_size_percent / 100)
        curr_index = 0
        for part_name, part_img_paths in zip(['trainval', 'test'], [img_paths[:-test_size], img_paths[-test_size:]]):
            curr_index = self.perform_conversion_part(part_name, part_img_paths, dst_path, curr_index)
