from __future__ import division
import cv2
import numpy as np
import os

# generates cola logos on image
class Generator():
    def __init__(self, 
                 cola_imgs_path, 
                 cola_imgs_info, 
                 cola_max_shrinks_percent, 
                 cola_min_max_sizes_percent, 
                 cola_max_rotation_degrees,
                 cola_min_max_cnts,
                 cola_min_transparency):
        
        cola_img_names, cola_img_probs = zip(*cola_imgs_info)
        self.cola_imgs = [cv2.imread(os.path.join(cola_imgs_path, cola_img_name), cv2.IMREAD_UNCHANGED) 
                          for cola_img_name in cola_img_names]
        self.cola_img_probs = np.array(cola_img_probs)
        self.cola_img_probs /= np.sum(self.cola_img_probs)
        assert len(self.cola_imgs) == len(self.cola_img_probs)
        
        
        def check_percent_value(value):
            assert value >= 0 and value <= 100
        
        def check_percent_values(values, required_len):
            assert len(values) == required_len
            map(check_percent_value, values)
        
        check_percent_values(cola_max_shrinks_percent, 2)
        self.cola_max_shrinks_percent = cola_max_shrinks_percent
        
        check_percent_values(cola_min_max_sizes_percent, 2)
        self.cola_min_max_sizes_percent = cola_min_max_sizes_percent
        
        assert cola_max_rotation_degrees >= 0 and cola_max_rotation_degrees <= 90
        self.cola_max_rotation_degrees = cola_max_rotation_degrees
        
        assert len(cola_min_max_cnts) == 2
        assert cola_min_max_cnts[0] < cola_min_max_cnts[1]
        for el in cola_min_max_cnts:
            assert el >= 0 and el <= 100
        self.cola_min_max_cnts = cola_min_max_cnts

        assert cola_min_transparency >= 0 and cola_min_transparency <= 1
        self.cola_min_transparency = cola_min_transparency

    def transform_img(self, img, angle_degrees, shrink_height_percent, shrink_width_percent):
        rows, cols, ch = img.shape
        pts_src = np.float32([[0,0],[cols,0],[0,rows],[cols,rows]])

        def shrink(value, percent):
            return int(value * (1 - percent / 100))

        def rotate_polygon(points, angle_degrees):
            def rotate_point(point, origin, angle):
                v = point - origin
                rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                            [np.sin(angle), np.cos(angle)]])
                v_rotated = np.dot(v, rotation_matrix)
                return v_rotated + origin

            angle = np.radians(angle_degrees)
            points = np.array(points)
            origin = np.mean(points, axis=0)
            return [rotate_point(point, origin, angle) for point in points]

        left, right, top, bottom = 0, shrink(cols, shrink_width_percent), 0, shrink(rows, shrink_height_percent)
        points = [[left,top], [right,top], [left,bottom], [right,bottom]]

        points = rotate_polygon(points, angle_degrees)
        points -= np.min(points, axis=0)
        new_size = np.ceil(np.max(points, axis=0)).astype(int)
        pts_dst = np.float32(points)

        M = cv2.getPerspectiveTransform(pts_src, pts_dst)
        dst = cv2.warpPerspective(img,M,tuple(new_size))
        return dst

    def paste_img(self, img_src, img_pasting, position_percent, width_percent, transparency, rectangles):
        img_src_h, img_src_w, _ = img_src.shape
        img_pasting_h, img_pasting_w, _ = img_pasting.shape
        img_pasting_scale = (width_percent / 100) * img_src_w / img_pasting_w
        img_pasting_resized = cv2.resize(img_pasting, (0,0), fx=img_pasting_scale, fy=img_pasting_scale)
        img_pasting_resized_h, img_pasting_resized_w, _ = img_pasting_resized.shape
        position = map(int, [(position_percent[0] / 100) * img_src_h, (position_percent[1] / 100) * img_src_w])
        top, bottom = position[0], position[0] + img_pasting_resized_h
        left, right = position[1], position[1] + img_pasting_resized_w
        if top < 0 or bottom > img_src_h:
            return img_src, rectangles
        if left < 0 or right > img_src_w:
            return img_src, rectangles
        
        def point_in_rec(point, rec):
            return True if point[0] >= rec[0] and point[0] <= rec[2] and point[1] >= rec[1] and point[1] <= rec[3] else False
        
        def get_points(rec):
            return [[rec[0], rec[1]],
                    [rec[0], rec[3]],
                    [rec[2], rec[1]], 
                    [rec[2], rec[3]]]
        
        # if current rectangle intersects with existings rectangles
        rec1 = left, top, right, bottom
        for rectangle in rectangles:
            rec2 = rectangle
            if rec1[0] >= rec2[0] and rec1[2] <= rec2[2]:
                return img_src, rectangles
            if rec2[0] >= rec1[0] and rec2[2] <= rec1[2]:
                return img_src, rectangles
            if rec1[1] >= rec2[1] and   rec1[3] <= rec2[3]:
                return img_src, rectangles
            if rec2[1] >= rec1[1] and rec2[3] <= rec1[3]:
                return img_src, rectangles
            for point in get_points(rec1):
                if point_in_rec(point, rec2):
                    return img_src, rectangles
            for point in get_points(rec2):
                if point_in_rec(point, rec1):
                    return img_src, rectangles
            
        rectangles.append((left, top, right, bottom))
        
        img_src = img_src.copy()
        img_src_part = img_src[position[0]:position[0] + img_pasting_resized_h, 
                               position[1]:position[1] + img_pasting_resized_w, 
                               :]
        transparencty_part = (img_pasting_resized[:,:,3] / 255)[:, :, np.newaxis]
        img_src[position[0]:position[0] + img_pasting_resized_h, 
                position[1]:position[1] + img_pasting_resized_w, 
                :] = (1 - transparencty_part * transparency) * img_src_part + \
                     (transparencty_part * transparency) * img_pasting_resized[:,:,:3]
        return img_src, rectangles

    def generate_coca_cola(self):
        coca_cola_img_indx = np.random.choice(range(len(self.cola_img_probs)), p=self.cola_img_probs)
        coca_cola_img = self.cola_imgs[coca_cola_img_indx] 
        
        shrink_height_percent, shrink_width_percent = map(lambda _: np.random.uniform(0, _), 
                                                          self.cola_max_shrinks_percent)
        angle_degrees = ((-1) ** np.random.randint(2)) * np.random.normal(0, self.cola_max_rotation_degrees / 2)
        random_coca_cola = self.transform_img(coca_cola_img, 
                                              angle_degrees, 
                                              shrink_height_percent, 
                                              shrink_width_percent)
        return random_coca_cola

    def try_paste_coca_colas(self, img_src):
        rectangles = []
        required_rectangles_cnt = np.random.randint(low = self.cola_min_max_cnts[0], 
                                                    high = self.cola_min_max_cnts[1] + 1)
        res_img = img_src
        rectangle_not_added_cnt = 0
        while len(rectangles) < required_rectangles_cnt:
            random_coca_cola = self.generate_coca_cola()
            position_percent = np.random.uniform(0, 100, 2)
            pasting_cola_width_percent = np.random.uniform(*self.cola_min_max_sizes_percent)
            
            old_rectangles_cnt = len(rectangles)
            res_img, rectangles = self.paste_img(res_img, 
                                     random_coca_cola, 
                                     position_percent, 
                                     pasting_cola_width_percent, 
                                     np.random.uniform(self.cola_min_transparency, 1), 
                                     rectangles)
            rectangle_added = len(rectangles) > old_rectangles_cnt
            old_rectangles_cnt = len(rectangles)
            if rectangle_added:
                rectangle_not_added_cnt = 0
            else:
                rectangle_not_added_cnt += 1
                if rectangle_not_added_cnt >= 20:
                    return res_img, rectangles
        return res_img, rectangles

    def paste_coca_colas(self, img_path):
        img = cv2.imread(img_path)
        try_cnt = 0
        while True:
            res_img, rectangles = self.try_paste_coca_colas(img)
            if len(rectangles) >= self.cola_min_max_cnts[0] and len(rectangles) <= self.cola_min_max_cnts[1]:
                return res_img, rectangles
            try_cnt += 1
            if try_cnt >= 20:
                raise ValueError('Not enough space in image')
