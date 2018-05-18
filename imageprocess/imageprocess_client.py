
from __future__ import print_function

import grpc

import imageprocess_pb2

import Levenshtein
import subprocess
import os
import time
import math, operator
import StringIO
import zlib
from PIL import Image, ImageDraw, ImageMath, ImageChops

import platform

# Set Position
cmd_str = '''tell application "System Events"
    set position of first window of application process "Foxit Reader" to {100, 100}
end tell '''

# Activate
cmd_str = '''activate application "Foxit Reader"'''

# Finder Menu
cmd_str = '''activate application "Finder"
tell application "System Events" to tell process "Finder"
    click menu item "New Finder Window" of menu 1 of menu bar item "File" of menu bar 1
end tell'''

# Foxit Reader Mene Controll
cmd_str = '''activate application "Foxit Reader"
delay 1
tell application "System Events" to tell process "Foxit Reader"
    click menu item "Open" of menu 1 of menu bar item "File" of menu bar 1
end tell'''

# Get Size
cmd_str = '''activate application "Foxit Reader"
delay 1
tell application "System Events" to tell process "Foxit Reader"
    get size of window 1
end tell'''

# Get Position
cmd_str = '''activate application "Foxit Reader"
delay 1
tell application "System Events" to tell process "Foxit Reader"
    get position of window 1
end tell'''

# UI Element
cmd_str = '''tell application "System Events"
tell process "Foxit Reader"
set visible to true
return every UI element of front window
return name of every UI element of front window
end tell
end tell'''

## Click 'Cancel' Button in OpenDialog
cmd_str = '''activate application "Foxit Reader"
tell application "System Events" to tell process "Foxit Reader"
    click menu item "Open" of menu 1 of menu bar item "File" of menu bar 1
    click button "Cancel" of window 1
end tell'''

## Open file from OpenDialog
#cmd_str = '''activate application "Foxit Reader"
#set strPath to POSIX file "/Users/linfeiyun/Desktop/work/RDKTest/Quick Start Guide.pdf"
#tell application "System Events" to tell process "Foxit Reader"#
#    select thefullpath
#end tell'''

cmd_str = '''activate application "Foxit Reader"'''
##applescript.AppleScript(cmd_str).run()

cmd_str = '''tell application "System Events"
tell process "Foxit Reader"
set visible to true
return every UI element of front window
end tell
end tell'''

cmd_str = '''
set allButtons to {}
tell application "System Events"
      tell process "Foxit Reader"
            with timeout of 0 seconds
                  set tElements to entire contents of window 1
            end timeout
            repeat with i in tElements
                  if class of i is button then set end of allButtons to contents of i
            end repeat
      end tell
end tell
allButtons
'''

cmd_str = '''activate application "Foxit Reader"
tell application "System Events" to tell process "Foxit Reader"
    click button "Cancel" of window 1
end tell'''

##print(len(applescript.AppleScript(cmd_str).run()))
##asdfasdf
##if platform.system() == 'Darwin':
##    res = applescript.AppleScript(cmd_str).run()
##    for r in res:
####        print(r)
####        print('=================')
##        for k in r.keys():
####            print(r[k])
####            print(r[k])
####            print('*************')
##            try:
##                for j in r[k]:
####                    print('**', r[k][j])
##                    try:
##                        for l in r[k][j]:
####                            print('***', r[k][j][l])
##                            try:
##                                for m in r[k][j][l]:
##                                    print('****', r[k][j][l][m])
##                            except:
##                                print('==========')
##                                print('normal:', r[k][j][l])
##                                print('==========')
##                    except:
##                        print(r[k][j])
##            except:
##                print(r[k])
####            if k == applescript.AEType('from'):
####                print('----',r[k])
####            try:
####                for kk in r[k].keys():
####                    continue
####                    print('-----')
####                    print(r[k][kk])
####            except:
####            if k == applescript.AEType('indx'):
####                print(r[k])
##
##            
##asdfsdf

if platform.system() == 'Darwin':
    reader = 'Foxit Reader'


def pilimg_to_buf(pil_img):
    output = StringIO.StringIO()
    pil_img.save(output, format="PNG")
    contents = output.getvalue()
    output.close()
    return zlib.compress(contents)

def GetImageServerStub():
    global g_stub
    return g_stub
    
def cv2pos2pil(cv2pos):
    return ((cv2pos[0], cv2pos[1]),(cv2pos[0]+cv2pos[2], cv2pos[1]+cv2pos[3]))

def FoxitReader_ParseUI(stub, user_rect=None):
    img = FoxitReader_GetImg(user_rect)
    img.save('tem.png')
    
    img_buf = pilimg_to_buf(img)
    eles = stub.DetectElements(\
        imageprocess_pb2.DetectImg(imgobj=img_buf, \
                                   thresh=123, \
                                   blur=imageprocess_pb2.Blur(x=5, y=5), \
                                   filter=imageprocess_pb2.FilterP(enable=False, zoom=1)))
    ele_rect = []
    txt_pos_map = {}
    for ele in eles:
##        if ele.w > 100 or ele.h > 100:
##            continue
        e_r = (ele.x, ele.y, ele.w, ele.h)
        ele_rect.append(e_r)
        #print('x:%d, y:%d, w:%d, h:%d' % (ele.x, ele.y, ele.w, ele.h))
        ele_img = img.crop((ele.x, ele.y,ele.x+ele.w, ele.y+ele.h))
        #print(ele_img)
        img_buf = pilimg_to_buf(ele_img)
        ocr_txt = stub.OCR(imageprocess_pb2.ImgRequest(imgobj=img_buf))
        txt = (ocr_txt.txt).encode('utf8')
        txt_pos_map[txt] = (ele.x, ele.y, ele.w, ele.h)
        print(txt)
        #dr.rectangle(((ele.x, ele.y),(ele.x+ele.w, ele.y+ele.h)), outline = "red")
    #image.save('tem.png')
    return txt_pos_map

    
def GetElementPosByName(ele_name, ele_name_map, lowercase=False):
    posl = []
    for name in ele_name_map.keys():
        if name == '' or name == None:
            continue  
        print(name+'**'+ele_name, Levenshtein.ratio(name, ele_name), ele_name_map[name])
        if lowercase:
            if Levenshtein.ratio(name.lower(), ele_name.lower()) >= 0.7:
                pos = ele_name_map[name]
                posl.append(pos)
        else:
            if Levenshtein.ratio(name.lower(), ele_name.lower()) >= 0.7:
                pos = ele_name_map[name]
                posl.append(pos)
    return posl

def GetElementPosByImg(stub, img, template_img):
    img_buf = pilimg_to_buf(img)
    temp_buf = pilimg_to_buf(template_img)
    img_rect = stub.FindImage(imageprocess_pb2.FindImgRequest(imgobj=img_buf, templateobj=temp_buf))
    return (img_rect.x0, img_rect.y0, img_rect.x1, img_rect.y1)

def FoxitReader_Open(testfile):
    if platform.system() != 'Darwin':
        subprocess.Popen(['FoxitReader', testfile])
    else:
        subprocess.Popen(['/Applications/Foxit Reader.app/Contents/MacOS/FoxitReader', testfile])
##        activateApplication('Foxit Reader')
##    time.sleep(4)
##    os.environ["QT_ACCESSIBILTY"] = "1"
##    os.environ["QT_LINUX_ACCESSIBILITY_ALWAYS_ON"] = "1"
##    ldtp.launchapp('FoxitReader', delay = 5, env = 1)
##    ldtp.activatewindow('*Foxit Reader')
##    time.sleep(1)
####    print(ldtp.getapplist())
##    print(ldtp.getwindowlist())
##    print(ldtp.getwindowsize('*Foxit Reader'))
##    print(ldtp.getobjectlist('*Foxit'))


##
##root = display.screen().root
##printWindowHierrarchy(root, '-')
##getWindowRect(0x4800006)
##ds_size = getDesktopScreenSize()
##print(ds_size)
##

##wnd = getWindowFromPointer()
##print(wnd)
##setTopWindow(reader)
##moveWindow(reader, 0, 0)
####resizeWindow(reader, ds_size[0], ds_size[1])
##reader_child = getWindowChildren(reader)
##print(reader_child)
##reader_geo = getWindowGeo(reader)
##print(reader_geo)
##reader_rect = getWindowRect(reader)
##print(reader_rect)
##asdf


def _adjust_pos(r0, r1):
    r = 0
    if r1 == 0:
        r = r0
    elif abs(r1) > 1:
        r = int(r0 + r1)
    else:
        r = int(r0 * r1)
    return r

def _adjust_size(r0, r1):
    r = 0
    if r1 == 0:
        r = int(r0)
    elif r1 > 1:
        if r1 > r0:
            r = int(r0)
        else:
            r = int(r1)
    elif r1 < 0:
        r = int(r0 + r1)
    else:
        r = int(r0 * r1)
    return r

def compareImg(img0, img1):
    h1 = img0.histogram()
    h2 = img1.histogram()
 
    rms = math.sqrt(reduce(operator.add, \
                           map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return rms

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    h = ImageChops.difference(im1, im2).histogram()
    print(h)
    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))


def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def seleced_color_change(img, ele_type=0):
    pixdata = img.load()
    # Clean the background noise, if color != white, then set to black.
    # change with your color
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
##            print(pixdata[x, y])
            if ele_type == 0:
                if pixdata[x, y] == (255, 255, 255):
                    pixdata[x, y] = (108, 180, 255)
                elif pixdata[x, y] >= (50, 50, 50):
                    pixdata[x, y] = (255, 255, 255)
            else:
                if platform.system() != 'Darwin':
                    if pixdata[x, y] != (255, 255, 255):
                        pixdata[x, y] = (108, 180, 255)
                else:
                    if x < img.size[0]/5 and \
                       pixdata[x, y] != (220, 220, 220):
                        pixdata[x, y] = (108, 180, 255)
    return img

def FoxitReader_Top():
    global reader
    print(reader)
    print(setTopWindow(reader))
    while not setTopWindow(reader):
        print('set top')
        time.sleep(0.2)

def FoxitReader_Move(x, y):
    for attempt in range(10):
        try:
            moveWindow(reader, x, y)
        except:
            time.sleep(0.5)
            FoxitReader_Top()
        else:
            break

def FoxitReader_Resize(w, h):
    if w == -1 and h == -1:
        if platform.system() != 'Darwin':
            reader_rect = getWindowRect(reader)
            sw, sh = getScreenSize()
            if reader_rect[0] + reader_rect[2] == sw and \
               reader_rect[1] + reader_rect[3] == sh:
                return
            g_m.move(reader_rect[0]+reader_rect[2]/2, reader_rect[1]-5)
            g_m.click(reader_rect[0]+reader_rect[2]/2, reader_rect[1]-5)
            g_m.click(reader_rect[0]+reader_rect[2]/2, reader_rect[1]-5)
            return
    resizeWindow(reader, w, h)

def FoxitReader_ClickPos(pos):
    reader_rect = getWindowRect(reader)
    print('ReaderRect:', reader_rect)
    g_m.move(pos[0]+reader_rect[0], pos[1]+reader_rect[1])
    g_m.click(pos[0]+reader_rect[0], pos[1]+reader_rect[1])
    print('ClickPos:', pos[0]+reader_rect[0], pos[1]+reader_rect[1])

def FoxitReader_GetImg(user_rect=None, covert_flag=None):
    reader_rect = getWindowRect(reader)
    print(reader_rect)
    x = reader_rect[0]
    y = reader_rect[1]
    w = reader_rect[0] + reader_rect[2]
    h = reader_rect[1] + reader_rect[3]
    if user_rect != None:
        x = _adjust_pos(reader_rect[0], user_rect[0])
        y = _adjust_pos(reader_rect[1], user_rect[1])
        w = x + _adjust_size(reader_rect[2], user_rect[2])
        h = y + _adjust_size(reader_rect[3], user_rect[3])
    FoxitReader_Top()
    print(user_rect)
    print(x, y, w,h)
    img = ImageGrab.grab().crop((x, y, w, h))
    if covert_flag != None:
        img = img.convert(covert_flag) 

    return img  

        
def NextPage(stub):
    template = Image.open('nextpage.png')
    reader_rect = getWindowRect(reader)
    FoxitReader_Top()
    print(reader_rect)
    img = ImageGrab.grab(bbox=(reader_rect[0], \
                               reader_rect[1], \
                               reader_rect[0]+reader_rect[2], \
                               reader_rect[1]+reader_rect[3]))
##    print(image)
##    image.save('save.png')
##    time.sleep(3)
    next_ele_pos = GetElementPosByImg(stub, img, template)
    print('MouseMove:', next_ele_pos[0]+reader_rect[0], next_ele_pos[1]+reader_rect[1])
    g_m.move(next_ele_pos[0]+reader_rect[0], next_ele_pos[1]+reader_rect[1])
    g_m.click(next_ele_pos[0]+reader_rect[0], next_ele_pos[1]+reader_rect[1])
    print('END:', next_ele_pos[0]+reader_rect[0], next_ele_pos[1]+reader_rect[1])
    print(next_ele_pos)

def FoxitReader_UI_SelectConnect(stub, ele_name_map):
    ele_pos = GetElementPosByName('Connect', ele_name_map)[0]
    if ele_pos != None:
        reader_rect = getWindowRect(reader)
        g_m.move(ele_pos[0]+reader_rect[0], ele_pos[1]+reader_rect[1])
        g_m.click(ele_pos[0]+reader_rect[0], ele_pos[1]+reader_rect[1])

def FoxitReader_UI_SelectComments(stub, ele_name_map):
    ele_pos = GetElementPosByName('Comments', ele_name_map)[0]
    if ele_pos != None:
        reader_rect = getWindowRect(reader)
        g_m.move(ele_pos[0]+reader_rect[0], ele_pos[1]+reader_rect[1])
        g_m.click(ele_pos[0]+reader_rect[0], ele_pos[1]+reader_rect[1])

def FoxitReader_Comments_Pencil(stub):
    template = Image.open('img/ReaderLite/ubuntu/comments_pencil.png')
    img = GetReaderImg()
    img.save('/home/xiaoxia_yu/Desktop/ReaderLite.png')
    template.save('/home/xiaoxia_yu/Desktop/template.png')
    pos = GetElementPosByImg(stub, img, template)
    mid_pos = (pos[0] + (pos[2]-pos[0])/2, pos[1]+(pos[3]-pos[1])/2)
    if pos != None:
        print('click:', mid_pos)
        FoxitReader_ClickPos(mid_pos)

def FoxitReader_UI_IsSelect(stub):
    pass


    
def FoxitReader_SelectUI(stub, ui_name, selected=-1, dropdown=False):
    template = Image.open('img/ReaderLite/Ubuntu/%s.png' % (ui_name))
##    template = Image.open('/home/xiaoxia_yu/Desktop/colorchage.png')
    template = template.convert('RGB')
    img = FoxitReader_GetImg()
    img.save('ReaderLite.png')
    template.save('emplate.png')
    pos = GetElementPosByImg(stub, img, template)
    ele_img = img.crop(pos)
    ele_img = ele_img.convert('RGB')
    ele_img.save('select.png')
    match = stub.DetectSimilarity(\
        imageprocess_pb2.CmpImgRequest(orgimgobj=pilimg_to_buf(ele_img), \
                                       cmpimgobj=pilimg_to_buf(template)))
    match_l = []
    for m in match:
        print(m)
        match_l.append(m)
    print('==========')
    print(match_l)
    print('==========')
    #if compareImg(ele_img, template) != 0:
    if len(match_l) < 3:
        if selected == 1:
            return
        if ui_name.find('-') == -1:
            template = seleced_color_change(template, 0)
        else:
            template = seleced_color_change(template, 1)
            template.save('template_color.png')
        print('color chage')
        template.save('template_change.png')
        pos = GetElementPosByImg(stub, img, template)

    mid_pos = (pos[0] + (pos[2]-pos[0])/2, pos[1]+(pos[3]-pos[1])/2)
    if pos != None:
        print('click:', mid_pos)
        FoxitReader_ClickPos(mid_pos)

##def FoxitReader_GetVisiableRect():
##    if platform.system() == 'Darwin':
##        fx_x, fx_y, fx_w, fx_h = getWindowRect('Foxit Reader')
##        sc_w,sc_h = getScreenSize()
##        if fx_x + fx_w > sc_w:
##            w = fx_x + fx_w - sc_w


        
def FoxitReader_WaitWindow(winTitle='', timeout=10):
    if platform.system() == 'Darwin':
        for i in range(timeout):
            if getFrontWindowTitle() != winTitle:
                time.sleep(1)
            else:
                return True
    else:
        global visible_windows
        for i in range(timeout):
            current_windows = getVisibleWindows()
            print('===================')
            print(len(current_windows))
            print(len(visible_windows))
            print('===================')
            if len(current_windows) == len(visible_windows):
                time.sleep(1)
            else:
                visible_windows = current_windows
                time.sleep(2)
                return True
    return False

def FoxitReader_WaitConnect(stub, timeout=10):
    for i in range(timeout):
        img = GetReaderImg()
        img_buf = pilimg_to_buf(img)
        hist = stub.GetHistArray(imageprocess_pb2.ImgRequest(imgobj=img_buf))
        hist_arr = []
        for data in hist:
            hist_arr.append(data.y)
        if hist_arr[255] != 255:
            time.sleep(1)
            print('Connect Wait.')
        else:
            print('Connect OK.')
            return True
        
    return False

def getFoxitReader(all_windows):
    for win in all_windows:
        if win['class'] != None:
            for classname in win['class']:
                if classname.find('FoxitReader') != -1:
                    setTopWindow(win['obj'])
                    return win['obj']
                
def Init():
    if platform.system() == 'Darwin':
        return
    global visible_windows
    visible_windows = getVisibleWindows()
    global reader
    reader = getFoxitReader(visible_windows)
    
def FoxitReader_Menu(stub, menu_name):
    if platform.system() == 'Darwin':
        return
    aa = _foxitReaderMenu(stub, menu_name)
    aa.clickMain()
    aa.clickChild()

class _foxitReaderBase:
    def __init__(self, stub, select_name):
        self.preimg = None
        self.afterimg = None
        self.select_name = select_name
        self.click_name = None
        self.stub = stub
        self.menu_offset = None
        self.diff_rect = None
        self.detect_blur = None
        self.preprocess_enable = None
        self.preprocess_zoom = None

    def setDetectBlur(self, x, y):
        self.detect_blur = (x, y)

    def setPreProcess(self, enable, zoom):
        self.preprocess_enable = enable
        self.preprocess_zoom = zoom

    def getpos(self, select_map, select_name, lowercase=False):
        pos = GetElementPosByName(select_name, select_map, lowercase)[0]
        if pos == None:
##            print(menu_map)
            return None
        return pos

    def clickMain(self):
        main_select = self.select_name#select_list[0]

        self.preimg = FoxitReader_GetImg()
        self.preimg.save('orgimg.png')

        FoxitReader_SelectUI(self.stub, main_select)
        FoxitReader_WaitWindow()

        self.afterimg = FoxitReader_GetImg()
        self.afterimg.save('afterimg.png')

        self.diff_rect = self.stub.GetDiffRect(\
                imageprocess_pb2.CmpImgRequest(orgimgobj=pilimg_to_buf(self.preimg), \
                                               cmpimgobj=pilimg_to_buf(self.afterimg)))

    def clickChild(self, select_name):
        diff_img = self.afterimg.crop((self.diff_rect.x, \
                                           self.diff_rect.y, \
                                           self.diff_rect.x+self.diff_rect.w, \
                                           self.diff_rect.y+self.diff_rect.h))
        diff_img.save('popup_window.png')
        print(self.diff_rect)

        img_buf = pilimg_to_buf(diff_img)
        eles = self.stub.DetectElements(\
            imageprocess_pb2.DetectImg(imgobj=img_buf, \
                               thresh=53, \
                               blur=imageprocess_pb2.Blur(x=self.detect_blur[0], y=self.detect_blur[1]), \
                               filter=imageprocess_pb2.FilterP(enable=self.preprocess_enable, zoom=self.preprocess_zoom)))
        
        ele_rect = []
        txt_pos_map = {}
        for ele in eles:
            e_r = (ele.x, ele.y, ele.w, ele.h)
            ele_rect.append(e_r)
            #print('x:%d, y:%d, w:%d, h:%d' % (ele.x, ele.y, ele.w, ele.h))
            ele_img = diff_img.crop((ele.x, ele.y,ele.x+ele.w, ele.y+ele.h))
            #print(ele_img)
            img_buf = pilimg_to_buf(ele_img)
            ocr_txt = self.stub.OCR(imageprocess_pb2.ImgRequest(imgobj=img_buf))
            txt = (ocr_txt.txt).encode('utf8')
            txt_pos_map[txt] = (ele.x, ele.y, ele.w, ele.h)
            print(txt)
        
        pos = self.getpos(txt_pos_map, select_name)
        ele_pos = (self.diff_rect.x + pos[0]+pos[2]/2, \
                        self.diff_rect.y + pos[1]+pos[3]/2)
        FoxitReader_ClickPos(ele_pos)


    def Test(self):
        print('asdf')

class _foxitReaderPopupWindow(_foxitReaderBase):
    def __init__(self, stub, select_name):
        _foxitReaderBase.__init__(self, stub, select_name)
        _foxitReaderBase.setDetectBlur(self, 17, 17)
        _foxitReaderBase.setPreProcess(self, True, 1)
        

    

class _foxitReaderMenu:
    def __init__(self, stub, menu_name):
        self.preimg = None
        self.afterimg = None
        self.menu_name = menu_name
        self.click_name = None
        self.stub = stub
        self.menu_offset = None
        self.menu_dropdown_rect = None

    def clickMain(self):
        menu_list = self.menu_name.split('-')
        main_menu = menu_list[0]

        # Get Menu Bar.
        abs_rect = (0, 0, 0, 25)
        menu_map = FoxitReader_ParseUI(self.stub, abs_rect)
        
        pos = self.getpos(menu_map, main_menu)

        # Get Image before click main menu.
        self.menu_offset = (pos[0], 25, 0.3, -25)
##        print('Orgimge Rect:', user_rect)
        img0 = FoxitReader_GetImg(self.menu_offset, 'LA')
        img0.save('orgimg.png', quality=5)

        # Click main menu.
        menu_pos = (pos[0]+pos[2]/2, \
                    pos[1]+pos[3]/2)
        print("POs:", pos)
        print("MenuPOs:", menu_pos)
        FoxitReader_ClickPos(menu_pos)
        
        time.sleep(1)

        # Get image after click main menu.
##        abs_rect = (0, 25, 0.3, -25)
        img1 = FoxitReader_GetImg(self.menu_offset, 'LA')
        img1.save('afterimg.png', quality=5)
        self.afterimg = img1.copy()

        self.menu_dropdown_rect = self.stub.GetDiffRect(\
            imageprocess_pb2.CmpImgRequest(orgimgobj=pilimg_to_buf(img0), \
                                           cmpimgobj=pilimg_to_buf(img1)))
        if self.menu_dropdown_rect.x == -1:
            return self.clickMain()

    def clickChild(self):
        menu_list = self.menu_name.split('-')
        for menu_n in menu_list[1:]:
            
            menu_img = self.afterimg.crop((self.menu_dropdown_rect.x, \
                                           self.menu_dropdown_rect.y, \
                                           self.menu_dropdown_rect.x+self.menu_dropdown_rect.w, \
                                           self.menu_dropdown_rect.y+self.menu_dropdown_rect.h))
            menu_img.save('menu_dropdown.png', quality=5)
            print(self.menu_dropdown_rect)

            img_buf = pilimg_to_buf(menu_img)
            eles = self.stub.DetectElements(\
                imageprocess_pb2.DetectImg(imgobj=img_buf, \
                                   thresh=10, \
                                   blur=imageprocess_pb2.Blur(x=17, y=17), \
                                   filter=imageprocess_pb2.FilterP(enable=True, zoom=2.5)))
            
            ele_rect = []
            txt_pos_map = {}
            for ele in eles:
                e_r = (ele.x, ele.y, ele.w, ele.h)
                ele_rect.append(e_r)
                #print('x:%d, y:%d, w:%d, h:%d' % (ele.x, ele.y, ele.w, ele.h))
                ele_img = menu_img.crop((ele.x, ele.y,ele.x+ele.w, ele.y+ele.h))
                #print(ele_img)
                img_buf = pilimg_to_buf(ele_img)
                ocr_txt = self.stub.OCR(imageprocess_pb2.ImgRequest(imgobj=img_buf))
                txt = (ocr_txt.txt).encode('utf8')
                txt_pos_map[txt] = (ele.x, ele.y, ele.w, ele.h)
                print(txt)
##            abs_rect = (0, 25, 0, -25)
            pos = self.getpos(txt_pos_map, menu_n, False)
            # Click menu.
            menu_pos = (self.menu_offset[0]+pos[0]+pos[2]/2, \
                        self.menu_offset[1]+pos[1]+pos[3]/2)
            print(menu_pos)
            FoxitReader_ClickPos(menu_pos)

    def getpos(self, menu_map, menu_name, lowercase=True):
        pos = GetElementPosByName(menu_name, menu_map, lowercase)[0]
        if pos == None:
##            print(menu_map)
            return None
        return pos

# Connect->Convert to cPDF->Password->Email->Login    
def testLogin(stub):
    FoxitReader_SelectUI(stub, 'Connect', 1)
        
    a = _foxitReaderPopupWindow(stub, 'Connect-Convert_to_cPDF')
    a.clickMain()
    a.clickChild('Password')
    g_k.type_string('abcd@fx.com')

    FoxitReader_SelectUI(stub, 'Sign_In-Email', 1)
    g_k.type_string('abcd@fx.com')
##
##    a.clickChild('Sign In')
    
def Init(server):
    channel = grpc.insecure_channel(server)
    stub = imageprocess_pb2.ImageStub(channel)
    return stub


class ImageProcesser:
    def __init__(self, server):
        channel = grpc.insecure_channel(server)
        self._stub = imageprocess_pb2.ImageStub(channel)

    def detect_elements(self, img, thresh, blur_x=5, blur_y=5, filter=False, zoom=1, filter_core=25, debug=False):
        img_buf = pilimg_to_buf(img)

        eles = self._stub.DetectElements(\
                imageprocess_pb2.DetectImg(imgobj=img_buf, \
                                           thresh=thresh, \
                                           blur=imageprocess_pb2.Blur(x=blur_x, y=blur_y), \
                                           filter=imageprocess_pb2.FilterP(enable=filter, \
                                                                           zoom=zoom, \
                                                                           core=filter_core)))
        ele_l = []
        for ele in eles:
            e_r = (ele.x, ele.y, ele.w, ele.h)
            ele_l.append(e_r)
            if debug:
                print(e_r)
                draw = ImageDraw.Draw(img)
                draw.rectangle([(ele.x, ele.y),(ele.x+ele.w, ele.y+ele.h)], outline='Red')
        if debug:
            img.show()
        return ele_l

    def find_image(self, img, template_img, debug=False):
        img_buf = pilimg_to_buf(img)
        temp_buf = pilimg_to_buf(template_img)
        img_rect = self._stub.FindImage(imageprocess_pb2.FindImgRequest(imgobj=img_buf, templateobj=temp_buf))
        if debug:
            draw = ImageDraw.Draw(img)
            draw.rectangle([(img_rect.x0, img_rect.y0),(img_rect.x1, img_rect.y1)], outline='Black')
            img.show()
        return img_rect

    def get_diff_rect(self, img0, img1, disparities=16, blur_x=-1, blur_y=-1, filter_core=25, debug=False):
        diff_rect = self._stub.GetDiffRect(\
            imageprocess_pb2.CmpImgRequest(orgimgobj=pilimg_to_buf(img0), \
                                           cmpimgobj=pilimg_to_buf(img1), \
                                           disparities = disparities, \
                                           blur=imageprocess_pb2.Blur(x=blur_x, y=blur_y), \
                                           filter_core=filter_core
                                           ))
        width, height = img0.size
        if width == diff_rect.w and height == diff_rect.h:
            return
        if debug:
            draw = ImageDraw.Draw(img0)
            draw.rectangle([(diff_rect.x, diff_rect.y),(diff_rect.x+diff_rect.w, diff_rect.y+diff_rect.h)], outline='Black')
            img0.show()
        return diff_rect

    def detect_similarity(self, img0, img1, matching_distance=0.75, debug=False):
        if debug:
            ret = self._stub.DrawSimilarity(\
                imageprocess_pb2.CmpImgRequest(orgimgobj=pilimg_to_buf(img0), \
                                               cmpimgobj=pilimg_to_buf(img1), \
                                               feature_matching_distance = matching_distance))
            img = Image.open(StringIO.StringIO(ret.imgobj))
            img.show()
            return None
        match = self._stub.DetectSimilarity(\
        imageprocess_pb2.CmpImgRequest(orgimgobj=pilimg_to_buf(img0), \
                                       cmpimgobj=pilimg_to_buf(img1), \
                                       feature_matching_distance = matching_distance))
        match_pos = []
        for m in match:
            match_pos.append((m.x0, m.x1, m.x1, m.y1))
        return match_pos

    def get_hist_array(self, img):
        img_buf = pilimg_to_buf(img)
        hist = self._stub.GetHistArray(imageprocess_pb2.ImgRequest(imgobj=img_buf))

        hist_arr = []
        for data in hist:
            hist_arr.append(data.y)
        return hist_arr

    def ocr_text(self, img):
        img_buf = pilimg_to_buf(img)
        ocr_txt = self._stub.OCR(imageprocess_pb2.ImgRequest(imgobj=img_buf))
        txt = (ocr_txt.txt).encode('utf8')
        return txt

    def compare_color_hist(self, img0, img1):
        img0_buf = pilimg_to_buf(img0)
        img1_buf = pilimg_to_buf(img1)

        d_s = self._stub.CompareColorHist(\
            imageprocess_pb2.CmpImgRequest(orgimgobj=pilimg_to_buf(img0), \
                                           cmpimgobj=pilimg_to_buf(img1)))
        return d_s.data

    def filter_2d(self, img, matrix):
        img_buf = pilimg_to_buf(img)
        m_s = ''
        for line in matrix:
            for i in line:
                m_s += str(i) + ','
        ret = self._stub.Filter2D(imageprocess_pb2.FilterRequest(imgobj=img_buf, matrix=m_s))
        return Image.open(StringIO.StringIO(ret.imgobj))

    def equal(self, im0, im1):
        return ImageChops.difference(im0, im1).getbbox() is None

    def ssim(self, img0, img1):
        img0_buf = pilimg_to_buf(img0)
        img1_buf = pilimg_to_buf(img1)
        ret = self._stub.SSIM(imageprocess_pb2.ImgCmpRequest(img0=img0_buf, img1=img1_buf))
        return ret

    def cosine_sim(self, txt0, txt1):
        ret = self._stub.CosineSim(imageprocess_pb2.TxtCmpRequest(txt0=txt0, txt1=txt1))
        return ret

    def reflow_compare_image(self, img0, img1):
        img0_buf = pilimg_to_buf(img0)
        img1_buf = pilimg_to_buf(img1)
        ret = self._stub.reflow_compare_image(imageprocess_pb2.ImgCmpRequest(img0=img0_buf, img1=img1_buf))
        return ret

    def reflow_compare_text(self, img0, img1):
        img0_buf = pilimg_to_buf(img0)
        img1_buf = pilimg_to_buf(img1)
        ret = self._stub.reflow_compare_text(imageprocess_pb2.ImgCmpRequest(img0=img0_buf, img1=img1_buf))
        return ret

    def info(self):
        return self._stub.Info(imageprocess_pb2.StringReq(reqstr=''))


def run():
    # Init()
    # FoxitReader_Resize(-1, -1)
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = imageprocess_pb2.ImageStub(channel)
    print(stub.Info(imageprocess_pb2.StringReq(reqstr='')))
    return
##    testLogin(stub)

##    print(stub)
##    FoxitReader_Menu(stub, 'File-Open')
##    FoxitReader_SelectUI(stub, 'View' )

    macmamcmacmamcmamc
    FoxitReader_Open('/Users/linfeiyun/test.pdf')
    FoxitReader_Toprr()
    FoxitReader_Move(200 , 200)
##    FoxitReader_SelectUI(stub, 'Top-Highlight')
####    time.sleep(1)
####    FoxitReader_SelectUI(stub, 'Comments')
##    FoxitReader_SelectUI(stub, 'Connect')
##    time.sleep(1)
##    FoxitReader_SelectUI(stub, 'Connect-Register_New_Version')
##    if FoxitReader_WaitWindow('Register New Version'):
##        FoxitReader_WaitConnect(stub, 20)
    

    ele_name_map = FoxitReader_ParseUI(stub)
    pos = GetElementPosByName('Register', ele_name_map)
    FoxitReader_ClickPos(pos)
##    g_m.move(380 + 200 + 20, 459+200+20)
##    g_m.click(380 + 200 + 20, 459+200+20)
    
##    NextPage(stub)
##    FoxitReader_UI_Connect(stub, ele_name_map)
##    time.sleep(1)
##    FoxitReader_UI_SelectComments(stub, ele_name_map)
  
  
    asdf
    img = Image.open('E:/ReaderLite.png')
    template = Image.open('E:/temp.png')
    pos = GetElementPosByImg(stub, img, template)
    ele_name_map = ParseElements(stub, img)
    ele_pos = GetElementPosByName('Connect', ele_name_map)

    dr = ImageDraw.Draw(img)
    print(pos)
    dr.rectangle(pos, outline = "red")
    img.save('tem.png')
##  print(ele_pos)



# if __name__ == '__main__':
#   run()
