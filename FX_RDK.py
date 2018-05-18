
from mobile.base import *
from FX_Image import *


def _check_displayed(mb, xpath_str, timeout=10):
    for i in range(timeout):
        try:
            eles = mb.find_elements_by_xpath(xpath_str)
            for i in range(eles.size):
                ele = eles.get(i)
                if ele.is_displayed() == False:
                    print('No Displayed')
                    return False
                # print('Displayed:', ele.location)
            time.sleep(1)
            return True
        except:
            print('Check Error')
            time.sleep(1)

class RDKMobile(MobileBase):
    __fx_pageinfo_xpath = '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]'
    __fx_bottombar_xpath = '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.LinearLayout/android.widget.RelativeLayout'

    def __init__(self, platformName, platformVersion, deviceName, app='',
                 ios_bundleId='', ios_udid='',
                 android_appPackage='com.foxit.home', android_appActivity='.MainActivity', foxitDocument=''):
        MobileBase.__init__(self, platformName, platformVersion, deviceName, app, ios_bundleId, ios_udid,
                            android_appPackage, android_appActivity)
        self.comment_eles = None
        self.foxit_document = foxitDocument

        if platformName == 'iOS':
            fp = open('devices.cfg', 'r')
            cfgs = fp.read()
            js_cfg = json.loads(cfgs)
            for device_cfg in js_cfg['iOS']:
                if device_cfg['deviceName'] == deviceName:
                    self.s_w = device_cfg['screen']['width']
                    self.s_h = device_cfg['screen']['height']

    def open_file(self, filename, timeout=100):
        # self.copy_file_from
        self.device_file_push('testfiles/' + filename, self.foxit_document + '/testfile/' + filename)
        self.wait_activity('.MainActivity')
        for i in range(timeout):
            try:
                if self.platform_name == 'Android':
                    el = self.select_text('testfile')
                    el.click()
                el = self.select_text(filename)
                el.click()
                if self.platform_name == 'Android':
                    while not _check_displayed(self, RDKMobile.__fx_bottombar_xpath+'//android.widget.TextView'):
                        time.sleep(1)
                return True
            except Exception, e:
                print(str(e))
                time.sleep(1)
        return False

    def open_from_sdcard(self, filename):
        if self.platform_name == 'iOS':
            return
        ele = self.find_element_by_xpath('//android.widget.TextView[@text="sdcard"]')
        ele.click()

        file_ele = self.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % filename)
        while file_ele == None:
            file_ele = self.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % filename)
            if file_ele == None:
                self.flick(self.s_w / 2, self.s_h / 2, 0, -self.s_h / 3)
                continue
            file_ele.click()

    def close_file(self, mode="Discard all changes"):
        if self.platform_name == 'iOS':
            ele = self.find_element_by_accessibility_id('common back black')
            ele.click()

            ele_save = self.find_element_by_accessibility_id('Save')
            if None != ele_save:
                if mode == "Discard all changes":
                    ele = self.find_element_by_accessibility_id('Discard Changes')
                    ele.click()
                else:
                    ele_save.click()                   
        else:
            _comment_check_displayed(self, RDKMobile.__fx_bottombar_xpath + '//android.widget.ImageView')

            topbar = self.topbar_tool()
            topbar.topbar_select('close')
            if self.platform_name == 'iOS':
                return
            ele = self.find_element_by_xpath('//android.widget.ListView/android.widget.TextView[@text="Discard all changes"]')
            if ele != None:
                ele = self.find_element_by_xpath('//android.widget.ListView/android.widget.TextView[@text="%s"]' % mode)
                ele.click()
            ele = self.select_text('FoxitSDK')
            ele.click()
    def choose_directory(self,directory):
        ele = self.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % directory)
        ele.click()
   
    def open_from_download(self, filename):
        if self.platform_name == 'iOS':
            return
        else:
            ele = self.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % filename)
            ele.click()

    def browser_open_url(self,url):
        if self.platform_name == 'iOS':
            return
        else:
            ele = self.find_element_by_xpath('//android.widget.EditText')
            time.sleep(10)
            ele.send_keys(url)
            time.sleep(3)
            self.press_keycode(66)   
            
            
    def change_language(self,language):
        if self.platform_name == 'iOS':
            return
        else: 
            ele = self.find_element_by_xpath('//android.widget.ScrollView//android.widget.LinearLayout[3]//android.widget.FrameLayout[4]//android.widget.TextView')
            ele.click()  
            time.sleep(1)
            ele = self.find_element_by_xpath('//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView[2]')
            ele.click()               
            ele = self.find_element_by_xpath('//android.widget.ListView//android.widget.TextView[@text="%s"]' % language)
            ele.click() 
            time.sleep(1)
            #ele = self.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
            #ele.click()             
                    
    def save_to_sdcard(self, name):
        if self.platform_name == 'iOS':
            return
        self.close_file('Save to a new file')
        ok_ele = self.select_button('OK')
        ok_ele.click()

        edit_ele = self.select_editText()
        self.press_keycode(67)
        edit_ele.send_keys(name)
        ok_ele = self.select_button('OK')
        ok_ele.click()

        ele = self.find_element_by_xpath('//android.widget.TextView[@text="The file already exists, do you want to replace it?"]')
        if ele != None:
            ok_ele = self.select_button('OK')
            ok_ele.click()

    def save(self):
        self.close_file('Save to a new file')
        ele = self.find_element_by_accessibility_id('Save')
        ele.click()

    def _page_get_info(self):
        if self.platform_name == 'Android':
            try:
                els = self.find_elements_by_xpath(
                    RDKMobile.__fx_pageinfo_xpath + '//android.widget.TextView')
                return (int(els.get(0).name), int(els.get(1).name[1:]))
            except:
                return None
        else:
            try:
                ele = self.find_element_by_xpath('//XCUIElementTypeStaticText[contains(@name, "/")]')
                infos = ele.name.split('/')
                return (int(infos[0]), int(infos[1]))
            except:
                return None

    def page_info(self, timeout=10):
        for i in range(timeout):
            info = self._page_get_info()
            if info != None:
                return info
            time.sleep(1)
            print(info)

            if self.platform_name == 'Android':
                self.tap([(5, self.s_h / 2)])
            else:
                self.tap([(self.s_w/2, self.s_h / 2)])
                print(self.s_w/2, self.s_h / 2)
        return None

    def page_to(self, index):
        while 1:
            page_info = self.page_info()
            print('PageInfo:', page_info)
            if page_info == None:
                self.flick(self.s_w - 20, self.s_h / 2, -(self.s_w - 10), 0)
            elif index == int(page_info[0]):
                print('page ok:', index)
                return True
            else:
                if index > page_info[1] or index < 0:
                    return False
                if index < int(page_info[0]):
                    self.flick(10, self.s_h / 3, self.s_w*0.9, 0)
                    print('page prev')
                if index > int(page_info[0]):
                    self.flick(self.s_w - 20, self.s_h / 2, -(self.s_w - 10), 0)
                    print('page next')
                # time.sleep(2)

    def bottom_bar(self, tool_name):
        # for i in range(100):
        #     try:
        if self.platform_name == 'Android':
            # ele = self.find_element_by_xpath(RDKMobile.__fx_bottombar_xpath+'/android.widget.LinearLayout')
            # if ele == None:
            #     self.tap([(5, self.s_h / 2)])
            while not _comment_check_displayed(self, RDKMobile.__fx_bottombar_xpath+'//android.widget.TextView'):
                time.sleep(1)
            # _check_displayed(self, RDKMobile.__fx_bottombar_xpath + '//android.widget.ImageView')
            # els = self.select_text(tool_name)
            ele = self.find_element_by_xpath(RDKMobile.__fx_bottombar_xpath+'/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]' % tool_name)
            ele.click()
        elif self.platform_name == 'iOS':
            for i in range(10):
                ele = self.find_element_by_accessibility_id(tool_name)
##                ele = self.select_button(tool_name)
##                ele = self.find_element_by_xpath('//XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeButton[@name="%s"]' % tool_name)
                if ele == None:
                    time.sleep(1)
                else:
                    print('Click')
                    ele.click()
                    break
        if tool_name == 'Comment':
            mb_comment = RDKMobileComment(self)
            if self.platform_name == 'Android':
                time.sleep(2)
                pass
                #mb_comment.parse('//android.widget.RelativeLayout')
            elif self.platform_name == 'iOS':
                time.sleep(3)
            return mb_comment
        elif tool_name == 'List':
            mb_list = RDKMobileList(self)
            if self.platform_name == 'Android':
                time.sleep(1)
                # mb_list.parse('//android.widget.RelativeLayout')
            else:
                time.sleep(3)
            return mb_list
        elif tool_name == 'View':
            mb_view = RDKMobileView(self)
            return mb_view
            # except Exception, e:
            #     print(str(e))
            #     time.sleep(1)

    def topbar_tool(self):
        mb_topbar = RDKMobileTopBar(self)
        if self.platform_name == 'Android':
            # while 4 != mb_topbar.parse():
            #     time.sleep(1)
            #     continue
            return mb_topbar
        else:
            time.sleep(3)
            return mb_topbar

    def click_ok(self, timeout=3):
        for i in range(timeout):
            try:
                if self.platform_name == 'Android':
                    ele_ok = self.select_button('OK')
                else:
                    ele_ok = self.find_element_by_accessibility_id('Yes')
                if not ele_ok.is_enabled():
                    return False
                ele_ok.click()
                return True
            except:
                time.sleep(1)

    def click_cancel(self, timeout=3):
        for i in range(timeout):
            try:
                if self.platform_name == 'Android':
                    ele = self.select_button('Cancel')
                else:
                    ele = self.find_element_by_accessibility_id('No')
                if not ele.is_enabled():
                    return False
                ele.click()
                return True
            except:
                time.sleep(1)

    def edittext_input(self, text, auto_clear=False):
        edit_ele = self.select_editText()
        if auto_clear == True:
            if self.platform_name == 'Android':
                self.press_keycode(67)
            else:
                ele_clear = self.find_element_by_accessibility_id('Clear text')
                ele_clear.click()
        edit_ele.send_keys(text)
        if self.platform_name == 'Android':
            return self.click_ok()
        else:
            ele_done = self.find_element_by_accessibility_id('Done')
            ele_done.click()
            ele = self.find_element_by_accessibility_id('Please input a new file name')
            if ele == None:
                return False
            return True

    def textview_input(self, text, auto_clear=False):
        if auto_clear:
            ele_clear = self.find_element_by_accessibility_id('Clear text')
            ele_clear.click()
        edit_ele = self.select_textview()
        edit_ele.send_keys(text)
        ele_done = self.find_element_by_accessibility_id('common keyboard done')
        ele_done.click()

    def view_zoom(self, x, y):
        if self.platform_name == 'Android':
            time.sleep(3)
            self.tap([(x, y)])
            self.tap([(x, y)])
        else:
            ele = self.find_element_by_xpath('//XCUIElementTypeImage')
            self.element_tap(ele, x, y, 2)

    def screen_check(self, testsuit, imgname, exclude=None, debug=False, duration=3, expect_img=None):
        time.sleep(duration)
        screen_img = self.screen_save(testsuit, imgname)
        if debug:
            return True
        if expect_img == None:
            expect_img = screen_img.replace('img/running', 'img/expect')
        else:
            parsed_path = expect_img.split('.')
            expect_img = expect_img[:-(len(parsed_path[-1]) + 1)]
            expect_img = expect_img + '_' + self.device_name + '_' + str(self.s_w) + 'x' + str(self.s_h) + '.' + \
                       parsed_path[-1]
            expect_img = 'img/expect/' + testsuit + '/' + expect_img
        if self.platform_name == 'iOS':
            fximg_ios = FXImage()
            fximg_ios.open(screen_img)
            fximg_ios.draw_rectangle((0, 0), \
                                     (self.s_w, self.s_h / 19), \
                                     fill=(255, 255, 255))
            fximg_ios.save(screen_img)
            
        print('ScreenShot: %s' % screen_img)
        fximg0 = FXImage()
        fximg1 = FXImage()
        fximg0.open(screen_img)
        fximg1.open(expect_img)
        if exclude != None:
            overwrite_size = 30 * (self.s_w / 480)
            fximg0.draw_rectangle((exclude[0][0] - overwrite_size, exclude[0][1] - overwrite_size), \
                                  (exclude[0][0] + exclude[1][0] + overwrite_size,
                                   exclude[0][1] + exclude[1][1] + overwrite_size),
                                  fill=(255, 255, 255))
            fximg1.draw_rectangle((exclude[0][0] - overwrite_size, exclude[0][1] - overwrite_size), \
                                  (exclude[0][0] + exclude[1][0] + overwrite_size,
                                   exclude[0][1] + exclude[1][1] + overwrite_size),
                                  fill=(255, 255, 255))
            fximg1.save(screen_img + '_overwrite.png')
            fximg0.save(expect_img + '_overwrite.png')
        return fximg1.equal(fximg0.image, fximg1.image)

    def screen_save(self, testsuit, imgname):
        return self.screenshot('img/running/%s/%s' % (testsuit, imgname))
    
    def tap_move(self,android_startx=0,android_starty=0,android_endx=0,android_endy=0,ios_startx=0,ios_starty=0,ios_endx=0,ios_endy=0,duration=500):   
        if self.platform_name == 'iOS':
            action = TouchAction(self.driver)
            action.long_press(None,ios_startx,ios_starty,None) 
            action.perform()
            self.flick(ios_startx,ios_starty,ios_endx,ios_endy)
            self.tap([(1,1)])
        else:
            self.tap([(android_startx,android_starty)],duration)
            self.swipe(android_startx,android_starty,android_endx,android_endy, 1000) 
            self.tap([(1,1)])
            
    def long_press_move(self,android_startx=0,android_starty=0,android_endx=0,android_endy=0,ios_startx=0,ios_starty=0,ios_endx=0,ios_endy=0):   
        if self.platform_name == 'iOS':
            action = TouchAction(self.driver)
            action.long_press(None,ios_startx,ios_starty,None) 
            action.perform()
            self.flick(ios_startx,ios_starty,ios_endx,ios_endy)
            self.tap([(1,1)])
        else:
            self.tap([(android_startx,android_starty)],500)
            self.swipe(android_startx,android_starty,android_endx,android_endy, 1000) 
            self.tap([(1,1)])     
    def do_popup_page_turn(self,width,height,duration=500):
        print ('test popup page turn')
        mb = self
        winWidth = mb.get_screen_size()['width']
        winHeight = mb.get_screen_size()['height']    
        if duration != '500':
            action = TouchAction(mb.driver)
            action.long_press(None,width,height,None) 
            action.perform()  
        else:
            mb.tap([(width,height)])   
        if mb.platform_name == 'iOS':
            mb.flick(winWidth*4/5, winHeight/2,-winWidth*3/5, 0) 
        else:
            mb.swipe(winWidth*4/5, winHeight/2,winWidth/5, winHeight/2,500)   
        time.sleep(3)
        if mb.platform_name == 'iOS':
            mb.flick(winWidth/5, winHeight/2,winWidth3/5, 0) 
        else:
            mb.swipe(winWidth/5, winHeight/2,winWidth*4/5, winHeight/2,500)  
        time.sleep(5)
        mb.tap([(1,1)])  
        
    def key_input(self,key_name):
        if self.platform_name == 'iOS':
            ele = self.mb.select_key(key_name)
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True
        else:
            self.driver.keyevent(key_name)
            return True   
        
    def popup_menu_select(self,item,width,height,show_more=True,duration=500):
        mb = self
        if mb.platform_name == 'iOS':
            if duration != '500':
                action = TouchAction(mb.driver)
                action.long_press(None,width,height,None) 
                action.perform()  
            else:
                mb.tap([(width,height)])
            annot_ac = RDKMobileAnnotActionHandle(mb) 
            if show_more == True:
                annot_ac.popup_menu_select('Show more items')
            annot_ac.popup_menu_select(item) 
        else:
            print('Start Popup')
            time.sleep(3)      
            before_img_path = mb.screenshot('BeforePopup.png')
            time.sleep(5) # Wait Render.
            mb.tap([(width,height)],duration)
            print('End Popup')
            time.sleep(5)
            new_path = mb.screenshot('Popup.png')
            popup_img = Image.open(new_path)
            poper = RDKMobilePopup(mb.get_screen_size()['width'],mb.get_screen_size()['height'], mb.device_dpi)
            poper.set_popup_img(popup_img)
            img_pre = Image.open(before_img_path)
            poper.parse(img_pre)
            sel_pos = poper.select(item)
            mb.tap([sel_pos])
            time.sleep(3)       


def _comment_check_displayed(mb, xpath_str, timeout=10):
    for i in range(timeout):
        try:
            eles = mb.find_elements_by_xpath(xpath_str)
            if eles == None:
                if mb.platform_name == 'Android':
                    mb.tap([(5, mb.s_h / 2)])
                else:
                    mb.tap([(mb.s_w / 2, mb.s_h / 2)])
                time.sleep(1)
                return False
            for i in range(eles.size):
                ele = eles.get(i)
                if ele.is_displayed() == False:
                    print('No Displayed')
                    return False
                # print('Displayed:', ele.location)
            time.sleep(1)
            return True
        except:
            time.sleep(1)

class RDKMobileComment:
    __fx_comment_pos_define = {
        "common back blue":(1,0),
        "common back black":(1,1),
        "annot note": 1,
        "annot hight": 2,
        "annot strokeout": 3,
        "annot typewriter": 4,
        "annot pencil": 5,
        "common read more": 6
        }

    __fx_comment_more_pos_define = {
        "annot hight":(1,1),
        "annot underline":(1,2),
        "annot squiggly":(1,3),
        "annot strokeout":(1,4),
        "annot insert":(1,5),
        "annot replace":(1,6),
        "annot line":(2,1),
        "annot rect":(2,2),
        "annot circle":(2,3),
        "annot arrows":(2,4),
        "annot pencil":(2,5),
        "annot eraser":(2,6),
        "Typewriter":(3,1),
        "Note":(3,2),
        "Stamp":(3,3),
        "Attachment": (3, 4)
        }

    __fx_topbar_xpath = '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]'
    __fx_bottombar_xpath = '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout[2]'
    __fx_moretool_xpath = '//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout'

    # __fx_tool_bottombar_xpath = __fx_bottombar_xpath + '/android.widget.RelativeLayout/'

    def __init__(self, mb):
        self.mb = mb
        self.els_dic = None

    def tool_select(self, tool_name):
        if self.mb.platform_name == 'Android':
            while False == _comment_check_displayed(self.mb, \
                                            RDKMobileComment.__fx_bottombar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout'):
                time.sleep(1)
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_bottombar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout[%d]' % RDKMobileComment.__fx_comment_pos_define[tool_name])
            ele.click()
        else:
            if tool_name == 'annot pencil':
                tool_name = 'annot pencile'
            eles = self.mb.select_buttons(tool_name)
            for i in range(eles.size):
                print(eles.get(i).location)
                if eles.get(i).location['y'] > 0:
                    eles.get(i).click()
                    return

            
    def more_tool_select(self, tool_name):
        if self.mb.platform_name == 'Android':
            if RDKMobileComment.__fx_comment_more_pos_define[tool_name][0]!=3:
                _check_displayed(self.mb, 
                RDKMobileComment.__fx_moretool_xpath + '/android.widget.LinearLayout[%d]//android.widget.LinearLayout/android.widget.ImageView[%d]' \
                % RDKMobileComment.__fx_comment_more_pos_define[tool_name])
                ele = self.mb.find_element_by_xpath(
                    RDKMobileComment.__fx_moretool_xpath + '/android.widget.LinearLayout[%d]//android.widget.LinearLayout/android.widget.ImageView[%d]' \
                    % RDKMobileComment.__fx_comment_more_pos_define[tool_name])                  
            else:
                _check_displayed(self.mb, 
                    RDKMobileComment.__fx_moretool_xpath + '/android.widget.LinearLayout[%d]/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[%d]/android.widget.ImageView[1]' \
                    % RDKMobileComment.__fx_comment_more_pos_define[tool_name])
                ele = self.mb.find_element_by_xpath(
                    RDKMobileComment.__fx_moretool_xpath + '/android.widget.LinearLayout[%d]/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[%d]/android.widget.ImageView[1]' \
                    % RDKMobileComment.__fx_comment_more_pos_define[tool_name]) 
            ele.click()
            while False == _comment_check_displayed(self.mb, \
                                            RDKMobileComment.__fx_bottombar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout'):
                time.sleep(1)
        else:
            if tool_name == 'annot pencil':
                tool_name = 'annot pencile'
            ele = self.mb.find_element_by_xpath(
                '//XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeButton[@name="%s"]' \
                % tool_name)
            ele.click()

    def key_input(self,key_name):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.select_key(key_name)
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True
        else:
            self.mb.driver.keyevent(key_name)
            return True


    def tool_done(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.select_button('annot done')
            ele.click()
            return
        else:
            while False == _comment_check_displayed(self.mb, \
                                            RDKMobileComment.__fx_bottombar_xpath + '/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout//android.widget.ImageView'):
                time.sleep(1.5)
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_bottombar_xpath + '/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]')
            ele.click()


    def tool_back(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.select_button('common back blue')
            ele.click()
        else:
            while False == _comment_check_displayed(self.mb, \
                                                    RDKMobileComment.__fx_topbar_xpath + '//android.widget.LinearLayout'):
                time.sleep(1.5)
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_topbar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout[1]')
            ele.click()
            # self.select_by_pos((0, 0))

    def tool_undo(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.select_button('annot undo')
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True
        else:
            while False == _comment_check_displayed(self.mb, \
                                                    RDKMobileComment.__fx_bottombar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout'):
                time.sleep(1)
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_topbar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout[2]')
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True

    def tool_redo(self):
        if self.mb.platform_name == 'iOS':
##            ele = self.mb.select_button('annot redo')
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeButton[@name="annot redo"]')
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True
        else:
            while False == _comment_check_displayed(self.mb, \
                                                    RDKMobileComment.__fx_bottombar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout'):
                time.sleep(1)
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_topbar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout[3]')
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True
            # self.select_by_pos((0, 0))

    def more(self, timeout=10):
        # for i in range(timeout):
        #     try:
        if self.mb.platform_name == 'iOS':
            eles = self.mb.select_buttons('common read more')
            for i in range(eles.size):
                print(eles.get(i).location)
                if eles.get(i).location['y'] > 0:
                    eles.get(i).click()
                    return
        else:
            while False == _comment_check_displayed(self.mb, \
                                            RDKMobileComment.__fx_bottombar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout'):
                time.sleep(1)
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_bottombar_xpath + '//android.widget.LinearLayout/android.widget.LinearLayout[6]')
            ele.click()
            # except Exception as e:
            #     print(str(e))
            #     time.sleep(1)

    def tool_set(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.select_button('annotation toolitembg')
            ele.click()
            return
        else:
            while False == _check_displayed(self.mb, \
                                            RDKMobileComment.__fx_bottombar_xpath + '/android.widget.RelativeLayout/android.widget.LinearLayout//android.widget.ImageView'):
                time.sleep(1)
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_bottombar_xpath + '/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.ImageView')
            ele.click()

    def tool_keep(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.select_button('annot single')
            ele.click()
            return
        else:
            ele = self.mb.find_element_by_xpath(
                RDKMobileComment.__fx_bottombar_xpath + '/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]')
            ele.click()

    def popup_comments_is_open(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('Done')
            if ele != None:
                if ele.is_displayed():
                    return True
            return False
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView[@text="Comments"]')
            if ele != None:
                return True
            else:
                return False

    def popup_comments_delete(self):
        if self.mb.platform_name == 'iOS':
            pass
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView[@text="Delete"]')
            ele.click()

    def popup_comments_more(self, index=1):
        for i in range(10):
            try:
                if self.mb.platform_name == 'iOS':
                    els = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[%d]/XCUIElementTypeButton' % index)
                    print('button:', els.size)
                    if els.size == 4:
                        ele = els.get(1)
                    else:
                        ele = els.get(0)
                    ele.click()
                else:
                    ele = self.mb.find_element_by_xpath('//android.widget.ListView/android.widget.LinearLayout[%d]//android.widget.RelativeLayout/android.widget.ImageView' % index)
                    ele.click()
                return
            except Exception as e:
                print(str(e))
                time.sleep(1)

    def popup_comments_cancel(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('Done')
            ele.click()
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView')
            ele.click()

    def popup_comments_more_select(self, index, name):
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[%d]/XCUIElementTypeButton[@name="%s"]' % (index, name))
            ele = els.get(0)
            ele.click()
##            ele = self.mb.find_element_by_xpath('//XCUIElementTypeCell/XCUIElementTypeButton[@name="%s"]' % name)
##            ele.click()
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.ListView/android.widget.LinearLayout[%d]//android.widget.LinearLayout/android.widget.TextView[@text="%s"]' \
                                                % (index, name))
            ele.click()

    def popup_comments_get_reply_info(self):
        reply_info = []
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[3]/parent::*/XCUIElementTypeStaticText[2][contains(@name, " to ")]/parent::*/XCUIElementTypeStaticText[1]')
            if els == None:
                return None
            for i in range(els.size):
                ele = els.get(i)
                reply_info.append(ele.name)
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView')
            if els == None:
                return None
            if els.size == 1:
                return []
            for i in range(els.size):
                if i == 0:
                    continue
                ele = els.get(i)
                reply_info.append(ele.name)
        return reply_info

    def popup_comments_get_comment_info(self):
        if self.mb.platform_name == 'iOS':
            time.sleep(1)
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[3]/parent::*/XCUIElementTypeStaticText[1]')
            if ele == None:
                return ''
            return ele.name
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.ListView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView')
            return ele.name

    def popup_comments_comment_select(self, timeout=10):
        if self.mb.platform_name == 'iOS':
            for i in range(timeout):
                try:
                    ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[1]')
                    ele.click()
                    return
                except:
                    time.sleep(1)
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.ListView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView')
            ele.click()

    def popup_comments_comment_values_get(self, timeout=10):
        if self.mb.platform_name == 'iOS':
            for i in range(timeout):
                try:
                    ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[1]')
                    return ele.name
                except:
                    time.sleep(1)
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.ListView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView')
            return ele.name
    def popup_comments_text_input(self, text):
        if self.mb.platform_name == 'Android':
            ed_ele = self.mb.select_editText()
            ed_ele.send_keys(text)
            ok_ele = self.mb.select_button('OK')
            ok_ele.click()
        else:
            ed_ele = self.mb.select_textview()
            ed_ele.send_keys(text)
            ok_ele = self.mb.find_element_by_accessibility_id('OK')
            ok_ele.click()


    def popup_comments_expand(self, reply_info):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]/parent::*/XCUIElementTypeButton[@name="panel annotation open"]' % reply_info)
            ele.click()
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.ListView//android.widget.LinearLayout/android.widget.TextView[@text="%s"]/parent::*/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView' % reply_info)
            if els.size != 2:
                return False
            else:
                ele = els.get(0)
                ele.click()
            return True

    def popup_comments_collapse(self, reply_info):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]/parent::*/XCUIElementTypeButton[@name="panel annotation close"]' % reply_info)
            ele.click()
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.ListView//android.widget.LinearLayout/android.widget.TextView[@text="%s"]/parent::*/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView' % reply_info)
            if els.size != 2:
                return False
            else:
                ele = els.get(0)
                ele.click()
            return True

    def popup_comments_input(self, index, info):
        if self.mb.platform_name == 'iOS':
            ele = None
            for i in range(5):
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[%d]' % index)
                if ele != None:
                    break
            ele.send_keys(info)
            ele_done = self.mb.find_element_by_accessibility_id('common keyboard done')
            ele_done.click()
        else:
            # self.popup_comments_comment_select()
            # self.popup_comments_text_input(info)
            # self.popup_comments_comment_select()
            edit_ele = self.mb.select_editText()
            edit_ele.send_keys(info)
            self.mb.click_ok()

    def popup_type_write_input(self, info):
        if self.mb.platform_name == 'iOS':
            ele = None
            for i in range(5):
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeTextView')
                if ele != None:
                    break
            ele.send_keys(info)
            self.mb.tap([(1,1)])
            #ele_done = self.mb.find_element_by_accessibility_id('common keyboard done')
            #ele_done.click()
        else:
            edit_ele = self.mb.select_editText()
            edit_ele.send_keys(info)
            hook_ele = self.mb.find_element_by_xpath('//android.widget.TextView/../../android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout//android.widget.ImageView[2]')
            hook_ele.click()
            
    def popup_comments_get_reply_by_index(self, index):
        if self.mb.platform_name == 'iOS':
            time.sleep(1)
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[%d]/XCUIElementTypeStaticText[1]' % index)
            if ele == None:
                return ''
            return ele.name
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="Comments"]/../..//android.widget.ListView/android.widget.LinearLayout[%d]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView' % index) 
            print ele
            print ele.name
            return ele.name                   

    def popup_comments_input_clear(self, index, char_count=1):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[%d]/XCUIElementTypeTextView' % index)
            ele.clear()
        else:
            ed_ele = self.mb.select_editText()
            for i in range(char_count):
                self.mb.press_keycode(67)
            ok_ele = self.mb.select_button('OK')
            ok_ele.click()


    def popup_comments_input_all_clear(self, index=1):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell[%d]/XCUIElementTypeTextView' % index)
            ele.clear()
        else:
            ed_ele = self.mb.select_editText()
            ed_ele.clear()

    def appearance_color_palette(self):
        if self.mb.platform_name == 'iOS':
            return
        ele = self.mb.find_element_by_xpath('//android.support.v4.view.ViewPager')
        self.mb.flick(ele.location['x'] + ele.size['width'] - 5, ele.location['y'] + ele.size['height'] / 2, \
                      -ele.size['width'] / 2, 0)
        self.mb.tap([(ele.location['x'] + ele.size['width'] / 2, ele.location['y'] + ele.size['height'] / 2)])

    def appearance_font_select(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Font"]/../XCUIElementTypeButton[1]')            
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="Font Name"]/..//android.widget.LinearLayout/android.widget.TextView[1]')
        ele.click()
    
    def appearance_size_select(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Font"]/../XCUIElementTypeButton[2]')            
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="Font Name"]/../android.widget.LinearLayout/android.widget.TextView[2]')
        ele.click()
    
    def appearance_font_get(self, index=None):
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeStaticText[@name="Font"]/../XCUIElementTypeTable//XCUIElementTypeStaticText')            
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.TextView[@text="Font"]/../..//android.widget.ListView//android.widget.TextView')
        if index != None:
            ele = els.get(index)
            ele.click()
        return els.size
    
    def appearance_size_get(self, index=None):
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeStaticText[@name="Font Size"]/../XCUIElementTypeTable//XCUIElementTypeStaticText')            
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.TextView[@text="FontSize"]/../..//android.widget.ListView//android.widget.TextView')
        if index != None:
            ele = els.get(index)
            ele.click()
        return els.size
    
    def appearance_font_back(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Font"]/../XCUIElementTypeButton[@name="common back black"]')            
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="Font"]/../android.widget.ImageView')
        ele.click()  

    def appearance_size_back(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Font Size"]/../XCUIElementTypeButton[@name="common back black"]')            
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="FontSize"]/../android.widget.ImageView')
        ele.click()  
        
    def appearance_color_get(self, index=None):
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeOther/XCUIElementTypeStaticText[@name="Color"]/parent::*/XCUIElementTypeOther/XCUIElementTypeButton')            
        else:
            els = self.mb.find_elements_by_xpath(
                '//android.support.v4.view.ViewPager/android.widget.LinearLayout//android.widget.ImageView')
        if index != None:
            ele = els.get(index)
            ele.click()
        return els.size

    def appearance_linewidth_set(self, width):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeStaticText[@name="Thickness"]/parent::*/XCUIElementTypeSlider')
            ele.set_value(width)
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.SeekBar')
            self.mb.tap([(ele.location['x'] + width * ele.size['width'], ele.location['y'] + ele.size['height'] / 2)])

    def appearance_opacity_select(self, per=100):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeStaticText[@name="Opacity"]/parent::*/XCUIElementTypeOther/XCUIElementTypeButton[@name="%d %%"]' % per)
            ele.click()
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.TextView[@text="%d%%"]/parent::*' % per)
            ele.click()

    def appearance_cancel(self):
        if self.mb.platform_name == 'iOS':
            return
        else:
            self.mb.press_keycode(4)
            while not _check_displayed(self.mb,\
                                       RDKMobileComment.__fx_bottombar_xpath + '/android.widget.RelativeLayout/android.widget.LinearLayout//android.widget.ImageView'):
                self.mb.press_keycode(4)
                time.sleep(1)
                # self.mb.press_keycode(4)
    def popup_note_comments_input(self, info):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeTextView')
            ele.send_keys(info)
            ele = self.mb.select_button('Save')
            ele.click()
        else:
            ed_ele = self.mb.select_editText()
            ed_ele.send_keys(info)
            ok_ele = self.mb.select_button('OK')
            ok_ele.click()             

    def appearance_icon_select(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeButton[@name="Icon"]')            
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="Icon"]')
        ele.click()
    
    def appearance_icon_get(self, index=None):
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeButton[@name="Icon"]/../..//XCUIElementTypeStaticText')            
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.TextView[@text="Icon"]/../../..//android.widget.ListView//android.widget.TextView')
        if index != None:
            ele = els.get(index)
            ele.click()
        return els.size 
    
    def appearance_fill_select(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeButton[@name="Fill"]')            
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="Fill"]')
        ele.click()

    def appearance_stamp_get(self, index=None):
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeStaticText[@name="Stamp"]/../..//XCUIElementTypeCell/XCUIElementTypeButton')            
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.GridView//android.view.View')
        if index != None:
            ele = els.get(index)
            ele.click()
        return els.size 
    
    def appearance_stamp_type_select(self, index=None):
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeStaticText[@name="Stamp"]/../../XCUIElementTypeOther/XCUIElementTypeImage/../XCUIElementTypeButton')            
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.TextView/../../android.widget.LinearLayout[2]//android.widget.ImageView')
        if index != None:
            ele = els.get(index)
            ele.click()
        return els.size
    
    def popup_note_cancel(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeButton[@name="Cancel"]')
            ele.click()
    def popup_note_save(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeButton[@name="Save"]')
            ele.click()

    def tap_move(self,android_startx=0,android_starty=0,android_endx=0,android_endy=0,ios_startx=0,ios_starty=0,ios_endx=0,ios_endy=0,duration=500):   
        if self.mb.platform_name == 'iOS':
            action = TouchAction(mb.driver)
            action.long_press(None,ios_startx,ios_starty,None) 
            action.perform()
            self.mb.flick(ios_startx,ios_starty,ios_endx,ios_endy)
            self.mb.tap([(1,1)])
        else:
            self.mb.tap([(android_startx,android_starty)],duration)
            self.mb.swipe(android_startx,android_starty,android_endx,android_endy, 1000) 
            self.mb.tap([(1,1)])
    def long_press_move(self,android_startx=0,android_starty=0,android_endx=0,android_endy=0,ios_startx=0,ios_starty=0,ios_endx=0,ios_endy=0):   
        if self.mb.platform_name == 'iOS':
            action = TouchAction(mb.driver)
            action.long_press(None,ios_startx,ios_starty,None) 
            action.perform()
            self.mb.flick(ios_startx,ios_starty,ios_endx,ios_endy)
            self.mb.tap([(1,1)])
        else:
            self.mb.tap([(android_startx,android_starty)],500)
            self.mb.swipe(android_startx,android_starty,android_endx,android_endy, 1000) 
            self.mb.tap([(1,1)]) 
       
    def popup_menu_select(self,item,width,height,show_more=True,duration=500):
        mb = self.mb
        if mb.platform_name == 'iOS':
            if duration != '500':
                action = TouchAction(mb.driver)
                action.long_press(None,width,height,None) 
                action.perform()  
            else:
                mb.tap([(width,height)])
            annot_ac = RDKMobileAnnotActionHandle(mb) 
            if show_more == True:
                annot_ac.popup_menu_select('Show more items')
            annot_ac.popup_menu_select(item) 
        else:
            print('Start Popup')
            time.sleep(3)      
            before_img_path = mb.screenshot('BeforePopup.png')
            time.sleep(5) # Wait Render.
            mb.tap([(width,height)],duration)
            print('End Popup')
            time.sleep(5)
            new_path = self.mb.screenshot('Popup.png')
            popup_img = Image.open(new_path)
            poper = RDKMobilePopup(mb.get_screen_size()['width'],mb.get_screen_size()['height'], mb.device_dpi)
            poper.set_popup_img(popup_img)
            img_pre = Image.open(before_img_path)
            poper.parse(img_pre)
            sel_pos = poper.select(item)
            mb.tap([sel_pos])
            time.sleep(3)                    
        
    def do_popup_page_turn(self,width,height,duration=500):
        print 'test popup page turn'
        mb = self.mb
        winWidth = mb.get_screen_size()['width']
        winHeight = mb.get_screen_size()['height']    
        if duration != '500':
            action = TouchAction(mb.driver)
            action.long_press(None,width,height,None) 
            action.perform()  
        else:
            mb.tap([(width,height)])   
        if mb.platform_name == 'iOS':
            mb.flick(winWidth*4/5, winHeight/2,-winWidth*3/5, 0) 
        else:
            mb.swipe(winWidth*4/5, winHeight/2,winWidth/5, winHeight/2,500)   
        time.sleep(3)
        if mb.platform_name == 'iOS':
            mb.flick(winWidth/5, winHeight/2,winWidth3/5, 0) 
        else:
            mb.swipe(winWidth/5, winHeight/2,winWidth*4/5, winHeight/2,500)  
        time.sleep(5)
        mb.tap([(1,1)])            
##    def tool_set(self):
##        if self.mb.platform_name == 'iOS':
##            ele = self.mb.select_button('annotation toolitembg')
##            ele.click()
##            return
##        else:
##            ele = self.mb.find_element_by_xpath(
##                RDKMobileComment.__fx_bottombar_xpath + '/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout[4]')
##            ele.click()

    @property
    def current_tool_name(self):
        if self.mb.platform_name == 'iOS':
            return
        ele = self.mb.find_element_by_xpath(
            RDKMobileComment.__fx_bottombar_xpath + '/android.widget.LinearLayout/android.widget.TextView')
        try:
            return ele.name
        except:
            return None


class RDKMobileList:
    __fx_list_pos_define = {
        "Bookmarks": 1,
        "Outline": 2,
        "Annotations": 3
    }
    __fx_list_iosname_define = {
        "Outline": "panel top outline normal",
        "Bookmarks": "panel top bookmak normal",
        "Annotations": "panel top annot normal"
        }

    def __init__(self, mb):
        self.mb = mb
        self.els_dic = None

    def parse(self, xpath_s):
        screen_size = self.mb.get_screen_size()
        for i in range(100):
            try:
                line_l = []
                ele_dc = {}
                ele_dc[0] = []
                all_eles = {}

                els = self.mb.find_elements_by_xpath(xpath_s)
                print('ELESIZE:', els.size)
                for i in range(els.size):
                    try:
                        ele = els.get(i)
                        if ele.size['width'] == screen_size['width'] or \
                                        ele.size['height'] == screen_size['height'] or \
                                        ele.location['y'] < 10:
                            # print('========')
                            # print(ele.size)
                            # print(ele.location)
                            # print('========')
                            continue
                        if ele.location['y'] not in ele_dc.keys():
                            ele_dc[ele.location['y']] = []

                        if ele.name != None and ele.name.find('common back') != -1:
                            ele_dc[0].append(ele)
                        else:
                            ele_dc[ele.location['y']].append(ele)
                            # print('========')
                            # print(ele.location['y'], ele.size, ele.name)
                            # print('========')

                    except Exception, e:
                        print(str(e))
                self.els_dic = ele_dc
                return ele_dc
            except Exception, e:
                print(str(e))

    def select_by_pos(self, pos, parse=False):
        # if self.els_dic == None or parse == True:
        #     self.parse()
        print(self.els_dic)
        i = 0
        l, r = pos[0], pos[1]
        ele_keys = sorted(self.els_dic.iteritems(), key=lambda d: d[0])
        for ele_m in ele_keys:
            ele_pos = ele_m[0]
            ele_arr = ele_m[1]
            print(ele_pos)
            if l == i:
                if r == -1:
                    r = len(ele_arr) - 1
                ele = ele_arr[r]
                ele.click()
                if r != 0 and r != -1 and i != 0:
                    pass
                return
            i += 1


    def panel_select(self, module_name):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id(RDKMobileList.__fx_list_iosname_define[module_name])
            ele.click()
        else:
            _check_displayed(self.mb, '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout[2]//android.widget.ImageView')
            ele = self.mb.find_element_by_xpath(
                '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout[2]/android.widget.RelativeLayout[%d]' %
                RDKMobileList.__fx_list_pos_define[module_name])
            ele.click()
            # self.select_by_pos(RDKMobileList.__fx_list_pos_define[module_name])
            # time.sleep(3)

    def clear(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeButton[@name="Clear"]')
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.TextView[@text="Clear"]')
        ele.click()

    def panel_cancel(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('panel cancel')
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.TextView[@text="Clear"]/parent::*/android.widget.ImageView')
            if ele == None:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.TextView[@text="Outline"]/parent::*/android.widget.ImageView')
        ele.click()
        

    def outline_back(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="..."]')
        else:
            ele = self.mb.find_element_by_xpath('//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView')
        ele.click()

    def outline_get_all(self):
        all_outline_name = []
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText')
        else:
            els = self.mb.find_elements_by_xpath('//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')
        for i in range(els.size):
            ele = els.get(i)
            all_outline_name.append(ele.name)
        return all_outline_name

    def outline_select(self, name, more=False):
        if self.mb.platform_name == 'iOS':
            if more:
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]/parent::*/XCUIElementTypeButton' % name)
            else:
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]/parent::*' % name)
        else:
            if more:
                ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="%s"]/parent::*/parent::*/android.widget.LinearLayout/android.widget.ImageView' % name)
            else:
                ele = self.mb.find_element_by_xpath('//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]'%name)
        if ele == None:
            return False
        ele.click()
        return True

    def annotations_clear(self, confirm='No'):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('Clear')
            ele.click()
            ele = self.mb.find_element_by_accessibility_id(confirm)
            ele.click()
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.TextView[@text="Annotations"]/parent::*/android.widget.TextView[@text="Clear"]')
            ele.click()
            if confirm == 'Yes':
                ele_ok = self.mb.select_button('OK')
                ele_ok.click()
            else:
                ele_ok = self.mb.select_button('Cancel')
                ele_ok.click()

    def annotations_is_empty(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('Empty list')
            if ele == None:
                return False
            else:
                return True
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.TextView[@text="No Annotation List"]')
            if ele == None:
                return False
            return True

    # def annotations_get_info(self):
    #     info_dic = {}
    #     if self.mb.platform_name == 'iOS':
    #         els = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeOther/XCUIElementTypeStaticText')
    #     else:
    #         els = self.mb.find_elements_by_xpath('//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "Page ")]/parent::*/child::*')
    #     if els == None:
    #         return None
    #     page_info = ''
    #     for i in range(els.size):
    #         ele = els.get(i)
    #         if i == 0:
    #             page_info = ele.name
    #             continue
    #         if i % 2 != 0:
    #             info_dic[page_info] = ele.name
    #         else:
    #             page_info = ele.name
    #     return info_dic

    def annotations_get_suminfo(self):
        info_dic = {}
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath(
                '//XCUIElementTypeTable/XCUIElementTypeOther/XCUIElementTypeStaticText')
        else:
            for i in range(10):
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.TextView[@text="Annotations"]/parent::*/android.widget.TextView[@text="Clear"]')
                if ele.is_enabled():
                    break
                else:
                    time.sleep(1)
            els = self.mb.find_elements_by_xpath(
                '//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "Page ")]/parent::*/child::*')
        if els == None:
            return None
        page_info = ''
        for i in range(els.size):
            ele = els.get(i)
            if i == 0:
                page_info = ele.name
                continue
            if i % 2 != 0:
                info_dic[page_info] = ele.name
            else:
                page_info = ele.name
        return info_dic

    def annotations_get_info(self):
        infos = []
        if self.mb.platform_name == 'iOS':
            els = self.mb.find_elements_by_xpath(
                '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[2]/preceding-sibling::*')
            if els == None:
                return None
        else:
            for i in range(10):
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.TextView[@text="Annotations"]/parent::*/android.widget.TextView[@text="Clear"]')
                if ele.is_enabled():
                    break
                else:
                    time.sleep(1)
            els = self.mb.find_elements_by_xpath(
                '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView')
        if els == None:
            return None
        for i in range(els.size):
            ele = els.get(i)
            infos.append(ele.name)
        return infos

    def annotations_get_reply_info(self):
        infos = []
        if self.mb.platform_name == 'iOS':
            pass
        else:
            els = self.mb.find_elements_by_xpath(
                '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView')
        for i in range(els.size):
            ele = els.get(i)
            infos.append(ele.name)
        return infos

    def annotations_select_comment(self, text, fuzzy=True):
        if self.mb.platform_name == 'iOS':
            if fuzzy:
                ele = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@name, "%s")]' % text)
            else:
                ele = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]' % text)
        else:
            if fuzzy:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "%s")]' \
                    % text)
            else:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]' \
                    % text)
        ele.click()

    def annotations_select(self, text, more=False, fuzzy=True):
        if self.mb.platform_name == 'iOS':
            if fuzzy:
                if more:
                    ele = self.mb.find_element_by_xpath(
                        '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@name, "%s")]/parent::*/XCUIElementTypeButton[@name="document cellmore more"]' \
                        % text)
                else:
                    ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@name, "%s")]/parent::*' % text)
            else:
                if more:
                    ele = self.mb.find_element_by_xpath(
                        '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]/parent::*/XCUIElementTypeButton[@name="document cellmore more"]' \
                        % text)
                else:
                    ele = self.mb.find_element_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]/parent::*' % text)

        else:
            if fuzzy:
                if more:
                    ele = self.mb.find_element_by_xpath(
                        '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "%s")]/parent::*/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView' \
                        % text)
                else:
                    ele = self.mb.find_element_by_xpath(
                        '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "%s")]/parent::*/android.widget.RelativeLayout' \
                        % text)
            else:
                if more:
                    ele = self.mb.find_element_by_xpath(
                        '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]/parent::*/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView' \
                        % text)
                else:
                    ele = self.mb.find_element_by_xpath(
                        '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]/parent::*/android.widget.RelativeLayout' \
                        % text)
        ele.click()

    def annotations_select_by_index(self, index, more=False):
        if self.mb.platform_name == 'iOS':
            if more:
                ele = self.mb.find_element_by_xpath(
                    '//XCUIElementTypeTable/XCUIElementTypeCell[%d]/XCUIElementTypeStaticText/parent::*/XCUIElementTypeButton[@name="document cellmore more"]' \
                    % index)
            else:
                ele = self.mb.find_element_by_xpath(
                    '//XCUIElementTypeTable/XCUIElementTypeCell[%d]/XCUIElementTypeStaticText/parent::*' % index)

        else:
            if more:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.ListView/android.widget.LinearLayout[%d]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView/parent::*/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView' \
                    % index)
            else:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.ListView/android.widget.LinearLayout[%d]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView/parent::*/android.widget.RelativeLayout' \
                    % index)
        ele.click()
        time.sleep(3)

    ## s can be 'Reply', 'Comment'/'Note', 'Delete'
    def annotations_select_more(self, s):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath(
                        '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeButton[@name="%s"]' \
                        % s)
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]')
        ele.click()

    def bookmarks_is_empty(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('Empty list')
            if ele == None:
                return False
            else:
                return True
        else:
            ele =  self.mb.find_element_by_xpath('//android.widget.TextView[@text="No Reading Bookmarks Information"]')
            if ele == None:
                return False
            else:
                return True

    def bookmarks_select(self, text, more=False):
        if self.mb.platform_name == 'iOS':
            if more:
                ele = self.mb.find_element_by_xpath(
                            '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]/parent::*/XCUIElementTypeButton[@name="document cellmore more"]' \
                            % text)
            else:
                ele = self.mb.find_element_by_xpath(
                            '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]' \
                            % text)
        else:
            if more:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.ListView/android.widget.FrameLayout//android.widget.TextView[@text="%s"]/parent::*/parent::*/android.widget.ImageView' % text)
            else:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.ListView/android.widget.FrameLayout/android.widget.RelativeLayout//android.widget.TextView[@text="%s"]' \
                    % text)
        ele.click()

    ## s can be 'Rename', 'Delete'
    def bookmarks_more_select(self, s):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath(
                            '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeButton[@name="%s"]' \
                            % s)
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]'%s)
        ele.click()

    def bookmarks_rename_input(self, text, auto_clear=True):
        if self.mb.platform_name == 'iOS':
            return self.mb.textview_input(text, auto_clear)
        else:
            return self.mb.edittext_input(text, auto_clear)

    def bookmarks_get_all(self):
        bookmarks = []
        if self.mb.platform_name == 'iOS':
            eles = self.mb.find_elements_by_xpath(
                '//XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeButton[@name="document cellmore more"]/preceding-sibling::*')
        else:
            eles = self.mb.find_elements_by_xpath(
                '//android.widget.ListView/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')
        for i in range(eles.size):
            ele = eles.get(i)
            bookmarks.append(ele.name)
        return bookmarks


class RDKMobileView:
    __fx_bottombar_xpath = '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]'

    def __init__(self, mb):
        self.mb = mb
        self.els_dic = None

    ## name can be 'Single', 'Continuous', 'Thumbnail'
    def page_mode(self, mode, auto_close=False):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath(
                '//XCUIElementTypeOther/XCUIElementTypeButton[@name="%s"]' \
                % mode)
            ele.click()
        else:
            while _comment_check_displayed(self.mb, \
                                       RDKMobileView.__fx_bottombar_xpath + '/android.widget.LinearLayout//android.widget.ImageView'):
                time.sleep(1)

            ele = self.mb.find_element_by_xpath(
                '//android.view.View/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]' \
                % mode)
            ele.click()
            if auto_close == True:
                self.mb.press_keycode(4)

    def view_cancel(self):
        if self.mb.platform_name == 'iOS':
            return
        else:
            self.mb.press_keycode(4)
            while not _check_displayed(self.mb, \
                                       RDKMobileView.__fx_bottombar_xpath + '/android.widget.LinearLayout//android.widget.ImageView'):
                self.mb.press_keycode(4)
                time.sleep(1)
                # self.mb.press_keycode(4)

    def thumbnail_edit_cancel(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('Done')
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView')
        ele.click()

    def thumbnail_cancel(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('property back')
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView')
        ele.click()

    def thumbnail_select(self, page_num):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath(
                '//XCUIElementTypeOther/XCUIElementTypeStaticText[@name="%d"]' \
                % page_num)
        else:
            ## something strange
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="Edit"]',\
                timeout=3)
            # if ele != None:
            #     page_num = page_num
            # else:
            #     page_num = page_num
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%d"]' \
                % page_num)
        ele.click()

    def thumbnail_get_show_pages(self):
        pages = []
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath(
                '//XCUIElementTypeOther/XCUIElementTypeStaticText')
        else:
            ## something strange
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="Edit"]',\
                timeout=3)
            # if ele != None:
            #     page_num = page_num
            # else:
            #     page_num = page_num
            els = self.mb.find_elements_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView')
            for i in range(els.size):
                ele = els.get(i)
                pages.append(int(ele.name))
        return pages

    ## action can be 'all', 'delete', 'rotate', 'extract', 'add', 'edit'
    def thumbnail_edit(self, action='edit'):
        ele = None
        if self.mb.platform_name == 'iOS':
            if action == 'edit':
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeButton[@name="Edit"]')
            else:
                if action == 'all':
                    ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeButton[@name="thumb select all"]')
                if action == 'delete':
                    ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeButton[@name="thumb delete"]')
        else:
            if action == 'edit':
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="Edit"]')
            else:
                els = self.mb.find_elements_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView')
                for i in range(els.size):
                    ele = els.get(i)
                    if action == 'extract' and i == 1:
                        break
                    if action == 'rotate' and i == 2:
                        break
                    if action == 'delete' and i == 3:
                        break
                    if action == 'add' and i == 4:
                        break
                    if action == 'all' and i == 5:
                        break
        if ele == None:
            return None
        if False == ele.is_enabled():
            return False
        ele.click()
        return True

    def thumbnail_edit_swape(self, page0, page1):
        if self.mb.platform_name == 'iOS':
            pass
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="Edit"]', \
                timeout=3)
            # if ele != None:
            #     page_num = page_num
            # else:
            #     page_num = page_num

            if page0 > page1:
                ele0 = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%d"]' \
                    % page0).ele
                ele1 = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%d"]/parent::*/preceding-sibling::*[2]' \
                    % page1).ele
                self.mb.drag_and_drop(ele0, ele1)
            else:
                ele0 = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%d"]/parent::*/preceding-sibling::*[2]' \
                    % page0).ele
                ele1 = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[@text="%d"]' \
                    % page1).ele
                self.mb.long_flick(ele0.location['x'], ele0.location['y'], ele1.location['x'] - ele0.location['x'],
                                   ele1.location['y'] - ele0.location['y'], duration=1000)

            # self.mb.drag_and_drop(ele0, ele1)

    def thumbnail_is_delete_allowed(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_accessibility_id('Deleting all page(s) is not allowed')
            if ele == None:
                return True
            ele = self.mb.find_element_by_accessibility_id('OK')
            ele.click()
            return False
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.TextView[@text="Deleting all page(s) is not allowed."]')
            if ele == None:
                return True
            ele = self.mb.select_button('OK')
            ele.click()
            return False


    def thumbnail_get_info(self):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeButton[@name="thumb select all"]/parent::*/following-sibling::*[1]/XCUIElementTypeButton')
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')
        return ele.name

    def auto_brightness(self, enable=True):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath(
                '//XCUIElementTypeSwitch')
            if ele.value == 0:
                if enable == False:
                    return False
                else:
                    ele.click()
                    return True
            else:
                if enable == True:
                    return False
                else:
                    ele.click()
                    return True
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.SeekBar')
            b_enable = ele.is_enabled()
            if b_enable != enable:
                return False
            else:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.LinearLayout/android.widget.TextView[@text="Auto-Brightness"]/parent::*/android.widget.ImageView')
                ele.click()
                return True

    def change_brightness(self, value):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeSlider')
            ele.set_value(value)
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.SeekBar')
            ele.set_value(value)

    def night_mode(self, enable=None):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeButton[@name="readview night normal"]')
            print('night:',ele.value)
            if enable == None:
                if ele.value == 'true':
                    if enable == True:
                        return False
                    else:
                        ele.click()
                        return True
                else:
                    if enable == False:
                        return False
                    else:
                        ele.click()
                        return True
            else:
                ele.click()
                if ele.value == 'true':
                    return False
                else:
                    return True
        else:
            els = self.mb.find_elements_by_xpath(
                '//android.widget.SeekBar/parent::*/parent::*/following-sibling::*/android.widget.ImageView')
            for i in range(els.size):
                ele = els.get(i)
                if i == 1:
                    ele.click()
                    return
                    # print('clickable:', ele.clickable)
                    # if ele.clickable == 'true':
                    #     if enable != True:
                    #         return False
                    #     else:
                    #         ele.click()
                    #         return True
                    # else:
                    #     if enable != False:
                    #         return False
                    #     else:
                    #         ele.click()
                    #         return True

        # ele.click()

    ## mode can be 'Portrait', 'Landscape', 'Auto-rotate with screen'
    def screen_lock(self, mode=None):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeScrollView/XCUIElementTypeButton[@name="Screen Lock"]')
            if ele.value == 'true':
                if mode == True:
                    return False
                else:
                    ele.click()
                    return True
            else:
                if mode == False:
                    return False
                else:
                    ele.click()
                    return True
        else:
            ele = self.mb.find_element_by_xpath(
                '//android.widget.LinearLayout/android.widget.TextView[@text="Screen Lock"]/parent::*')
            ele.click()
            if mode != None:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.TextView[@text="%s"]' % mode)
                ele.click()

    def reflow(self, mode=None):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeScrollView/XCUIElementTypeButton[@name="Reflow"]')
            if ele.value == 'true':
                if mode == True:
                    return False
                else:
                    ele.click()
                    return True
            else:
                if mode == False:
                    return False
                else:
                    ele.click()
                    return True


class RDKMobileTopBar:
    __fx_topbar_pos_define = {
        "close": (1, 0),
        "bookmark": (1, 1),
        "search": (1, 2),
        "more": (1, 3)
    }

    __fx_search_pos_define = {
        "cancel": (1, 0),
        "bookmark": (1, 1),
        "search": (1, 2),
        "more": (1, 3)
    }
    __fx_ios_topbar_pos_define = {
        "close":"common back black",
        "bookmark":"readview bookmark",
        "search":"search",
        "more":"common read more",
        "cancel":"Cancel"
        }

    __fx_android_more_define = {
        'File information': 'Properties',
        'Reset Form Fields': 'Reset Form Fields',
        'Import Form Data': 'Import Form Data',
        'Export Form Data': 'Export Form Data',
        'OOM_TEST':'Test_OOM'
        }

    __fx_topbar_xpath = '//android.widget.FrameLayout/android.widget.RelativeLayout'+\
                        '/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout'

    def __init__(self, mb):
        self.mb = mb
        self.els_dic = None
        self.search_ok_button = None
        self.search_cancel_button = None
        self.search_result = None

    def parse(self, xpath_s='//android.widget.LinearLayout/android.widget.ImageView'):
        if self.mb.platform_name == 'Android':
            screen_size = self.mb.get_screen_size()
            for i in range(100):
                try:
                    line_l = []
                    ele_dc = {}
                    ele_dc[0] = []
                    all_eles = {}

                    els = self.mb.find_elements_by_xpath(xpath_s)
                    print('ELESIZE:', els.size)
                    for i in range(els.size):
                        try:
                            ele = els.get(i)
                            if ele.size['width'] == screen_size['width'] or \
                                            ele.size['height'] == screen_size['height'] or \
                                    (ele.location['y'] < 10 and ele.location['x'] < 10):
                                # print(ele.location)
                                continue
                            l_y = ele.location['y']
                            if l_y < 10:
                                l_y = 0
                            if l_y not in ele_dc.keys():
                                ele_dc[l_y] = []

                            if ele.name != None and ele.name.find('common back') != -1:
                                ele_dc[0].append(ele)
                            else:
                                ele_dc[l_y].append(ele)
                                print(ele.location, ele.size)

                        except Exception, e:
                            print(str(e))
                    self.els_dic = ele_dc
                    return els.size
                except Exception, e:
                    print(str(e))

    def select_by_pos(self, pos, parse=False):
        if self.mb.platform_name != 'Android':
            return
        i = 0
        l, r = pos[0], pos[1]
        ele_keys = sorted(self.els_dic.iteritems(), key=lambda d: d[0])
        for ele_m in ele_keys:
            ele_pos = ele_m[0]
            ele_arr = ele_m[1]
            if l == i:
                if r == -1:
                    r = len(ele_arr) - 1
                ele = ele_arr[r]
                ele.click()
                if r != 0 and r != -1 and i != 0:
                    pass
                return
            i += 1

    ## cancel, bookmark, search, more
    def topbar_select(self, name):
        if self.mb.platform_name == 'Android':
            _comment_check_displayed(self.mb, RDKMobileTopBar.__fx_topbar_xpath)
            if name == 'cancel' or name == 'close':
                ele = self.mb.find_element_by_xpath(RDKMobileTopBar.__fx_topbar_xpath+'/android.widget.LinearLayout[1]//android.widget.ImageView')
            elif name == 'bookmark':
                ele = self.mb.find_element_by_xpath(
                    RDKMobileTopBar.__fx_topbar_xpath + '/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.widget.ImageView')
            elif name == 'search':
                ele = self.mb.find_element_by_xpath(
                    RDKMobileTopBar.__fx_topbar_xpath + '/android.widget.LinearLayout[2]/android.widget.LinearLayout[2]/android.widget.ImageView')
            elif name == 'more':
                ele = self.mb.find_element_by_xpath(
                    RDKMobileTopBar.__fx_topbar_xpath + '/android.widget.LinearLayout[2]/android.widget.LinearLayout[3]/android.widget.ImageView')
            # self.select_by_pos(RDKMobileTopBar.__fx_topbar_pos_define[name])
            ele.click()
        else:
            ele = self.mb.find_element_by_accessibility_id(RDKMobileTopBar.__fx_ios_topbar_pos_define[name])
            while False != ele.is_displayed():
                time.sleep(1)
                ele.click()

    def search(self, fstr, run=True):
        if self.mb.platform_name == 'Android':
            ele = self.mb.select_editText()
            if ele == None:
                return False
            ele.send_keys(fstr)
            if run:
                self.mb.press_keycode(66)
            return True
        else:
            try:
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeSearchField')
                if run:
                    fstr = fstr + '\n'
                ele.send_keys(fstr)
                return True
            except:
                return False

    def search_get_input_rect(self):
        if self.mb.platform_name == 'Android':
            return None
        else:
            ele = self.mb.find_element_by_accessibility_id('Whitespace ignored!')
            return (ele.location['x'], ele.location['y'], ele.size['width'], ele.size['height'])

    def search_cancel(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath('//android.widget.Button[@text="Cancel"]')
            ele.click()
        else:
            eles = self.mb.select_buttons(RDKMobileTopBar.__fx_ios_topbar_pos_define['cancel'])
            for i in range(eles.size):
                print(eles.get(i).location)
                if eles.get(i).location['y'] > 0:
                    eles.get(i).click()
                    return


    def search_clear(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath('//android.widget.LinearLayout/android.widget.EditText/parent::*/android.widget.ImageView[2]')
            if ele == None:
                return False
            ele.click()
            return True
        else:
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeSearchField/XCUIElementTypeButton[@name="Clear text"]')
            if ele == None:
                return False
            ele.click()
            return True
            

    def search_get_edittext_str(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.select_editText()
            if ele == None:
                return None
            return ele.text
        else:
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeSearchField')
            if ele == None:
                return None
            return ele.value
            

    def search_get_total(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "Total Found")]')
        else:
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeStaticText[contains(@name, "Totally found")]')
            if ele == None:
                return 0
        return int(ele.name.split(' ')[-1])

    def search_get_result(self):
        all_res = []
        if self.mb.platform_name == 'Android':
            els = self.mb.find_elements_by_xpath(
                '//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')
            if els == None:
                return []
            for i in range(els.size):
                ele = els.get(i)
                all_res.append(ele.name)
        else:
            time.sleep(3)
            els = self.mb.find_elements_by_xpath(
                '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@name, "Page ")]/parent::*/XCUIElementTypeStaticText')
            if els == None:
                return []
            for i in range(els.size):
                ele = els.get(i)
                all_res.append(ele.name)
        self.search_result = all_res
        return all_res
            

    def search_select(self, str, index=None):
        if self.mb.platform_name == 'Android':
            if index == None:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]' % str)
            else:
                eles = self.mb.find_elements_by_xpath(
                    '//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]' % str)
                for i in range(eles.size):
                    ele = eles.get(index)
            ele.click()
        else:
            ## iOS not support.
            pass

    def search_select_by_index(self, i):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]' % str)
            ele.click()
        else:
            res_cnt = 0
            page_i = -1
            for res in self.search_result:
                if res.find('Page') == -1:
                    res_cnt = res_cnt + int(res)
                    if i < res_cnt:
                        break
                else:
                    page_i += 1
            i = page_i + i
                    
            ele = self.mb.find_element_by_xpath(
                '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@name, "Page ")]/parent::*/parent::*/XCUIElementTypeCell[%d]' % i)
            ele.click()
            

    def search_next(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView/parent::*/following-sibling::*')
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True
        else:
            for i in range(10):
                try:
                    ele = self.mb.find_element_by_accessibility_id('search next')
                    print('next:', ele.location)
                    ele.click()
                    return True
                except:
                    time.sleep(1)

    def search_prev(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView/parent::*/preceding-sibling::*')
            if ele.is_enabled() == False:
                return False
            ele.click()
            return True
        else:
            ele = self.mb.find_element_by_accessibility_id("search previous")
            print('previous:', ele.location)
            ele.click()
            return True

    def search_panel(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView')
            ele.click()
        else:
            ele = self.mb.find_element_by_accessibility_id("search showlist")
            print('list:', ele.location)
            ele.click()
            return True


    ## 'Properties'
    def more_select(self, s):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath('//android.widget.RelativeLayout/android.widget.TextView[@text="%s"]' % RDKMobileTopBar.__fx_android_more_define[s])
            ele.click()
        else:
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeCell/XCUIElementTypeStaticText[@name="%s"]' % s)
            ele.click()

    def form_is_enable(self, type_name=None):
        if self.mb.platform_name == 'Android':
            if type_name == None:
                els = self.mb.find_elements_by_xpath('//android.widget.RelativeLayout/android.widget.TextView[contains(@text, "Form")]')
                for i in range(els.size):
                    ele = els.get(i)
                    if ele.is_enabled() == True:
                        return True
                return False
            else:
                ele = self.mb.find_element_by_xpath(
                    '//android.widget.RelativeLayout/android.widget.TextView[@text="%s"' % type_name)
                return ele.is_enabled()
        else:
            if type_name == None:
                ele = self.mb.find_element_by_accessibility_id('Reset Form Fields')
                ele.click()
                form_data_ele = self.mb.find_element_by_accessibility_id('This document has no form data')
                if form_data_ele != None:
                    ok_ele = self.mb.find_element_by_accessibility_id('OK')
                    ok_ele.click()
                    self.topbar_select('more')
                    return False
                else:
                    no_ele = self.mb.find_element_by_accessibility_id('No')
                    no_ele.click()
                    self.topbar_select('more')
                    
                return True
            else:
                ele = self.mb.find_element_by_accessibility_id(type_name)
                return ele.is_enabled()

    def form_export_data(self, save_name=None, replace='Yes'):
        self.more_select('Export Form Data')
        if self.mb.platform_name == 'Android':
            for i in range(10):
                ele = self.mb.find_element_by_xpath('//android.widget.EditText')
                if ele == None:
                    time.sleep(1)
                    continue
                if save_name != None:
                    self.mb.press_keycode(67)
                    for i in range(len(save_name)):
                        self.mb.press_keycode(112)
                    ele.send_keys(save_name)

                if replace == 'Yes':
                    self.mb.click_ok()
                    ele = self.mb.find_element_by_xpath(
                        '//android.widget.TextView[@text="The file already exists, do you want to replace it?"]')
                    if ele != None:
                        ok_ele = self.mb.select_button('OK')
                        ok_ele.click()
                else:
                    self.mb.click_cancel()
                return True
            return False
        else:
            if save_name == None:
                return True
            ele = self.mb.find_element_by_accessibility_id('Select "OK" to save the document here.')
            if ele != None:
                ok_ele = self.mb.find_element_by_accessibility_id('OK')
                ok_ele.click()
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeTextField')
                ele.send_keys(save_name)
                ok_ele = self.mb.find_element_by_accessibility_id('OK')
                ok_ele.click()

                if None != self.mb.find_element_by_accessibility_id('File already exists'):
                    if replace == 'Yes':
                        ele = self.mb.find_element_by_accessibility_id('Replace')
                    else:
                        ele = self.mb.find_element_by_accessibility_id('Cancel')
                    ele.click()
                success_ele = self.mb.find_element_by_accessibility_id('Form data was successfully exported.')
                if None == success_ele:
                    return False
                else:
                    ok_ele = self.mb.find_element_by_accessibility_id('OK')
                    ok_ele.click()
                return True
                        
            else:
                return False
            return True
            
                

    def form_import_data(self, xml_name):
        self.more_select('Import Form Data')
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="0_fxtest_xml"]')
            ele.click()

            file_ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % xml_name)
            while file_ele == None:
                file_ele = self.mb.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % xml_name)
                if file_ele == None:
                    self.mb.flick(self.s_w / 2, self.s_h / 2, 0, -self.s_h / 3)
                    continue
            file_ele.click()
            self.mb.click_ok()
        else:
            ele = self.mb.find_element_by_accessibility_id(xml_name)
            if ele == None:
                return False
            ele.click()
            
            ele = self.mb.find_element_by_accessibility_id('Select')
            ele.click()

            success_ele = self.mb.find_element_by_accessibility_id('Successfully imported data to the current document.')
            if success_ele == None:
                return False
            return True
        
        

    def file_information_get_all(self):
        if self.mb.platform_name == 'Android':
            els = self.mb.find_elements_by_xpath('//android.widget.TableRow/android.widget.TextView')
            i = 0
            info_dic = {}
            for i in range(els.size):
                ele = els.get(i)
                if i == 0:
                    page_info = ele.name
                    continue
                if i % 2 != 0:
                    info_dic[page_info] = ele.name
                else:
                    page_info = ele.name
        else:
            els = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText')
            info_dic = {}
            for i in range(els.size):
                ele = els.get(i)
                print(ele.name)
                if ele.name[-1:] == u':':
                    page_info = ele.name
                else:
                    info_dic[page_info] = ele.name
                    page_info = ''
        return info_dic
    
    def file_information_get_last_modified(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath('//android.widget.TextView[contains(@text,"Last modified")]/../android.widget.TextView[2]')
            last_modified_time = ele.name
            self.mb.tap([(1,1)])
            return last_modified_time
            
        else:
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Last Modified:"]/../XCUIElementTypeStaticText[2]')
            last_modified_time = ele.name
            back_ele = self.mb.find_element_by_xpath('//XCUIElementTypeButton[@name="property backselected"]')
            back_ele.click()
            return last_modified_time   
        

    def file_information_get_security(self):
        security_dic = {}
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath('//android.widget.LinearLayout/android.widget.TextView[@text="Security"]/following-sibling::*[1]/android.widget.TextView')
            security_dic['Security'] = ele.name
            ele.click()

            while None == self.mb.find_element_by_xpath('//android.widget.TextView[@text="Document Restrictions Summary"]'):
                time.sleep(1)

            els = self.mb.find_elements_by_xpath('//android.widget.RelativeLayout/android.widget.TextView')
            i = 0
            for i in range(els.size):
                ele = els.get(i)
                if i == 0:
                    page_info = ele.name
                    continue
                if i % 2 != 0:
                    security_dic[page_info] = ele.name
                else:
                    page_info = ele.name
        else:
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeOther/XCUIElementTypeStaticText[@name="Security"]/parent::*/following-sibling::*[1]/XCUIElementTypeStaticText')
            security_dic['Security'] = ele.name
            ele.click()

            els = self.mb.find_elements_by_xpath('//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText')
            for i in range(els.size):
                ele = els.get(i)
                print(ele.name)
                if i == 0:
                    page_info = ele.name
                    continue
                if i % 2 != 0:
                    security_dic[page_info] = ele.name
                else:
                    page_info = ele.name
##                if ele.name[-1:] == u':':
##                    page_info = ele.name
##                else:
##                    security_dic[page_info] = ele.name
##                    page_info = ''
        return security_dic

    def file_information_cancel(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]')
            ele.click()
        else:
            ele = self.mb.find_element_by_accessibility_id('common back black')
            ele.click()


    def more_cancel(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]')
            ele.click()
        else:
            ele = self.mb.find_element_by_accessibility_id('property backselected')
            ele.click()

    def more_back(self):
        if self.mb.platform_name == 'Android':
            ele = self.mb.find_element_by_xpath(
                '//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.ImageView')
            if ele == None:
                self.mb.tap([(5, 5)])
                return
            ele.click()
        else:
            ele = self.mb.find_element_by_accessibility_id('property backselected')
            ele.click()

            

class RDKMobilePopup:
    def __init__(self, screen_w=0, screen_h=0, device_dpi="640", mode='find'):
        self.img_process = FXImageProcess('10.103.129.80:32454')
        self.dif_rt = None
        self.pos_dic = {}
        self.popup_img = None
        self.mode = 'parse'
        self.s_w = screen_w
        self.s_h = screen_h
        self.dpi = str(device_dpi)
        self.mode = mode

    def set_popup_img(self, popup_img):
        self.popup_img = popup_img

    def parse(self, pre_img):
        if self.mode == 'find':
            return

        # Get Popup Location
        self.dif_rt = self.img_process.difference(pre_img, self.popup_img, disparities=16)
        print('Popup Pos:', self.dif_rt.x, self.dif_rt.y, self.dif_rt.w, self.dif_rt.h)

        popup = popup_img.crop((self.dif_rt.x, self.dif_rt.y, self.dif_rt.x + self.dif_rt.w, self.dif_rt.y + self.dif_rt.h))
        # aaa.save('aaa.png')
        eles = self.img_process.detect(popup, thresh=80, blur_x=19, blur_y=19, filter=True)

        for ele in eles:
            tem = popup
            ele_img = tem.crop((ele[0], ele[1], ele[0] + ele[2], ele[1] + ele[3]))
            # ele_img.show()
            r = self.img_process.ocr(ele_img)
            if r != '':
                self.pos_dic[r] = ele

    def select(self, name):
        if self.mode == 'find':
            template_img_path = 'img/RDKDemo/android_annot_popup_%s_%dx%dx%s.png' % (name, self.s_w, self.s_h, self.dpi)
            if not os.path.isfile(template_img_path):
                template_img_path = 'img/RDKDemo/android_annot_popup_%s_1440x2560.png' % name
                fximg0 = FXImage(filepath=template_img_path)
                img0 = fximg0.image
                width, height = img0.size
                if self.s_w > 1440:
                    radio = self.s_w / 1440
                    img = img0.resize((width * radio, height * radio), Image.ANTIALIAS)
                else:
                    radio = 1440 / self.s_w
                    img = img0.resize((width / radio, height / radio), Image.ANTIALIAS)
            else:
                img = FXImage(filepath=template_img_path).image
            rect = self.img_process.find(self.popup_img, img)
            sel_pos = ((rect.x0 + rect.x1) / 2, \
                       (rect.y0 + rect.y1) / 2)
            print(sel_pos)
        else:
            sel_pos = (self.dif_rt.x + self.pos_dic[name][0] + self.pos_dic[name][2] / 2, \
                       self.dif_rt.y + self.pos_dic[name][1] + self.pos_dic[name][3] / 2)
        print('Screen Pos:', sel_pos)
        return sel_pos
        # mb.tap([sel_pos])
        # print('END')

    def get_display_circle_region_pos(self, popup_img):
        fximg = FXImage()
        fximg.open('img/RDKDemo/android_circle_region.png')
        circle_template_img = fximg.image
        match_pos = self.img_process.similarity(circle_template_img, popup_img, matching_distance=0.8, debug=False)
        return match_pos


class RDKMobileAnnotActionHandle:
    def __init__(self, mb):
        self.mb = mb
        s_s = self.mb.get_screen_size()
        self.s_w = s_s['width']
        self.s_h = s_s['height']
        self.dpi = self.mb.device_dpi

        self.rect = {'x0': self.s_w, 'y0': self.s_h, 'x1': 0, 'y1': 0}
        self.pos = []
        self.mov_pos = []
        self.poper = None
        self.parsed_popup = False
        self.popup_img = None

    def _ios_adjust(self):
        if self.mb.platform_name != 'iOS':
            return True
        ele = self.mb.find_element_by_xpath('//XCUIElementTypeMenu/XCUIElementTypeMenuItem[@name="Open"]', timeout=5)
        if ele != None:
            self.parsed_popup = True
            self.mb.tap([(5, self.s_h / 2)])
            return True
        i = 0
        while ele == None:
            if i > self.mov_pos[0]:
                return False
            i = i + 2
            self.pos[0] = self.pos[0] + i
            self.pos[1] = self.pos[1] + i
            print(self.pos)
            self.mb.tap([self.pos])
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeMenu/XCUIElementTypeMenuItem[@name="Open"]', timeout=5)
##                print(self.mb.page_info())
            if ele != None:
                self.parsed_popup = True
                self.mb.tap([(5, self.s_h / 2)])
                return True

    def draw(self, pos, move_pos, reuse=False):
##        self.mb.tap([(pos[0], pos[1])], 0.5)
        print('from:', pos[0], pos[1])
        print('to:', pos[0]+move_pos[0], pos[1]+move_pos[1])
        self.mb.long_flick(pos[0], pos[1], pos[0] + move_pos[0], pos[1] + move_pos[1])
##        time.sleep(3)
        
##        self.mb.swipe(pos[0], pos[1], move_pos[0], move_pos[1], 1000)
##        self.mb.long_flick(pos[0], pos[1], move_pos[0], move_pos[1], 0.1)
        if pos[0] < self.rect['x0']:
            self.rect['x0'] = pos[0]
        if pos[0] > self.rect['x1']:
            self.rect['x1'] = pos[0] + move_pos[0]
        if pos[1] < self.rect['y0']:
            self.rect['y0'] = pos[1]
        if pos[1] > self.rect['y1']:
            self.rect['y1'] = pos[1] + move_pos[1]
        self.pos.append(pos[0])
        self.pos.append(pos[1])
        self.mov_pos.append(move_pos[0])
        self.mov_pos.append(move_pos[1])
        #self.mov_pos = move_pos

    def scale(self, scale_pos, type='r_bottom'):
        print('Start Scale')
        if self.mb.platform_name != 'iOS' and self.parsed_popup != True:
            self._ios_adjust()
        time.sleep(2)
        self.mb.tap([self.pos])
        time.sleep(5)
        if type == 'r_bottom':
            self.mb.long_flick(self.rect['x1'] + 20, self.rect['y1'] + 20, self.rect['x1'] + scale_pos[0], self.rect['y1'] + scale_pos[1])
            # self.mb.flick(self.rect['x1'] + 20, self.rect['y1'] + 20, scale_pos[0], scale_pos[1])
            self.rect['x1'] = self.rect['x1'] + scale_pos[0]
            self.rect['y1'] = self.rect['y1'] + scale_pos[1]
        elif type == 'r_top':
            self.mb.long_flick(self.rect['x1'] + 20, self.rect['y0'] - 20, self.rect['x1'] + scale_pos[0],
                               self.rect['y0'] + scale_pos[1],
                               duration=2)
            self.rect['x1'] = self.rect['x1'] + scale_pos[0]
            self.rect['y0'] = self.rect['y0'] + scale_pos[1]
        elif type == 'r_middle':
            self.mb.long_flick(self.rect['x1'] + 20, (self.rect['y0'] + self.rect['y1']) / 2 + 10,
                               self.rect['x1'] + scale_pos[0],
                               (self.rect['y0'] + self.rect['y1']) / 2 + scale_pos[1])
            self.rect['x1'] = self.rect['x1'] + scale_pos[0]
        elif type == 'l_bottom':
            if self.mb.platform_name == "Android" and self.mb.platform_version != '4.1.2':
                self.mb.long_flick(self.rect['x0'] - 20, self.rect['y1'] + 20, self.rect['x0'] + scale_pos[0],
                                   self.rect['y1'] + scale_pos[1])
            else:
                self.mb.flick(self.rect['x0'], self.rect['y1'], scale_pos[0], scale_pos[1])
            self.rect['x0'] = self.rect['x0'] + scale_pos[0]
            self.rect['y1'] = self.rect['y1'] + scale_pos[1]
        elif type == 'l_top':
            self.mb.long_flick(self.rect['x0'] - 20, self.rect['y0'] - 20, self.rect['x0'] + scale_pos[0],
                               self.rect['y0'] + scale_pos[1])
            self.rect['x0'] = self.rect['x0'] + scale_pos[0]
            self.rect['y0'] = self.rect['y0'] + scale_pos[1]
        elif type == 'l_middle':
            self.mb.long_flick(self.rect['x0'] - 20, (self.rect['y0'] + self.rect['y1']) / 2 + 10,
                          self.rect['x0'] + scale_pos[0], (self.rect['y0'] + self.rect['y1']) / 2 + scale_pos[1])
            self.rect['x0'] = self.rect['x0'] + scale_pos[0]
        elif type == 't_middle':
            self.mb.long_flick((self.rect['x0'] + self.rect['x1']) / 2, self.rect['y0'] - 20,
                               (self.rect['x0'] + self.rect['x1']) / 2 + scale_pos[0], self.rect['y0'] + scale_pos[1])
            self.rect['y0'] = self.rect['y0'] + scale_pos[1]
        elif type == 'b_middle':
            self.mb.long_flick((self.rect['x0'] + self.rect['x1']) / 2, self.rect['y1'] + 20,
                               (self.rect['x0'] + self.rect['x1']) / 2 + scale_pos[0], self.rect['y1'] + scale_pos[1])
            self.rect['y1'] = self.rect['y1'] + scale_pos[1]
        else:
            return False
        if self.mb.platform_name == 'iOS':
            self.mb.tap([(5, self.s_h / 2)])
        print(self.rect)
        return True

    def move(self, move_pos):
        if self.mb.platform_name != 'iOS' and self.parsed_popup != True:
            self._ios_adjust()
        print('Start Move')
        time.sleep(1)
        self.mb.tap([self.pos])
        time.sleep(1)
        if self.mb.platform_name == 'iOS':
            self.mb.flick(self.rect['x0'], self.rect['y0'] + (self.rect['y1'] - self.rect['y0']) / 2, move_pos[0], move_pos[1])
        else:
            self.mb.long_flick((self.rect['x0'] + self.rect['x1']) / 2, (self.rect['y0'] + self.rect['y1']) / 2,
                               (self.rect['x0'] + self.rect['x1']) / 3 + move_pos[0],
                               (self.rect['y0'] + self.rect['y1']) / 2 + move_pos[1], duration=5000)
        time.sleep(1)
        self.mb.tap([(5, self.s_h / 2)])
        time.sleep(1)
        self.pos = [self.pos[0] + move_pos[0], self.pos[1] + move_pos[1]]
        #self.pos = (self.pos[0] + mo, self.pos[1])
        self.rect['x0'] = self.rect['x0'] + move_pos[0]
        self.rect['x1'] = self.rect['x1'] + move_pos[0]
        self.rect['y0'] = self.rect['y0'] + move_pos[1]
        self.rect['y1'] = self.rect['y1'] + move_pos[1]
        print('End Move')

    def popup_menu(self, parse=False, mode='find', duration=1500):
        print('Start Popup')
        if self.mb.platform_name != 'iOS':
            self.mb.tap([(5, self.s_h / 2)])
            time.sleep(3)
        else:
            if self.parsed_popup == False:
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeMenu/XCUIElementTypeMenuItem', timeout=5)
                if ele != None:
                    self.parsed_popup = True
                    return True
##            if True == self.parsed_popup:
##                self.mb.tap([self.pos])
            i = 0
            while 1:
                if i > self.mov_pos[0] and i > self.mov_pos[1]:
                    return False
                i = i + 2
                self.pos[0] = self.pos[0] + i
                self.pos[1] = self.pos[1] + i
                print(self.pos)
                self.mb.tap([self.pos])
                ele = self.mb.find_element_by_xpath('//XCUIElementTypeMenu/XCUIElementTypeMenuItem', timeout=5)
##                print(self.mb.page_info())
                if ele != None:
                    self.parsed_popup = True
                    return True
            return True
        
        if parse == True and mode != 'find':
            before_img_path = self.mb.screenshot('BeforePopup.png')
            time.sleep(3)  # Wait Render.

        self.mb.tap([self.pos], duration)
        if self.mb.platform_name == 'iOS':
            return
        time.sleep(3)
        print('End Popup')

        new_path = self.mb.screenshot('Popup.png')
        self.popup_img = Image.open(new_path)
        self.poper = RDKMobilePopup(self.s_w, self.s_h, self.dpi, mode=mode)
        self.poper.set_popup_img(self.popup_img)
        if not parse:
            return
        if mode == 'find':
            self.poper.parse(None)
        else:
            img_pre = Image.open(before_img_path)
            self.poper.parse(img_pre)

    def popup_menu_select(self, name, auto_popup=False):
        if self.mb.platform_name == 'iOS':
            ele = self.mb.find_element_by_xpath('//XCUIElementTypeMenu/XCUIElementTypeMenuItem[@name="%s"]' \
                                                % name)
            ele.click()
        else:
            if auto_popup:
                after_path = self.mb.screenshot('Popup.png')
                img_after = Image.open(after_path)
                self.poper = RDKMobilePopup(self.s_w, self.s_h, self.dpi)
                self.poper.parse(None, img_after, 'find')
            if self.poper == None:
                return False
            sel_pos = self.poper.select(name)
            self.mb.tap([sel_pos])
            return True

    def popup_menu_is_show_circle_region(self):
        if self.mb.platform_name == 'iOS':
            return True
        else:
            if self.popup_img == None or self.poper == None:
                return False
            match_pos = self.poper.get_display_circle_region_pos(self.popup_img)
            if len(match_pos) < 2:
                return False
            return True



    @property
    def rect(self):
        return self.rect


