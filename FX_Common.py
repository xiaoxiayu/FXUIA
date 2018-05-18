import os
import platform
if platform.system() == 'Windows':
    import win32api, win32con
import Levenshtein
import sys
import functools
import math
from itertools import izip
from FX_Image import FXImage



if sys.version_info.major == 3:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

    def POSTRequest(url, data):
        print(data)
        return Request(url, urlencode(data).encode())

    def ParseRespond(s):
        return urlopen(s).read().decode()

    def GetRequest(url): 
        response = urlopen(url)  
        return response

    def PutRequest(url, put_data):
        req = Request(url, data=put_data,method='PUT')
        response = urllib.request.urlopen(req)
        return response
else:
    import urllib
    import urllib2
    def POSTRequest(url, data):
        return urllib.urlopen(url, bytes(urllib.urlencode(data)))

    def ParseRespond(s):
        return s.read()

    def GetRequest(url): 
        response = urllib.urlopen(url)  
        return response

    def PutRequest(url, put_data):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(url, data=put_data)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request.get_method = lambda: 'PUT'
        response = opener.open(request)
        return response

if platform.system() == 'Windows':
    IMAGE_PROCESS = 'tools\\ImageProcess\\ImageProcessing.exe'
else:
    IMAGE_PROCESS = './tools/ImageProcess/ImageProcessing.exe'

class LastError:
    Error = ''
    def __init__(self):
        pass

    @property
    def Err(self):
        return LastError.Error

    @Err.setter
    def Err(self, val):
        LastError.Error = val

def GetLastError():
    return LastError.Error

def FX_CloseProcess(pid):
    if platform.system() == 'Windows':
        os.popen('taskkill /F /PID %d' % pid)
    else:
        os.kill(pid, 0)



def FX_Exit():
    pid = os.getpid()
    FX_CloseProcess(pid)


def FX_GetDefaultEmailClient():
    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, \
                              'mailto\\shell\\open\\command', \
                              0, \
                              win32con.KEY_READ)
    client_str = win32api.RegQueryValue(key, '')
    if client_str.find('OUTLOOK') != -1:
        return 'OUTLOOK'
    return 'FX_UNKNOW'

def FX_GetElementPosFormRect(x, y, width, height, elename):
    if os.path.exists(IMAGE_PROCESS) == False:
        print('Error:ImageProcess Not Found.')
        return (-1, -1)
    ## Foxit OCR
    cmd_s = IMAGE_PROCESS + ' ' + \
            ' -r ' + \
            ' -m ' + \
            ' %d*%d*%d*%d --border-x=0.17' % (x, y, width, height)
    print(cmd_s)
    buf = os.popen(cmd_s).read()
    
    buf_lines = buf.strip().split('\n')
    i = 0
    b_find = False
    click_x = -1
    click_y = -1
    for line in buf_lines:
        if Levenshtein.ratio(line, elename) > 0.8:
            b_find = True
            break
        i += 1
    if b_find:
        click_x = x + width / 2
        click_y = y + ((height / len(buf_lines)) * i) + 5
    return (click_x, click_y)

def FX_FindStringInRect(x, y, width, height, find_str, border_x=0, border_y=0):
    if os.path.exists(IMAGE_PROCESS) == False:
        print('Error:ImageProcess Not Found.')
        return
    ## Foxit OCR
    cmd_s = IMAGE_PROCESS + ' ' + \
            ' -r ' + \
            ' -m ' + \
            ' %d*%d*%d*%d --border-x=%f --border-y=%f' % (x, y, width, height, border_x, border_y)
    buf = os.popen(cmd_s).read()
    print('======================')
    print(buf)
    print('======================')
    print(Levenshtein.ratio(buf, find_str))
    
    if Levenshtein.ratio(buf, find_str) < 0.8:
        return False
    return True


def FX_ScreenCapture(x, y, width, height, output):
    if os.path.exists(IMAGE_PROCESS) == False:
        print('Error:ImageProcess Not Found.')
        return
    ## Foxit OCR
    cmd_s = IMAGE_PROCESS + ' ' + \
            ' -g ' + \
            ' -m ' + \
            ' %d*%d*%d*%d ' % (x, y, width, height) + \
            ' -o "%s"' % output
    print(cmd_s)
    buf = os.popen(cmd_s).read()
    
    print(buf)


def screenshot(x, y, width, height, output):
    if os.path.exists(IMAGE_PROCESS) == False:
        print('Error:ImageProcess Not Found.')
        return
    ## Foxit OCR
    cmd_s = IMAGE_PROCESS + ' ' + \
            ' -g ' + \
            ' -m ' + \
            ' %d*%d*%d*%d ' % (x, y, width, height) + \
            ' -o "%s"' % output
    print(cmd_s)
    buf = os.popen(cmd_s).read()

    print(buf)

def dot_product(v1, v2):
    return sum(map(lambda x: x[0] * x[1], izip(v1, v2)))

def cosine_measure(v1, v2):
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    return prod / (len1 * len2)

def equal_image(img0, img1):
    imgp = FXImage()
    return imgp.equal(img0, img1)

def StrToHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        z = '0'
        if len(hv) == 1:
            hv = '0'+hv
        if len(hv) < 4:
            for i in range(0, (3 - len(hv))):
                z = z + '0'
            hv = z + hv
        hv = '\\u' + hv
        lst.append(hv)
    return functools.reduce(lambda x,y:x+y, lst)