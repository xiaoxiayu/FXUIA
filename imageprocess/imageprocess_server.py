
from concurrent import futures
import time

import grpc
import zlib

import imageprocess_pb2
from PIL import Image
import sys
import cv2

import pyocr
import pyocr.builders
import numpy as np
import fxqaimage
import os
import platform

os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'
if platform.system() != 'Windows':
    os.environ['TESSDATA_PREFIX'] = '/foxitqa/ocrdata'

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

ocr_tool, ocr_lang = fxqaimage.OCRInit()

def load_cv2img_from_buf(img_buf):
    img_buf = zlib.decompress(img_buf)
    nparr = np.fromstring(img_buf, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    

class Image(imageprocess_pb2.ImageServicer):

    def Info(self, request, context):
        return imageprocess_pb2.StringReply(replystr='hello imageprocess')

    def Draw(self, request, context):
        img_array = np.asarray(bytearray(request.imgobj), dtype=np.uint8)
        cv2_img_flag = 0
        img = cv2.imdecode(img_array, cv2_img_flag)
        print(img)
        new_img = img[100:200,200:300]
  
        img_str = cv2.imencode('.png', new_img)[1].tostring()
        return imageprocess_pb2.ImgReply(imgobj = img_str)

    def DetectElements(self, request, context):
        img = load_cv2img_from_buf(request.imgobj)
        #cv2.imwrite('tem.png', img)
        if request.filter.core == 0:
            request.filter.core = 25
        if request.filter.zoom == 0:
            request.filter.zoom = 1
        if request.blur.x == 0:
            request.blur.x = 5
        if request.blur.y == 0:
            request.blur.y = 5
        if request.thresh == 0:
            request.thresh = 100
        ele_rects = fxqaimage.DetectLetter(img, \
                                           request.thresh, \
                                           (request.blur.x, request.blur.y), \
                                           request.filter.enable, \
                                           request.filter.zoom, \
                                           request.filter.core)
        for ele_rect in ele_rects:
            yield imageprocess_pb2.ElementRect(x=ele_rect[0], \
                                               y=ele_rect[1], \
                                               w=ele_rect[2], \
                                               h=ele_rect[3])

    def OCR(self, request, context):
        img = load_cv2img_from_buf(request.imgobj)
        b_filter = False
        if request.filter == 1:
            b_filter = True
        zoom = 1
        if request.zoom != 0:
            zoom = request.zoom
        ocr_text = fxqaimage.DoOCR(ocr_tool, ocr_lang, img, b_filter, zoom)
        # img = load_cv2img_from_buf(request.imgobj)
        # ocr_text = fxqaimage.DoOCR(ocr_tool, ocr_lang, img)

        return imageprocess_pb2.TxtReply(txt = ocr_text)

    def FindImage(self, request, context):
##        print('FindImage')
        img = load_cv2img_from_buf(request.imgobj)
        template = load_cv2img_from_buf(request.templateobj)
        matchvalue = request.matchvalue
        img_rect = fxqaimage.Find(img, template, matchvalue)
        return imageprocess_pb2.ElementPos(x0=img_rect[0], \
                                           y0=img_rect[1], \
                                           x1=img_rect[2], \
                                           y1=img_rect[3])
    
    def GetBrightnessHistArray(self, request, context):
        img = load_cv2img_from_buf(request.imgobj)
        #cv2.imwrite('tem.png', img)

        hist = fxqaimage.GetBrightnessHistData(img)
        for x,y in enumerate(hist):
            yield imageprocess_pb2.HistBarData(x=x, y=y[0])

    def GetDiffRect(self, request, context):
        img0 = load_cv2img_from_buf(request.orgimgobj)
        img1 = load_cv2img_from_buf(request.cmpimgobj)
        print('0')
##        cv2.imwrite('tem0.png', img0)
##        cv2.imwrite('tem1.png', img1)

        if request.blur.x == 0:
          request.blur.x = -1
        if request.blur.y == 0:
          request.blur.y = -1
        if request.filter_core == 0:
          request.filter_core = 30
        if request.disparities == 0:
            request.disparities = 16
        print('1')

        x_r, y_r = fxqaimage.DetectDiffRange(img0, img1, \
                                             request.disparities, \
                                           (request.blur.x, request.blur.y), \
                                           request.filter_core)
        if len(x_r) == 0 or len(x_r) == 0:
          rect_x = -1
          rect_y = -1
          rect_w = -1
          rect_h = -1
        else:
          rect_x = min(y_r) - 1
          rect_y = min(x_r) - 1
          rect_w = max(y_r) - rect_x + 1
          rect_h = max(x_r) - rect_y + 1
        return imageprocess_pb2.ElementRect(x=int(rect_x), \
                                         y=int(rect_y), \
                                         w=int(rect_w), \
                                         h=int(rect_h))

    def DetectSimilarity(self, request, context):
        img0 = load_cv2img_from_buf(request.orgimgobj)
        img1 = load_cv2img_from_buf(request.cmpimgobj)

        if request.feature_matching_distance == 0:
            request.feature_matching_distance = 0.75

        pos1, pos2 = fxqaimage.FeatureMatching(img0, img1, request.feature_matching_distance)
        if pos1 == None:
            return
        for i in range(len(pos1)):
            yield imageprocess_pb2.DMatchPos(x0 = pos1[i][0], y0 = pos1[i][1], \
                                             x1 = pos2[i][0], y1 = pos2[i][1])

    def DrawSimilarity(self, request, context):
        img0 = load_cv2img_from_buf(request.orgimgobj)
        img1 = load_cv2img_from_buf(request.cmpimgobj)

        if request.feature_matching_distance == 0:
            request.feature_matching_distance = 0.75

        pos1, pos2, img = fxqaimage.FeatureMatching(img0, img1, request.feature_matching_distance, draw=True)
        if pos1 == None:
            return
                
        img_str = cv2.imencode('.png', img)[1].tostring()
        return imageprocess_pb2.CmpImgReply(dp = len(pos1), imgobj = img_str)

    def CompareColorHist(self, request, context):
        img0 = load_cv2img_from_buf(request.orgimgobj)
        img1 = load_cv2img_from_buf(request.cmpimgobj)

        ret = fxqaimage.CompareColorHist(img0, img1)
        return imageprocess_pb2.FloatReply(data=ret)

    def Filter2D(self, request, context):
        m_s_l = request.matrix.split(',')
        power = 0
        m_l = len(m_s_l)
        for p in [3, 5, 7, 9]:
            if m_l % p == 0:
                power = p
        matrix = []
        l = []
        for d in m_s_l:
            if d == '':
                continue
            l.append(int(d))
            if len(l) == power:
                matrix.append(l)
                l = []
        img = load_cv2img_from_buf(request.imgobj)
        ret = fxqaimage.Filter2D(img, matrix)
        img_buf = cv2.imencode('.png', ret)[1].tostring()
        return imageprocess_pb2.ImgReply(imgobj=img_buf)

    def SSIM(self, request, context):
        img0 = load_cv2img_from_buf(request.img0)
        img1 = load_cv2img_from_buf(request.img1)

        ret = fxqaimage.ssim_compare(img0, img1)
        return imageprocess_pb2.FloatReply(data=ret)

    def CosineSim(self, request, context):
        ret = fxqaimage.cosine_sim(request.txt0, request.txt1)
        return imageprocess_pb2.FloatReply(data=ret)

    def reflow_compare_image(self, request, context):
        img0 = load_cv2img_from_buf(request.img0)
        img1 = load_cv2img_from_buf(request.img1)

        ab_img = fxqaimage.magic_wand_fill(img0, (10, 10), 0, 0)
        h, w = ab_img.shape[:2]
        ab_img = fxqaimage.magic_wand_fill(ab_img, (w - 10, h - 10), 0, 0)

        ha, wa = img1.shape[:2]
        ab_img = cv2.resize(ab_img, (int(wa), int(ha)))

        ret = fxqaimage.ssim_compare(ab_img, img1)
        return imageprocess_pb2.FloatReply(data=ret)

    def reflow_compare_text(self, request, context):
        img0 = load_cv2img_from_buf(request.img0)
        img1 = load_cv2img_from_buf(request.img1)

        ab_img = fxqaimage.magic_wand_fill(img0, (10, 10), 0, 0)
        h, w = ab_img.shape[:2]
        ab_img = fxqaimage.magic_wand_fill(ab_img, (w - 10, h - 10), 0, 0)

        ab_filter = True
        ab_zoom = 2.5
        fx_filter = True
        fx_zoom = 2.5

        ab_ocr_txt = fxqaimage.DoOCR(ocr_tool, ocr_lang, ab_img, filter=ab_filter, zoom=ab_zoom)
        fx_ocr_txt = fxqaimage.DoOCR(ocr_tool, ocr_lang, img1, filter=fx_filter, zoom=fx_zoom)
        ret = fxqaimage.cosine_sim(fx_ocr_txt, ab_ocr_txt)
        return imageprocess_pb2.ReflowTextReply(sim=ret, txt0=ab_ocr_txt, txt1=fx_ocr_txt)

    def magic_wand_fill(self, request, context):
        img0 = load_cv2img_from_buf(request.img)
        new_img = fxqaimage.magic_wand_fill(img0, (request.posx, request.posy), 0, 0)
        img_str = cv2.imencode('.png', new_img)[1].tostring()
        return imageprocess_pb2.ImgReply(imgobj=img_str)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  imageprocess_pb2.add_ImageServicer_to_server(Image(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
