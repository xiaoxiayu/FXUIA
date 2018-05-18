# -*- coding: utf-8 -*-

from appium import webdriver
from appium.webdriver.webdriver import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
import time
import thread
import platform
import thread
import os

class MobileBase:
    __fx_android_define = {'Text': 'android.widget.TextView[@text="%s"]',
                           'Texts': 'android.widget.TextView',
                           'Image': 'android.widget.ImageView',
                           'EditText': 'android.widget.EditText',
                           'Button': 'android.widget.Button[@text="%s"]',
                           'Buttons': 'android.widget.Button'}

    __fx_ios_define = {'Text': 'UIAStaticText[@name="%s"]',
                       'Texts': 'UIAStaticText',
                       'Image': 'UIAImage',
                       'EditText': 'XCUIElementTypeTextField',
                       'Button': 'XCUIElementTypeButton[@name="%s"]',
                       'Buttons': 'UIAButton'}

    def __init__(self, platformName, platformVersion, deviceName, app, ios_bundleId, ios_udid, android_appPackage, android_appActivity):
        self.desired_caps = {}
        self.desired_caps['platformName'] = platformName
        self.desired_caps['platformVersion'] = platformVersion
        self.desired_caps['deviceName'] = deviceName
        self.desired_caps['noReset'] = True
        self.desired_caps["unicodeKeyboard"] = True
        self.desired_caps["resetKeyboard"] = True
        self.ui_define = None
        self.device_name = deviceName
        if platformName == 'iOS':
            self.ui_define = MobileBase.__fx_ios_define
            if ios_bundleId != '':
                self.desired_caps['bundleId'] = ios_bundleId
            else:
                self.desired_caps['app'] = app
                # desired_caps['app'] = '/Users/linfeiyun/Library/Developer/Xcode/DerivedData/samples-evbihecnyijpjnehabyijvoihzai/Build/Products/Debug-iphoneos/complete_pdf_viewer.app'
            self.desired_caps['udid'] = ios_udid
            self.desired_caps['automationName'] = 'XCUITest'
        elif platformName == 'Android':
            self.ui_define = MobileBase.__fx_android_define
            self.desired_caps['appPackage'] = android_appPackage
            ##desired_caps['appWaitActivity'] = '.MainActivity'
            if android_appActivity != '':
                self.desired_caps['appActivity'] = android_appActivity
            else:
                self.desired_caps['app'] = app
                #self.desired_caps['app'] = 'E:\\work\\foxit_mobile_pdf_sdk_android_en\\samples\\complete_pdf_viewer\\app\\build\\outputs\\apk\\app-debug.apk'
        self.platform_name = platformName
        self.platform_version = platformVersion
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

        s_s = self.get_screen_size()
        self.s_w = s_s['width']
        self.s_h = s_s['height']
        self.device_handle = DeviceBase(self.device_name, self.platform_name)
        self.device_dpi = self.device_get_dpi().strip()

    def select_texts(self, timeout=100):
        for i in range(timeout):
            try:
                return self.find_elements_by_xpath('//' + self.ui_define['Texts'])
            except Exception, e:
                print(str(e))
                time.sleep(1)

    def select_text(self, text_name, timeout=100):
        for i in range(timeout):
            try:
                return self.find_element_by_xpath('//' + self.ui_define['Text'] % text_name)
            except Exception, e:
                print(str(e))
                time.sleep(1)

    def select_images(self, timeout=100):
        for i in range(timeout):
            try:
                return self.find_elements_by_xpath('//' + self.ui_define['Image'])
            except Exception, e:
                print(str(e))
                time.sleep(1)

    def select_textview(self, timeout=10):
        for i in range(timeout):
            try:
                return WebDriverWait(self.driver, timeout).until(lambda the_driver:the_driver.find_element_by_xpath('//XCUIElementTypeTextView'))
            except:
                time.sleep(1)
        

    def select_editText(self, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(lambda the_driver: the_driver.find_element_by_xpath('//'+self.ui_define['EditText']))
        except Exception, e:
            print(str(e))
        return None

    def select_button(self, button_name, timeout=100):
        for i in range(timeout):
            try:
                if self.platform_name == 'iOS':
                    if button_name == 'OK':
                        button_name = 'common keyboard done'
                return self.find_element_by_xpath('//' + self.ui_define['Button'] % button_name)
            except Exception, e:
                print(str(e))
                time.sleep(1)

    def select_buttons(self, button_name='', timeout=100):
        for i in range(timeout):
            try:
                xpath_str = '//' + self.ui_define['Buttons']
                if button_name != '':
                    xpath_str += '[@name="%s"]' % button_name
                return self.find_elements_by_xpath(xpath_str)
            except Exception, e:
                print(str(e))
                time.sleep(1)

    def get_screen_size(self):
        screen_size = self.driver.get_window_size()
        return screen_size

    def screenshot(self, savepath):
        parsed_path = savepath.split('.')
        savepath = savepath[:-(len(parsed_path[-1]) + 1)]
        savepath = savepath + '_' + self.device_name + '_' + str(self.s_w) + 'x' + str(self.s_h) + 'x' + self.device_dpi + '.' + parsed_path[-1]
        savepath = savepath.replace(':', '-')
        print(savepath)
        self.driver.save_screenshot(savepath)
        return savepath

    def find_elements_by_xpath(self, xpath_s, timeout=15):
        try:
            return MobileElements(WebDriverWait(self.driver, timeout).until(lambda the_driver:the_driver.find_elements_by_xpath(xpath_s)))
        except:
            return None

    def find_element_by_xpath(self, xpath_s, timeout=15):
        try:
            return MobileElement(WebDriverWait(self.driver, timeout).until(lambda the_driver:the_driver.find_element_by_xpath(xpath_s)))
        except:
            return None

    def find_element_by_accessibility_id(self, acc_id, timeout=15):
        try:
            return MobileElement(WebDriverWait(self.driver, timeout).until(lambda the_driver:the_driver.find_element_by_accessibility_id(acc_id)))
        except:
            return None

    def wait_activity(self, activity_name):
        if self.platform_name == 'Android':
            self.driver.wait_activity(activity_name, 30, 2)

    def get_current_activity(self):
        return self.driver.current_activity()

    def is_app_installed(self):
        return self.driver.is_app_installed()

    def start_activity(self, app_package, app_activity):
        if self.platform_name != 'Android':
            return
        self.driver.start_activity(app_package, app_activity)

    def tap(self, pos_list, duration=None):
        if self.platform_name == 'iOS':
            self.driver.tap(pos_list)
        else:
            self.driver.tap(pos_list, duration)

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def flick(self, start_x, start_y, end_x, end_y):
        self.driver.flick(start_x, start_y, end_x, end_y)

    def tem0(self, x):
        print(x)
        action = TouchAction(self.driver)
        action \
            .long_press(x=100, y=100, duration=1000)

    def long_press(self, start_x, start_y, duration):
        action = TouchAction(self.driver)
        action \
            .long_press(x=start_x, y=start_y, duration=duration)
        action.perform()

    def fx_long_flick(self):
        thread.start_new_thread(self.tem0, ("Thread-1",))

    def long_flick(self, start_x, start_y, end_x, end_y, duration=None):
        wait_time = 1500
        action = TouchAction(self.driver)
##        action \
##            .long_press(x=start_x, y=start_y, duration=duration)
##        action1 = TouchAction(self.driver)
##        action1.long_press(x=start_x, y=start_y).wait(wait_time).release()
##        action2 = TouchAction(self.driver)
##        action2.move_to(x=end_x, y=end_y).wait(wait_time).release()
##
##        m_action = MultiAction(self.driver)
##        m_action.add(action1, action2)
##        m_action.perform()
##        return
        action \
           .long_press(x=start_x, y=start_y, duration=duration) \
           .move_to(x=end_x, y=end_y) \
           .release()
        action.perform()

    def tem0(self, x):
        print(x)
        action = TouchAction(self.driver)
        action \
            .long_press(x=self.s_w/2, y=self.s_h/2, duration=500)
        action.perform()
        print('END0')

    def tem1(self, x):
        print(x)
        action = TouchAction(self.driver)
        els = self.find_element_by_xpath('//XCUIElementTypeImage')
        action.move_to(els.ele, x=-150, y=0)
        action.perform()
        print('END1')


    def fx_long_flick(self):
##        thread.start_new_thread(self.tem0, ("Thread-1",))
        thread.start_new_thread(self.tem1, ("Thread-2",))

    def press_keycode(self, k):
        self.driver.press_keycode(k)

    ## LANDSCAPE or PORTRAIT
    def rotate(self, orientation):
        time.sleep(5)
        self.driver.orientation = orientation

    def zoom(self, mov_x, mov_y, wait_time=1500):
##        els = self.find_elements_by_xpath('//XCUIElementTypeImage')
##        print('sssss')
##        for i in range(els.size):
##            ele = els.get(i)
##            print(i)
##            self.driver.zoom(ele.ele)
##        return
        # Zoom
        action1 = TouchAction(self.driver)
        action1.long_press(x=self.s_w / 2, y=self.s_h / 2).move_to(x=mov_x, y=mov_y).wait(wait_time).release()
        action2 = TouchAction(self.driver)
        action2.long_press(x=self.s_w / 2, y=self.s_h / 2).move_to(x=-mov_x, y=-mov_x).wait(wait_time).release()

        m_action = MultiAction(self.driver)
        m_action.add(action1, action2)
        m_action.perform()

    def element_tap(self, ele, x, y, count=1):
        action1 = TouchAction(self.driver)
        action1.tap(ele.ele, x=x, y=y, count=count)
        action1.perform()
        

    def pinch(self):
        pass
        # action1 = TouchAction(self.driver)
        # action1.long_press(x=xx, y=yy).move_to(x=300, y=300).wait(500).release()
        # action2 = TouchAction(self.driver)
        # action2.long_press(x=xx, y=yy).move_to(x=-300, y=-300).wait(500).release()
        # m_action = MultiAction(self.driver)
        # m_action.add(action1, action2)
        # m_action.perform()

    def drag_and_drop(self, ele0, ele1):
        self.driver.drag_and_drop(ele0, ele1)

    def background_app(self, seconds):
        self.driver.background_app(seconds)

    def device_file_list(self, s):
        return self.device_handle.file_list(s)

    def device_file_delete(self, s):
        return self.device_handle.file_delete(s)

    def device_folder_create(self, s):
        return self.device_handle.folder_create(s)

    def device_folder_delete(self, s):
        return self.device_handle.folder_delete(s)

    def device_get_dpi(self):
        if self.platform_name == 'iOS':
            return ''
        else:
            return self.device_handle.get_dpi()

    def device_file_push(self, local_path, device_path):
        return self.device_handle.file_push(local_path, device_path)

    def device_file_pull(self, device_path, local_path):
        return self.device_handle.file_pull(device_path, local_path)

class DeviceBase:
    def __init__(self, device_name, platform_name):
        self.device_name = device_name
        self.platform_name = platform_name

    def lock(self):
        if self.platform_name == 'Android':
            os.system('adb -s "%s" shell input keyevent 26' % self.device_name)
            os.system('adb -s "%s" shell input keyevent 26' % self.device_name)

    def unlock(self):
        if self.platform_name == 'Android':
            print('adb -s %s shell am start -n io.appium.unlock/.Unlock' % self.device_name)
            os.system('adb -s "%s" shell am start -n io.appium.unlock/.Unlock' % self.device_name)

    def file_list(self, s):
        if self.platform_name == 'Android':
            print('adb -s "%s" shell ls %s' % (self.device_name, s))
            bufs = os.popen('adb -s "%s" shell ls %s' % (self.device_name, s)).read()
            print(bufs)
            return bufs.split('\r\n')

    def file_delete(self, s):
        if self.platform_name == 'Android':
            bufs = os.popen('adb -s "%s" shell rm %s' % (self.device_name, s)).read()
            return bufs

    def folder_create(self, s):
        if self.platform_name == 'Android':
            bufs = os.popen('adb -s "%s" shell mkdir "%s"' % (self.device_name, s)).read()
            return bufs

    def folder_delete(self, s):
        if self.platform_name == 'Android':
            bufs = os.popen('adb -s "%s" shell rm -rf "%s"' % (self.device_name, s)).read()
            return bufs

    def get_dpi(self):
        if self.platform_name == 'Android':
            bufs = os.popen('adb -s "%s" shell getprop ro.sf.lcd_density' % (self.device_name)).read()
            return bufs

    def file_push(self, local_path, device_path):
        if self.platform_name == 'Android':
            bufs = os.popen('adb -s "%s" push "%s" "%s"' % (self.device_name, local_path, device_path)).read()
            return bufs

    def file_pull(self, device_path, local_path):
        if self.platform_name == 'Android':
            bufs = os.popen('adb -s "%s" pull "%s" "%s"' % (self.device_name, device_path, local_path)).read()
            return bufs



class MobileElement():
    def __init__(self, ele=None):
        self.ele = ele

    def get_name(self):
        return self.ele.get_attribute('name')

    def get_className(self):
        pass

    def get_text(self):
        pass

    def get_resourceId(self):
        pass

    def is_selected(self):
        pass

    def is_enabled(self):
        return self.ele.is_enabled()

    def is_displayed(self):
        return self.ele.is_displayed()

    def send_keys(self, s):
        self.ele.send_keys(s)

    def click(self):
        self.ele.click()

    def set_value(self, val):
        self.ele.set_value(val)

    def clear(self):
        self.ele.clear()

    @property
    def size(self):
        return self.ele.size

    # @property
    # def rect(self):
    #     return self.ele.rect

    @property
    def location(self):
        return self.ele.location

    @property
    def name(self):
        return self.ele.get_attribute('name')

    @property
    def text(self):
        return self.ele.get_attribute('text')

    @property
    def clickable(self):
        return self.ele.get_attribute('clickable')

    @property
    def value(self):
        return self.ele.get_attribute('value')

    @property
    def ele(self):
        return self.ele

class MobileElements(MobileElement):
    def __init__(self, eles):
        self.eles = eles

    def get(self, i):
        return MobileElement(self.eles[i])

    @property
    def size(self):
        return len(self.eles)
