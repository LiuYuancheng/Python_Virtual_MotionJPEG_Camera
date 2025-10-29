#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        mgmHMIPlcDataMgr.py
#
# Purpose:     Data management module to start a sub-thread to connect to the 
#              PLCs fetch the plc state and send control request.
#
# Author:      Yuancheng Liu
#
# Created:     2025/06/13
# Version:     v_0.0.3
# Copyright:   Copyright (c) 2025 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import time
import io
import wx
import requests
import threading

import camDashboardGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class camStreamDataManager(threading.Thread):
    """ The data manager is a module running parallel with the main thread to 
        connect to PLCs to do the data communication with IEC-104.
    """
    def __init__(self, parent, urlList, interval=0.3) -> None:
        threading.Thread.__init__(self)
        self.parent = parent
        self.urlList = urlList
        self.interval = interval # image fetch interval time.
        self.bitmapDict = {}
        for url in urlList:
            self.bitmapDict[url] = None
        self.terminate = None

    #-----------------------------------------------------------------------------
    def getJPGImgFile(self, filePath, url):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                if 'image/jpeg' in response.headers.get('Content-Type', ''):
                    # Open a file in binary write mode and save the image content
                    with open(filePath, 'wb') as f:
                        f.write(response.content)
                    gv.gDebugPrint("Image saved to %s" %str(filePath), logType=gv.LOG_INFO)
            else:
                gv.gDebugPrint("Failed to retrieve image. Status code: %s" %str(response.status_code), logType=gv.LOG_WARN)
                gv.gDebugPrint("Response: %s" %str(response.text), logType=gv.LOG_WARN)
        except requests.exceptions.RequestException as e:
            gv.gDebugPrint("Error: getJPGImgFile() error occurred during the request: %s" %str(e), logType=gv.LOG_ERR)


    #-----------------------------------------------------------------------------
    def getJPGImgDataBM(self, url):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                if 'image/jpeg' in response.headers.get('Content-Type', ''):
                    imageStream = io.BytesIO(response.content)
                    wxImage = wx.Image(imageStream, wx.BITMAP_TYPE_ANY)
                    # Convert wx.Image → wx.Bitmap (ready for GUI display)
                    bitmap = wxImage.ConvertToBitmap()
                    return bitmap
            else:
                gv.gDebugPrint("Failed to retrieve image. Status code: %s" %str(response.status_code), logType=gv.LOG_WARN)
                gv.gDebugPrint("Response: %s" %str(response.text), logType=gv.LOG_WARN)
                return None
        except requests.exceptions.RequestException as e:
            gv.gDebugPrint("Error: getJPGImgFile() error occurred during the request: %s" %str(e), logType=gv.LOG_ERR)

    #-----------------------------------------------------------------------------
    def run(self):
        time.sleep(1)
        while not self.terminate:
            for url in self.urlList:
                self.bitmapDict[url] = self.getJPGImgDataBM(url)
            time.sleep(0.5)

    #-----------------------------------------------------------------------------
    def getImageBitmap(self, url):
        if url in self.bitmapDict:
            return self.bitmapDict[url]
        return None

    #-----------------------------------------------------------------------------
    def stop(self):
        self.terminate = True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    test = camStreamDataManager(None, None)
    test.getImageData('http://127.0.0.1:5000//cgi-bin/mjpg/motionJPEG')