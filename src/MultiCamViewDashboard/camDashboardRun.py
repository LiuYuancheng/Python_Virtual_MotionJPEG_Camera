#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        camDashboardRun.py
#
# Purpose:     This module is multi camera view dashboard application.
#              
# Author:      Yuancheng Liu
#
# Version:     v_0.0.1
# Created:     2025/10/27
# Copyright:   Copyright (c) 2025 Liu Yuancheng
# License:     MIT License    
#-----------------------------------------------------------------------------
"""
    System Design Purpose: 
        This module is the multi-camera monitoring dashboard application to fetch 
        the motion-jpeg ideo from different virtual cameras via http request.
"""
import time
import wx

import camDashboardGlobal as gv
import camDashboardPanel
import camDashboardDataMgr as dataMgr

FRAME_SIZE = (1900, 1050) # default UI frame size.
HELP_MSG="""
If there is any bug, please contact:
 - Author:      Yuancheng Liu 
 - Email:       liu_yuan_cheng@hotmail.com 
 - Created:     2025/10/27 
 - GitHub Link: https://github.com/LiuYuancheng/Python_Virtual_MotionJPEG_Camera
"""

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""

    def __init__(self, parent, id, title):
        """ Init the main UI and parameters."""
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        #self.SetIcon(wx.Icon(gv.ICO_PATH))
        self._initGlobals()
        # Build UI sizer
        self.camPanelDict = {}
        self._buildMenuBar()
        self.SetSizer(self._buildUISizer())
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' % str(gv.TEST_MD))
        # Init the local parameters:
        self.updateLock = False
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(gv.PERIODIC)  # every 500 ms
        self.Bind(wx.EVT_CLOSE, self.onClose)
        if not gv.TEST_MD and gv.iDataMgr: gv.iDataMgr.start()
        gv.gDebugPrint("Multi Camera View Dashboard UI Frame Inited, test mode: %s" % str(gv.TEST_MD), 
                       logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def _initGlobals(self):
        """ Init the global parameters used only by this module."""
        if not gv.TEST_MD:
            # build the url list
            camConfigDict = gv.iCamConfigLoader.getJsonData()
            urlList = []
            for item in camConfigDict.values():
                print(item)
                urlStr= item['url']+item['token']
                urlList.append(urlStr)
            gv.iDataMgr = dataMgr.camStreamDataManager(self, urlList)

    #-----------------------------------------------------------------------------
    def _buildMenuBar(self):
        """ Create the top function menu bar."""
        menubar = wx.MenuBar()
        # Add the about menu.
        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, 200, text="Help", kind=wx.ITEM_NORMAL)
        helpMenu.Append(aboutItem)
        self.Bind(wx.EVT_MENU, self.onHelp, aboutItem)
        menubar.Append(helpMenu, '&About')
        self.SetMenuBar(menubar)

    #-----------------------------------------------------------------------------
    def _buildUISizer(self):
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        camConfigDict = gv.iCamConfigLoader.getJsonData()
        gSizer = wx.GridSizer(2, 2, 2, 2)
        for key in camConfigDict.keys():
            imagePnl = camDashboardPanel.PanelImage(self, panelSize=(900, 500))
            self.camPanelDict[key] = imagePnl
            gSizer.Add(imagePnl, 0, flagsL, 5)
        mSizer.Add(gSizer, 0, flagsL, 5)
        mSizer.AddSpacer(5)
        return mSizer

    #-----------------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            camConfigDict = gv.iCamConfigLoader.getJsonData()
            for key in camConfigDict.keys():
                urlStr= camConfigDict[key]['url']+camConfigDict[key]['token']
                bitmap = gv.iDataMgr.getImageBitmap(urlStr)
                self.camPanelDict[key].updateBitmap(bitmap)
                self.camPanelDict[key].updateDisplay()

    #-----------------------------------------------------------------------------
    def onHelp(self, event):
        """ Pop-up the Help information window. """
        wx.MessageBox(HELP_MSG, 'Help', wx.OK)
        
    #-----------------------------------------------------------------------------
    def onClose(self, evt):
        """ Pop up the confirm close dialog when the user close the UI from 'x'."""
        try:
            fCanVeto = evt.CanVeto()
            if fCanVeto:
                confirm = wx.MessageDialog(self, 'Click OK to close this program, or click Cancel to ignore close request',
                                            'Quit request', wx.OK | wx.CANCEL| wx.ICON_WARNING).ShowModal()
                if confirm == wx.ID_CANCEL:
                    evt.Veto(True)
                    return
                if gv.iDataMgr: gv.iDataMgr.stop()
                self.timer.Stop()
                self.Destroy()
        except Exception as err:
            gv.gDebugPrint("Error to close the UI: %s" %str(err), logType=gv.LOG_ERR)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.UI_TITLE)
        gv.iMainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
