import cv2
import time
import numpy as np
from PIL import ImageGrab
##import pytesseract
##
##print(cv2.__version__)
##sdf
im=ImageGrab.grab(bbox=(10,10,510,510)) # X1,Y1,X2,Y2
im.save('grab.png')

img_rgb = cv2.imread('E:/mantis-53554-CA3821_Page_0.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = img_gray[100:250,20:200]

cv2.namedWindow("patch",1)
cv2.imshow('patch', template)
w, h = template.shape[::-1]
##print(template.shape)

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
##print(res)
threshold = 0.8
# x if condition else y
loc = np.where( res >= threshold)
##print(loc)
print(loc[::-1])
for pt in zip(*loc[::-1]):
    print(pt)
##    print(w, h)
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)
if (cv2.waitKey() & 255) == 27:
        asdf
fe
drag_start = None
sel = (0,0,0,0)

def onmouse(event, x, y, flags, param):
    global drag_start, sel, img
    if event == cv.EVENT_LBUTTONDOWN:
        drag_start = x, y
        sel = 0,0,0,0
    elif event == cv.EVENT_LBUTTONUP:
        if sel[2] > sel[0] and sel[3] > sel[1]:
            patch = gray[sel[1]:sel[3],sel[0]:sel[2]]
            result = cv.matchTemplate(gray,patch,cv.TM_CCOEFF_NORMED)
            result = np.abs(result)**3
            val, result = cv.threshold(result, 0.01, 0, cv.THRESH_TOZERO)
            result8 = cv.normalize(result,None,0,255,cv.NORM_MINMAX,cv.CV_8U)
            cv.imshow("result", result8)
        drag_start = None
    elif drag_start:
        #print flags
        if flags & cv.EVENT_FLAG_LBUTTON:
            minpos = min(drag_start[0], x), min(drag_start[1], y)
            maxpos = max(drag_start[0], x), max(drag_start[1], y)
            sel = minpos[0], minpos[1], maxpos[0], maxpos[1]
##            img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
            # x, y, width, height
            print((sel[0], sel[1]), (sel[2], sel[3]))
            cv.rectangle(img, (sel[0], sel[1]), (sel[2], sel[3]), (0,255,255), 1)
            cv.imshow("gray", img)
        else:
            print "selection is complete"
            drag_start = None
            
if __name__ == '__main__':
    global img
    img = cv.imread('E:/mantis-53554-CA3821_Page_0.png',0)

    w, h = img.shape[::-1]
##    cv.namedWindow("patch",1)
    patch = img[100:200,0:100]
##    cv.setMouseCallback("gray", onmouse)
##    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
##    cv2.imwrite('as.png', img)
    ##print(img)
##    cv.imshow('patch', patch)
##
##    time.sleep(5)
##    cv.imshow("gray",patch)
    
##    time.sleep(3)
    method = cv.TM_SQDIFF
    result = cv.matchTemplate(img, patch, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print(min_val, max_val, min_loc, max_loc)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    print(top_left, bottom_right)
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    
    cv.namedWindow("match",1)
##    match_img = img[pos[2][0]:pos[2][1], pos[3][0]:pos[3][1]]
    cv.imshow('match', img)
    if (cv.waitKey() & 255) == 27:
        asdf

    
##    print(result)
##    result = np.abs(result)**3
##    val, result = cv.threshold(result, 0.01, 0, cv.THRESH_TOZERO)
##    result8 = cv.normalize(result,None,0,255,cv.NORM_MINMAX,cv.CV_8U)
##    print(result8)
##    cv.imshow("gray", result8)
##    cv.destroyAllWindows()
##    cv.matchTemplate()
