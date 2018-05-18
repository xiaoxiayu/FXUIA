import applescript

##
##def getWindowRect(winID):
##    dsp = Display()
##    window = dsp.create_resource_object('window', winID)
##    geo = window.get_geometry()
##    gpos = [geo.x,  geo.y]
##    def wrapped(obj):
##      par = obj.query_tree().parent
##      if par:
##        p = par.get_geometry()
##        gpos[0] += p.x
##        gpos[1] += p.y
##        wrapped(par)
##    
##    wrapped(window)
##    print(gpos[0], gpos[1], geo.width, geo.height)
##    return (gpos[0], gpos[1], geo.width, geo.height)
##
##def getVisibleWindows():
##    """ Not the quickest function, but it does the job quite well!
##    """
##    ''' query_tree returns the windows as a tree - as seen by the user '''
##    windows = root.query_tree().children
##    result = []
##
##    def wrapped(obj, name, classname, pos, size):
##      ID = obj.id if isinstance(obj.id, int) else obj.id.id
##      if size > (1,1) and pos >= (0,0):
##        result.append({'obj':  ID, 
##                       'name': name,
##                       'class': classname,
##                       'pos':  pos,
##                       'size': size})
##          
##      children = obj.query_tree().children
##      for child in children:
##        attrs = child.get_attributes()
##        if attrs.map_state == X.IsViewable:
##          p = child.get_geometry()
##          wrapped(obj  = child, 
##                  name = child.get_wm_name(),
##                  classname = child.get_wm_class(),
##                  pos  = (pos[0]+p.x, pos[1]+p.y), 
##                  size = (p.width, p.height))
##          
##
##    for wnd_id in windows:
##      wnd = dsp.create_resource_object('window', wnd_id)
##      attrs = wnd.get_attributes()
##      if attrs.map_state == X.IsViewable:
##        f = wnd.id.get_geometry()
##        name = wnd.get_wm_name() if wnd.get_wm_name() != None else 'Frame'
##        classname = wnd.get_wm_class() if wnd.get_wm_class() != None else None
##        wrapped(obj  = wnd, 
##                name = name,
##                classname = classname,
##                pos  = (f.x, f.y),
##                size = (f.width, f.height))
##
##    return result
##
##def printWindowHierrarchy(window, indent):
##    children = window.query_tree().children
##    for w in children:
####        print(window.get_wm_class())
##        if window.get_wm_class() != None:
##            for t in window.get_wm_class():
##                if t.find('Foxit') != -1:
##                    print(w.get_wm_name())
##                    print(w.get_geometry())
##        printWindowHierrarchy(w, indent+'-')
##
##        
def setTopWindow(appName):
    print('setwindow')
    cmd_str = '''
    tell application "System Events"
        tell process "%s"
            set frontmost to true
            set visible to true
        end tell
    end tell
    ''' % appName
    try:
        applescript.AppleScript(cmd_str).run()
    except:
        return False
    return True


##
def getTopWindow():
   cmd_str = '''
   global frontApp, frontAppName, windowTitle

    set windowTitle to ""
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set frontAppName to name of frontApp
        tell process frontAppName
            tell (1st window whose value of attribute "AXMain" is true)
                set windowTitle to value of attribute "AXTitle"
            end tell
        end tell
    end tell

    return {frontAppName, windowTitle}
   '''
   return applescript.AppleScript(cmd_str).run()
##
###-----------------------------------------------------------------------
##def isTopWindow(winID):
##    atom = dsp.intern_atom('_NET_ACTIVE_WINDOW') 
##    window = root.get_full_property(atom, X.AnyPropertyType).value
##    if winID == window[0]:
##      return True
##    else:
##      return False
##
###-----------------------------------------------------------------------
def moveWindow(appName, X,Y):
    cmd_str = '''
    tell application "System Events"
        set position of first window of application process "%s" to {%d, %d}
    end tell ''' % (appName, X, Y)
    return applescript.AppleScript(cmd_str).run()
##
###-----------------------------------------------------------------------
##def resizeWindow(W,H):
##    win = dsp.create_resource_object('window', winID)
##    R = getWindowRect(winID)
##    win.configure(width=W, height=H)
##    dsp.flush()

#-----------------------------------------------------------------------
def getScreenSize():
    cmd_str = '''
    tell application "Finder"
      set _b to bounds of window of desktop
      set _width to item 3 of _b
    end tell'''
    w = applescript.AppleScript(cmd_str).run()

    cmd_str = '''
    tell application "Finder"
      set _b to bounds of window of desktop
      set _height to item 4 of _b
    end tell'''
    h = applescript.AppleScript(cmd_str).run()
    
    return w,h

#-----------------------------------------------------------------------  
def getDesktopScreenSize():
    cmd_str = '''
    tell application "Finder"
      get bounds of window of desktop
    end tell'''
    return applescript.AppleScript(cmd_str).run()
##    try:
##        prime = root.xrandr_get_screen_info()._data['sizes'][1]
##        size = prime['width_in_pixels'], prime['height_in_pixels']
##    except:
##        size = getScreenSize()
##    return size

#-----------------------------------------------------------------------
def getRoot():
    pass
##    window = root.id
##    return window

#-----------------------------------------------------------------------
def getWindowParent(winID):
    pass
##    window = dsp.create_resource_object('window', winID)
##    return window.query_tree().parent

#-----------------------------------------------------------------------
def getWindowChildren(winID):
    pass
##    window = dsp.create_resource_object('window', winID)
##    children = window.query_tree().children
##    return children

###-----------------------------------------------------------------------
##def getWindowGeo(winID):
##    window = dsp.create_resource_object('window', winID)
##    return window.get_geometry()
##
###-----------------------------------------------------------------------
##def getWindowObjGeo(win):
##    return win.get_geometry()

#-----------------------------------------------------------------------
def getWindowRect(appName):
    cmd_str = '''
    activate application "%s"
    tell application "System Events" to tell process "%s"
        set visible to true
        get position of window 1
    end tell''' % (appName, appName)
    pos = applescript.AppleScript(cmd_str).run()

    cmd_str = '''
    tell application "System Events" to tell process "%s"
        set visible to true
        get size of window 1
    end tell''' % appName
    size = applescript.AppleScript(cmd_str).run()
    return [pos[0], pos[1], size[0], size[1]]

def setWindowSize(appName, w, h):
    cmd_str = '''
    tell application "System Events" to tell process "%s"
        set visible to true
        set size of window 1 to {%d, %d}
    end tell''' % (appName, w, h)
    return applescript.AppleScript(cmd_str).run()


def activateApplication(appName):
    cmd_str = '''activate application "%s"''' % appName
    return applescript.AppleScript(cmd_str).run()

def getFrontWindowTitle():
    cmd_str = '''
    tell application "System Events"
        # Get the frontmost app's *process* object.
        set frontAppProcess to first application process whose frontmost is true
    end tell

    # Tell the *process* to count its windows and return its front window's name.
    tell frontAppProcess
        if count of windows > 0 then
           set window_name to name of front window
        end if
    end tell
    '''
    return applescript.AppleScript(cmd_str).run()


def menuHandler(app_name, item0, item1):
    cmd_str = '''
    activate application "%s"
    delay 1
    tell application "System Events" to tell process "%s"
        click menu item "%s" of menu 1 of menu bar item "%s" of menu bar 1
    end tell
    ''' % (app_name, app_name, item1, item0)

    return applescript.AppleScript(cmd_str).run()
