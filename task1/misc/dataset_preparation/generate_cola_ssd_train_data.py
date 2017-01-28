from utils.generator import Generator # generates cola logos on image
from utils.converter import Converter # converts VOC data to ssd train data
from utils.check_imgs_generator import Check_imgs_generator # generates check images

colas_path = 'colas'
g = Generator(colas_path, [('cola_black.png', 0.05), ('cola_red.png', 0.35), ('cola_white.png', 0.6)],
              (50, 50),
              (20, 40),
              90,
              (2, 3),
              0.6)

c = Converter(300, g)
src_path = '/media/renat/hdd1/workdir/datasets/images/VOCdevkit/VOC2012/JPEGImages'
dst_path = '/media/renat/hdd1/workdir/docker/ssd-af/data/VOCdevkit/cola'
c.perform_conversion(src_path, dst_path, 1e10) # achtung! parts hardcoded

check_imgs_generator = Check_imgs_generator()
check_imgs_generator.generate_check_imgs(dst_path, ['trainval', 'test']) # achtung! parts hardcoded