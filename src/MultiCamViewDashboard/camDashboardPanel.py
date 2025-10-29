#-----------------------------------------------------------------------------
# Name:        camDashboardPanel.py
#
# Purpose:     This module will provide the panels for the multi camera view
#              monitor dashboard.
#              
# Author:      Yuancheng Liu
#
# Created:     2025/07/26
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2025 Liu Yuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import wx
import camDashboardGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelImage(wx.Panel):
    """ Panel to display the camera image. """

    def __init__(self, parent, panelSize=(640, 480)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour("BLACK"))
        self.panelSize = panelSize
        self.defaultBmp = wx.Bitmap(gv.BGIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.bmp = None # Current display bitmap
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    #-----------------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        if self.bmp is not None:
            dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        else:
            dc.DrawBitmap(self._scaleBitmap(self.defaultBmp, w, h), 0, 0)
            
    #-----------------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

    #-----------------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bmp = bitMap

    #-----------------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()