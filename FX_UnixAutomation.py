
import platform
import os

if platform.system() == 'Darwin':
    from unix import mac
elif platform.system() == 'Linux':
    from unix import x11
    import pyscreenshot as ImageGrab

from unix import pymouse
from unix import pykeyboard

__keyboard__ = pykeyboard.PyKeyboard()
__mouse__ = pymouse.PyMouse()


def fx_mouse_lclick(x, y):
    __mouse__.click(x, y)


def fx_mouse_rclick(x, y):
    __mouse__.click(x, y, 2)


def fx_mouse_lpress(x, y):
    __mouse__.press(x, y)


def fx_mouse_lrelease(x, y):
    __mouse__.release(x, y)


def fx_mouse_move(x, y):
    __mouse__.move(x, y)


def fx_mouse_scroll(v, h, depth=None):
    __mouse__.scroll(v, h, depth)


def fx_cursor_getpos():
    return __mouse__.position()


def fx_special_key(s):
    return __keyboard__.lookup_character_keycode(s)


def fx_keyboard_tap(s):
    __keyboard__.tap_key(s)


def fx_keyboard_press(s):
    __keyboard__.press_key(s)


def fx_keyboard_release(s):
    __keyboard__.release_key(s)


def fx_keyboard_press_combine(l):
    __keyboard__.press_keys(l)

def fx_send_string(s, t=0.01):
    __keyboard__.type_string(s)




def fx_window_get_rect(id):
    if platform.system() == 'Linux':
        return x11.getWindowRect(id)
    elif platform.system() == 'Darwin':
        return mac.getWindowRect(id)


def fx_screen_get_size():
    if platform.system() == 'Linux':
        return x11.getScreenSize()
    elif platform.system() == 'Darwin':
        return mac.getScreenSize()


def fx_window_get_top():
    if platform.system() == 'Linux':
        return x11.getTopWindow()
    elif platform.system() == 'Darwin':
        return mac.getFrontWindowTitle()


def fx_window_close(id):
    pass


def fx_window_find(window_title):
    pass


def fx_window_set_top(id):
    if platform.system() == 'Linux':
        return x11.setTopWindow(id)
    elif platform.system() == 'Darwin':
        return mac.setTopWindow(id)


def fx_window_show(id):
    fx_window_set_top(id)


def fx_window_max(id):
    if platform.system() == 'Linux':
        reader_rect = x11.getWindowRect(id)
        sw, sh = x11.getScreenSize()
        if reader_rect[0] + reader_rect[2] == sw and \
            reader_rect[1] + reader_rect[3] == sh:
            return
        __mouse__.move(reader_rect[0]+reader_rect[2]/2, reader_rect[1]-5)
        __mouse__.click(reader_rect[0]+reader_rect[2]/2, reader_rect[1]-5)
        __mouse__.click(reader_rect[0]+reader_rect[2]/2, reader_rect[1]-5)
    elif platform.system() == 'Darwin':
        x, y, w, h = mac.getWindowRect(id)
        __mouse__.move(x + w / 2, y+5)
        __mouse__.click(x + w / 2, y+5)
        __mouse__.click(x + w / 2, y+5)


def fx_window_set_rect(id, x, y, w, h):
    if platform.system() == 'Linux':
        x11.moveWindow(id, x, y)
        x11.resizeWindow(id, w, h)
    elif platform.system() == 'Darwin':
        mac.moveWindow(id, x, y)


def fx_window_set_pos(id, x, y):
    if platform.system() == 'Linux':
        x11.resizeWindow(id, x, y)
    elif platform.system() == 'Darwin':
        mac.moveWindow(id, x, y)


def fx_window_set_size(id, w, h):
    if platform.system() == 'Linux':
        x11.resizeWindow(id, w, h)
    elif platform.system() == 'Darwin':
        mac.moveWindow(id, w, h)


def fx_window_get_title(id):
    pass


def fx_window_is_top(id):
    if platform.system() == 'Linux':
        return x11.isTopWindow(id)
    elif platform.system() == 'Darwin':
        app_name, title = mac.getTopWindow()
        if app_name.replace(' ', '') != id.replace(' ', ''):
            return False
        return True


def fx_window_get_visible():
    if platform.system() == 'Linux':
        return x11.getVisibleWindows()

def fx_activate_application(app_name):
    if platform.system() == 'Darwin':
        return mac.activateApplication(app_name)

def fx_menu(app_name, item0, item1):
    if platform.system() == 'Darwin':
        mac.menuHandler(app_name, item0, item1)

# send string
def fx_sendsavepath(astr): 
    patharr=os.path.split(astr)
    if platform.system()!='Darwin':
        if os.path.exists(astr):
            os.remove(astr)
        if os.path.exists(patharr[0])==False:
            os.mkdir(patharr[0])

	print('#####start to input path#######')
        fx_send_string(astr)
        print('#####finish to input path#######')



def fx_presskey(key):
    if platform.system()!='Darwin':
        fx_keyboard_press(key)






