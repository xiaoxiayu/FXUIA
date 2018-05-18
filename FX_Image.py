from imageprocess import imageprocess_client as _fx_imageprocess_client_
from PIL import Image, ImageDraw, ImageMath, ImageChops
import platform
if platform.system() == 'Darwin':
    from PIL import ImageGrab
else:
    import pyscreenshot as ImageGrab

class FXImageProcess:
    def __init__(self, server=None):
        self.server = server
        self.image_process = _fx_imageprocess_client_.ImageProcesser(server)

    def find(self, img0, img1, debug=False):
        return \
            self.image_process.find_image(img0, img1, debug=debug)

    def difference(self, img0, img1, disparities=16, blur_x=-1, blur_y=-1, filter_core=25, debug=False):
        return \
            self.image_process.get_diff_rect(img0, img1, disparities, blur_x, blur_y, filter_core, debug=debug)

    def similarity(self, img0, img1, matching_distance=0.75, debug=False):
        return \
            self.image_process.detect_similarity(img0, img1, matching_distance, debug=debug)

    def detect(self, img, thresh, blur_x=5, blur_y=5, filter=False, zoom=1, filter_core=25, debug=False):
        return \
            self.image_process.detect_elements(img, thresh, blur_x, blur_y, filter, zoom, filter_core, debug=debug)

    def hist(self, img):
        return self.image_process.get_hist_array(img)

    def ocr(self, img):
        return self.image_process.ocr_text(img)

    def compare_color_hist(self, img0, img1):
        return self.image_process.compare_color_hist(img0, img1)

    def filter(self, img, matrix):
        return self.image_process.filter_2d(img, matrix)

    def equal(self, img0, img1):
        return self.image_process.equal(img0, img1)

    def composite(self, img0, img1):
        img_w0, img_h0 = img0.size
        img_w1, img_h1 = img1.size
        new_img = Image.new('RGBA', (img_w0+img_w1+10, max(img_h0,img_h1)), (0, 0, 0, 255))
        new_img.paste(img0, (0,0))
        new_img.paste(img1, (img_w0+10, 0))
        return new_img

    def ssim(self, img0, img1):
        return self.image_process.ssim(img0, img1)

    def reflow_compare_text(self, img0, img1):
        return self.image_process.reflow_compare_text(img0, img1)

    def reflow_compare_image(self, ab_img, fx_img):
        return self.image_process.reflow_compare_image(ab_img, fx_img)

    def cosine_sim(self, txt0, txt1):
        return self.image_process.cosine_sim(txt0, txt1)

    def info(self):
        return self.image_process.info()


class FXImage:
    def __init__(self, img=None, filepath=None):
        self.img = img
        if filepath != None:
            self.img = Image.open(filepath)

    def screenshot(self, x0, y0, x1, y1):
        self.img = ImageGrab.grab().crop((x0, y0, x1, y1))

    def open(self, file_path):
        self.img = Image.open(file_path)
        print(self.img)

    def convert_to_buf(self):
        return _fx_imageprocess_client_.pilimg_to_buf(self.img)

    def crop(self, x, y, w, h):
        return self.img.crop((x, y, w, h))

    def convert(self, flag):
        self.img = self.img.convert(flag)

    def draw_rectangle(self, pos0, pos1, fill=None):
        draw = ImageDraw.Draw(self.img)
        draw.rectangle([pos0, pos1], fill=fill)
        print(pos0, pos1)

    def show(self):
        self.img.show()

    def save(self, savepath):
        self.img.save(savepath)

    def equal_by_path(self, imgpath0, imgpath1):
        im0 = Image.open(imgpath0)
        im1 = Image.open(imgpath1)
        return ImageChops.difference(im0, im1).getbbox() is None

    def equal(self, img0, img1):
        return ImageChops.difference(img0, img1).getbbox() is None


    @property
    def image(self):
        return self.img

    @image.setter
    def image(self, img):
        self.image = img

# test
##img_process = FXImageProcess('10.103.129.80:32454')
# img_process = FXImageProcess('192.168.199.132:50051')
# img_process = FXImageProcess('127.0.0.1:50051')
##print(img_process.info())
##fximg = FXImage()
##fximg.open('imageprocess/acrobat/663002.pdf_24.png')
##ab_img = fximg.image
##
##fximg.open('imageprocess/foxit/663002.pdf_24.png')
##fx_img = fximg.image
##ret = img_process.reflow_compare_image(ab_img, fx_img)
##print(ret)

# fximg.open('Line_Pre.png')
# img0 = fximg.image
#
# fximg.open('Line_Popup.png')
# img1 = fximg.image
# print(img_process.difference(img0, img1, disparities=16))
# print(img_process.ocr(img0))
# i = img_process.filter(img0, [[0,0,0],[0,2,0],[0,0,0]])
# i.show()
# fximg.open('ReaderLite1.png')
# img1 = fximg.image
# img_process.get_diff(img0, img1, disparities=64, blur_x=5, blur_y=5, filter_core=30, debug=True)
# match_pos = img_process.similarity(img0, img1, matching_distance=0.2, debug=True)
# eles = img_process.detect(fximg.image, thresh=100, blur_x=5, blur_y=5,filter=True, zoom=1,debug=False)
# txt_pos_map = {}
# for ele in eles:
#     ele_img = fximg.crop(ele[0], ele[1], ele[0]+ele[2], ele[1]+ele[3])
#     ele_img.save('tem.png')
#     ele_img.show()
#
#     txt = img_process.ocr(ele_img)
#     txt_pos_map[txt] = ele
#     print(txt)
# minx = 1000000000
# miny = 1000000000
# maxx = 0
# maxy = 0
# for m in match_pos:
#     print(m)
#     if m[2] < minx:
#         minx = m[2]
#     if m[3] < miny:
#         miny = m[3]
#     if m[2] > maxx:
#         maxx = m[2]
#     if m[3] > maxy:
#         maxy = m[3]
# print(minx, miny, maxx, maxy)
# fximg.draw_rectangle((minx, miny), (maxx, maxy))
# fximg.show()
# for m in match_pos:
#     print(m)

