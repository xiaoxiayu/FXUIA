from PIL import Image
import sys
import cv2

import pyocr
import pyocr.builders
import numpy as np


##def match(matchvalue):
##    img2 = img.copy()
##
##    result = cv2.matchTemplate(img,template,matchvalue)
##
##    cv2.normalize(result,result,0,255,cv2.NORM_MINMAX)
##
##    mini,maxi,(mx,my),(Mx,My) = cv2.minMaxLoc(result)    # We find minimum and maximum value locations in result
##
##    if matchvalue in [0,1]: # For SQDIFF and SQDIFF_NORMED, the best matches are lower values.
##        MPx,MPy = mx,my
##    else:                   # Other cases, best matches are higher values.
##        MPx,MPy = Mx,My
##
##    # Normed methods give better results, ie matchvalue = [1,3,5], others sometimes shows errors
##    cv2.rectangle(img2, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
##
##    cv2.imshow('input',img2)
##    cv2.imshow('output',result)
##
##trows,tcols = template.shape[:2]    # template rows and cols
##
##cv2.namedWindow('input')
##
##matchvalue = 0
##max_Trackbar = 5
##
##cv2.createTrackbar('method','input',matchvalue,max_Trackbar,match)
##
##match(0)
##
##if cv2.waitKey(0) == 27:
##    cv2.destroyAllWindows()
##

def toGray(img):
    try:
        _, _, channels = img.shape
        if channels == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
    except:
        gray = img
    return gray

def filterProcess(img_source, grey=True, zoom=2.5, filter_core=25):
    if grey:
        img = toGray(img_source)
    
    w, h = img.shape[::-1]
    resized_image = cv2.resize(img, (int(w*zoom), int(h*zoom))) 

    final = cv2.medianBlur(resized_image, 1)    

    v = np.array([ [-1.0,  -1.0, -1.0, -1.0, -1.0],\
                   [-1.0,  -1.0, -1.0, -1.0,  -1.0],\
                   [-1.0,  -1.0, filter_core, -1.0,  -1.0],\
                   [-1.0,  -1.0, -1.0, -1.0,  -1.0],\
                   [-1.0,  -1.0, -1.0, -1.0,  -1.0]])

    cvfilter = cv2.filter2D(final, -1, v)
    
    return cvfilter

def Filter2D(img, matrix):
    v = np.array(matrix)

    cvfilter = cv2.filter2D(img, -1, v)
    
    return cvfilter

##img = cv2.imread('E:/tem.png')
##m = [ [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0],\
##      [0, 0, 0, 0, 1, 0, 0, 0, 0]]
##kernel = (np.array(m, np.float32)/9)
##print(kernel)
##kernel = np.ones((5,5) , np.float32) / 25
##print(np.ones((5,5), np.float32))
##a = Filter2D(img, kernel)
##cv2.imshow('aaa', a)
##cv2.waitKey(0)
##asdf
##def thresh_callback(thresh):
##    edges = cv2.Canny(blur,thresh,thresh*2)
##    drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
##    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
##    img_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
##    new_img, contours,hierarchy = cv2.findContours(img_closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
##    img_n = blur.copy()
##    for cnt in contours:
##        color = np.random.randint(0,255,(3)).tolist()  # Select a random color
##        cv2.drawContours(drawing,[cnt],0,color,2)
##        [x,y,w,h] = cv2.boundingRect(cnt)
##        print(x,y,w,h)
##        cv2.rectangle(img_n,(x,y),(x+w,y+h),(0,255,0),2)
##        cv2.imshow('output',drawing)
##    cv2.imshow('input',img_n)
##
##img = cv2.imread('E:/tem5.png')
##img = filterProcess(img, filter_core=27, zoom=1)
##
##gray = img#cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
####blur = Filter2D(img, kernel)#cv2.GaussianBlur(gray,(21,21),0)
##blur = cv2.GaussianBlur(gray,(17,17),0)
##cv2.namedWindow('input',cv2.WINDOW_AUTOSIZE)
##
##thresh = 100
##max_thresh = 255
##
##cv2.createTrackbar('canny thresh:','input',thresh,max_thresh,thresh_callback)
##
##thresh_callback(thresh)
##
##if cv2.waitKey(0) == 27:
##    cv2.destroyAllWindows()
##asdf
##global g_i
##g_i = 0

def drawHistImg(im):
    h = np.zeros((300,256,3))
    if len(im.shape)!=2:
        print("hist_lines applicable only for grayscale images")
        #print("so converting image to grayscale for representation"
        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('input2',cv2.WINDOW_AUTOSIZE)
    
    hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        print(x, y[0])
        cv2.line(h,(x,0),(x,y),(255,255,255))

    y = np.flipud(h)
    cv2.imshow('input2', y)
    return y


def Find(img, template, matchvalue=0):
    trows,tcols = template.shape[:2] 

    result = cv2.matchTemplate(img, template, matchvalue)

    cv2.normalize(result,result,0,255,cv2.NORM_MINMAX)

    mini,maxi,(mx,my),(Mx,My) = cv2.minMaxLoc(result)    # We find minimum and maximum value locations in result

    if matchvalue in [0,1]: # For SQDIFF and SQDIFF_NORMED, the best matches are lower values.
        MPx,MPy = mx,my
    else:                   # Other cases, best matches are higher values.
        MPx,MPy = Mx,My
    
    ## Normed methods give better results, ie matchvalue = [1,3,5], others sometimes shows errors
    
    #cv2.imwrite('opencv.png', img2)
    #print(MPx, MPy, MPx+tcols, MPy+trows)
    return (MPx, MPy, MPx+tcols, MPy+trows)

def drawColorHistogram(img):
    hsv_map = np.zeros((180, 256, 3), np.uint8)
    h, s = np.indices(hsv_map.shape[:2])
    hsv_map[:,:,0] = h
    hsv_map[:,:,1] = s
    hsv_map[:,:,2] = 255
    hsv_map = cv2.cvtColor(hsv_map, cv2.COLOR_HSV2BGR)
##    cv2.imshow('hsv_map', hsv_map)
    
    hist_scale = 10
    small = cv2.pyrDown(img)

    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    dark = hsv[...,2] < 32
    hsv[dark] = 0
    h = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return h
    print(cv2.compareHist(h, h, cv2.HISTCMP_CORREL))

    h = np.clip(h*0.005*hist_scale, 0, 1)
    vis = hsv_map*h[:,:,np.newaxis] / 255.0
    
    return vis

def getColorHist(img):
    small = cv2.pyrDown(img)

    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    dark = hsv[...,2] < 32
    hsv[dark] = 0
    h = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return h

def CompareColorHist(img0, img1):
    h0 = getColorHist(img0)
    h1 = getColorHist(img1)
    return cv2.compareHist(h0, h1, cv2.HISTCMP_CORREL)

##img = cv2.imread('../select0.png')
##ha,wa = img.shape[:2]
##img = cv2.resize(img, (int(wa*1), int(ha*1)))
##template = cv2.imread('../emplate.png')
##template = cv2.resize(template, (int(wa*1), int(ha*1)))
####x, y , w, h = Find(img, template)
####cv2.rectangle(img,(x,y),(w,h),(0,255,0),2)
####cv2.imshow('asdf', img)
##h = drawColorHistogram(img)
##h1 = drawColorHistogram(template)
##print(cv2.compareHist(h, h1, cv2.HISTCMP_CORREL))
##cv2.imshow('hist', drawColorHistogram(img))
##cv2.imshow('hist1', drawColorHistogram(template))

##x = drawHistImg(img)
##cv2.imshow('asdf', x)
##y = drawHistImg(template)
##cv2.imshow('asdf1', y)
##cv2.waitKey(0)
##asdf


def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out



def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape)/2)
  rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape,flags=cv2.INTER_LINEAR)
  return result



def FeatureMatching(img1, img2, distance=0.75, draw=False):
    img1 = toGray(img1)
    ha,wa = img1.shape[:2]
    if ha < 25 and wa < 25:
        img1 = cv2.resize(img1, (int(wa*1.5), int(ha*1.5)))
    img2 = toGray(img2)
    ha,wa = img2.shape[:2]
    if ha < 25 and wa < 25:
        img2 = cv2.resize(img2, (int(wa*1.5), int(ha*1.5)))

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

##    rows1 = img1.shape[0]
##    cols1 = img1.shape[1]
##    rows2 = img2.shape[0]
##    cols2 = img2.shape[1]
##
##    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Apply ratio test
    good = []
    pos1 = []
    pos2 = []
    try:
        for m,n in matches:
            if m.distance < distance*n.distance:
                img1_idx = m.queryIdx
                img2_idx = m.trainIdx

                (x1,y1) = kp1[img1_idx].pt
                (x2,y2) = kp2[img2_idx].pt
                pos1.append((x1,y1))
                pos2.append((x2,y2))
                good.append([m])
    except:
        if draw:
            return None, None
        return None
    if draw:
        img4 = np.zeros((1,1))
        # cv2.drawMatchesKnn expects list of lists as matches.
        img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,img4,flags=2)
        cv2.imshow('asdf', img3)
        return pos1, pos2, img3
    return pos1, pos2

img1 = cv2.imread('E:/Font3.png',0)
ha,wa = img1.shape[:2]
print(ha,wa)
img1 = cv2.resize(img1, (int(wa*1.5), int(ha*1.5)))
img2 = cv2.imread('E:/Font11.png',0)
ha,wa = img2.shape[:2]
img2 = cv2.resize(img2, (int(wa*1.5), int(ha*1.5)))
FeatureMatching(img1, img2, distance=0.3, draw=True)
cv2.waitKey(0)
asdf

def OCRInit():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    ##print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'libtesseract'

    langs = tool.get_available_languages()
    ##print("Available languages: %s" % ", ".join(langs))
    for lang in langs:
        if lang == 'eng':
            return tool, lang
    return None, None
##     Ex: Will use lang 'fra'
##     Note that languages are NOT sorted in any way. Please refer
##     to the system locale settings for the default language
##     to use.
##g_i = 0

##        print(x,y)
##        cv2.line(h,(x,0),(x,y),(255,255,255))
##    y = np.flipud(h)
##    return y


def GetBrightnessHistData(img):
    h = np.zeros((300,256,3))
    if len(img.shape)!=2:
        #print("so converting image to grayscale for representation"
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    hist_item = cv2.calcHist([img],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    
    hist=np.int32(np.around(hist_item))
##    for x,y in enumerate(hist):
##        print(x, y[0])
##        cv2.line(h,(x,0),(x,y),(255,255,255))
    return hist

##img = cv2.imread('tem.png')
##img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##img_his = drawHistImg(img)
##cv2.namedWindow('input',cv2.WINDOW_AUTOSIZE)
##cv2.imshow('input', img_his)
##
##if cv2.waitKey(0) == 27:
##    cv2.destroyAllWindows()


def DetectLetter(img, thresh, blur=(5,5), filter=False, zoom=2.5, filter_core=25):
    if filter:
        grey = filterProcess(img, zoom=zoom, filter_core=filter_core)
    else:
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(grey, blur,0)
    edges = cv2.Canny(blur, thresh, thresh*2)
    drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    img_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    new_img, contours,hierarchy = cv2.findContours(img_closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    rect_arr = []
    for cnt in contours:
        color = np.random.randint(0,255,(3)).tolist()  # Select a random color
        cv2.drawContours(drawing,[cnt],0,color,2)
        [x,y,w,h] = cv2.boundingRect(cnt)
        cv2.rectangle(grey,(x,y),(x+w,y+h),(0,255,0),2)

        x,y,w,h = cv2.boundingRect(cnt)
        if filter and zoom > 1:
            x0,y0,x1,y1 = x, y, x+w, y+h
            x,y,w,h = int(x0/zoom),int(y0/zoom),int(x1/zoom)-int(x0/zoom),int(y1/zoom)-int(y0/zoom)
        rect_arr.append([x,y,w,h])
    cv2.imshow('asdf', grey)
    cv2.waitKey(0)
    return rect_arr

def ocr_beauty(im):
    h = np.zeros((300,256,3))
    if len(im.shape)!=2:
        print("hist_lines applicable only for grayscale images")
        #print("so converting image to grayscale for representation"
        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    
    hist=np.int32(np.around(hist_item))
    print(hist[255])
    for x,y in enumerate(hist):
        if 20 < x < 230 and y >50:
            return False
    return True


def DoOCR(ocr_tool, ocr_lang, img, filter=True, zoom=2.5):
    if filter:
        img_grey = filterProcess(img, zoom=zoom)
    else:
        img_grey = img
##    plt.hist(img.ravel(),256,[0,256]);
##    plt.show()
##    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    w,h = img_grey.shape[::-1]
    bt = ocr_beauty(img_grey)
##    cv2.imshow('image0',img_grey)
    if not bt:
        for x_i in range(len(img_grey)):
            y_border = len(img_grey[x_i])/20
            for y_i in range(len(img_grey[x_i])):
                if y_i < y_border or y_i > (len(img_grey[x_i])-15):
                    img_grey[x_i][y_i] = 255
                    continue
                if 100 < img_grey[x_i][y_i] < 230:
                    img_grey[x_i][y_i] = 255
##                if img_grey[x_i][y_i] > 230:
##                    # break border
##                    if y_i < y_border:
##                        continue
##                    img_grey[x_i][y_i] = 0#img_grey[x_i][y_i]
##                elif img_grey[x_i][y_i] < 177:
##                    img_grey[x_i][y_i] = 255
    cv2.imshow('image1',img_grey)
    
##    cv2.namedWindow('histogram',cv2.WINDOW_AUTOSIZE)
##    cv2.namedWindow('image',cv2.WINDOW_AUTOSIZE)
##    cv2.imshow('histogram',lines)
    
##    cv2.imwrite('aaa.png', img)
##    if cv2.waitKey(0) == 27:
##        cv2.destroyAllWindows()   
    pil_im = Image.fromarray(img_grey)
    txt = ocr_tool.image_to_string(
        pil_im,
        lang=ocr_lang,
        builder=pyocr.builders.TextBuilder()
    )
    return txt

##tool,lang = OCRInit()
##img = cv2.imread('../tem3.png')
##ocr_txt = DoOCR(tool, lang, img)
####drawHistImg(img)
##print(ocr_txt)
##cv2.waitKey()
##asdf
##
##orh, orw = img.shape[:2]
##print(orh, orw)
####grep = filterProcess(img)
##
##ele_rects = DetectLetter(img, 53, (17, 17),filter=True, zoom=1)
##for ele_rect in ele_rects:
##    x,y,w,h = (ele_rect[0], ele_rect[1], ele_rect[2], ele_rect[3])
####    x0,y0,x1,y1 = ele_rect[0], ele_rect[1], ele_rect[0]+ele_rect[2], ele_rect[1]+ele_rect[3]
####    print(x0,y0,x1,y1)
####    x2,y2,w2,h2 = int(x0/2.5),int(y0/2.5),int(x1/2.5)-int(x0/2.5),int(y1/2.5)-int(y0/2.5)
####    print(x2,y2,w2,h2)
##
##    #ele_img = img[ele_rect[1]:ele_rect[1]+ele_rect[3], ele_rect[0]*2.5:ele_rect[0]*2.5+ele_rect[2]*2.5]
##    ele_img = img[y:y+h,x:x+w]
##    cv2.imshow('bb', ele_img)
##    cv2.waitKey()
##
##    ocr_txt = DoOCR(tool, lang, ele_img)
##    print(ocr_txt)
##asadf

def drawDiffRange(img1, x_r, y_r):
    cv2.line(img1, (min(y_r), min(x_r)), (max(y_r), min(x_r)), (0,0,0))
    cv2.line(img1, (min(y_r), min(x_r)), (min(y_r), max(x_r)), (0,0,0))
    cv2.line(img1, (max(y_r), max(x_r)), (max(y_r), min(x_r)), (0,0,0))
    cv2.line(img1, (max(y_r), max(x_r)), (min(y_r), max(x_r)), (0,0,0))
    cv2.imshow("foo",img1)
    cv2.waitKey()
    

def DetectDiffRange(imgL, imgR, disparities=16, blur=(5,5), filter_core=25):
    imgL = toGray(imgL)
    imgR = toGray(imgR)
    if blur != (-1,-1):
        imgL = cv2.GaussianBlur( cv2.equalizeHist(imgL),blur, 0)
        imgR = cv2.GaussianBlur( cv2.equalizeHist(imgR),blur, 0)

    imgL = filterProcess(imgL, zoom=1, filter_core=filter_core)
    imgR = filterProcess(imgR, zoom=1, filter_core=filter_core)

    # disparity range is tuned for 'aloe' image pair
##    cv2.imshow("org",imgL)
##    cv2.imshow("after",imgR)
    window_size = 3
    min_disp = 16
    num_disp = 112-min_disp

    stereo = cv2.StereoSGBM_create(
        minDisparity = 0,          
        numDisparities = disparities,        
        blockSize = window_size,
        uniquenessRatio = 15,       
        speckleWindowSize = 50,      
        speckleRange = 16,          
        disp12MaxDiff = 0,          
        P1 = 8*3*window_size**2,    
        P2 = 32*3*window_size**2             
    )

    disp = stereo.compute(imgL, imgR)
    disp = cv2.normalize(disp, disp, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
##    cv2.imshow("disp",disp)
    
    hist=np.int32(np.around(disp))
    x_range = []
    y_range = []
    for x,y in enumerate(hist):
        if y.max() > 50:
##            print(x,y)
            x_range.append(x)
            for y_i, y_j in enumerate(np.nonzero(y > 50)):
                for yy in y_j:
                    if yy not in y_range:
                        y_range.append(yy)
    return x_range, y_range


##img0 = cv2.imread('../orgimg.png')
####gray = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
####imgL = cv2.GaussianBlur( cv2.equalizeHist(gray),(5,5), 0)
##img1 = cv2.imread('../afterimg.png')
##x_r, y_r = DetectDiffRange(img0, img1, (-1,-1), 25)
##print(min(y_r), min(x_r), max(y_r) - min(y_r), max(x_r) - min(x_r))
##drawDiffRange(img1, x_r, y_r)
######
##asdf

def camshift_demo():
    # take first frame of the video
    frame = cv2.imread('E:/bb.png')#cv2.imread('E:\\work\\quality_control\\SET\\Python\\FXUIA\\demo\\small.png')
##    print(frame.shape)
    
    ha,wa = frame.shape[:2]
    frame = cv2.resize(frame, (int(wa*2.5), int(ha*2.5)))
    print(wa,ha)
    
    # setup initial location of window
    r,h,c,w = 0,120,0,180  # simply hardcoded the values
    track_window = (c,r,w,h)

    cv2.rectangle(frame, (r, c), (r+w, c+h), (0,0,255), 2)
    
    # set up the ROI for tracking
    roi = frame[r:r+h, c:c+w]
##    print(roi)
    cv2.imshow('img2asdfas',roi)

    hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))

    roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

##    while(1):
    print(w, h)
    frame = cv2.resize(frame, (int(wa*3), int(ha*3)))#cv2.imread('E:/bb.png')#cv2.imread('E:\\work\\quality_control\\SET\\Python\\FXUIA\\demo\\big.png')
##    cv2.imshow('imge22a',frame)
    vis = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

    # apply meanshift to get the new location
    ret, track_window = cv2.CamShift(dst, track_window, term_crit)

    # Draw it on image
    print(ret)
##    pts = cv2.boxPoints(ret)
##    pts = np.int0(pts)
    cv2.ellipse(vis, ret, (0, 0, 255), 2)
##    img2 = cv2.polylines(frame,[pts],True, 255,2)
    cv2.imshow('img2aaas',vis)
    
    k = cv2.waitKey()

    cv2.destroyAllWindows()
    
def thresh_callback(thresh):
    global img_rgb
    contours = DetectLetter(img_rgb, thresh)
##    edges = cv2.Canny(blur,thresh,thresh*2)
    drawing = np.zeros(img_rgb.shape,np.uint8)     # Image to draw the contours
##    contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        color = np.random.randint(0,255,(3)).tolist()  # Select a random color
        cv2.drawContours(drawing,[cnt],0,color,2)
        cv2.imshow('output',drawing)
    cv2.imshow('input', img_rgb)

        



