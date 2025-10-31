#------------------------------------------------------------------------------
# Name:        virtualCamera.py
#
# Purpose:     This module is a virtual motion jpeg camera program to provide 
#              the video stream to a flask web page. It can capture the real 
#              video frame from a web-cam, a live video source or an images 
#              data set directory or the part of the desktop screen shot.
#
# Author:      Yuancheng Liu
#
# Created:     2025/10/15 
# version:     v_0.0.3
# Copyright:   Copyright (c) 2025 LiuYuancheng
# License:     GNU General Public License V3
#------------------------------------------------------------------------------
""" 
    Design Purpose: we want to generate the motion jpeg video stream which can 
    fetch the video frame from 4 types of source: 
        1. a web-cam/live video source
        2. an images data set directory
        3. capture from screen recording.
        4. capture from a running app window.(windows platform only)
        
    Then provide the video stream to a flask web page. 
    Motion JPEG formats: https://en.wikipedia.org/wiki/Motion_JPEG
    Usage: 
        refer to the test case module <virtualCameraTest.py>
"""
import os
import sys
import time
import cv2
import numpy as np
import pyautogui
# Capture from another App only works on windows platform.
if sys.platform == "win32":
    import win32gui
    import win32ui
    import win32con
    #from PIL import Image

# Default video stream frame rate
DEF_FPS = 10

# camera image timestamp format: 
FONT_TYPE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE = 0.5
FONT_COLOR = (0, 255, 255)  # Text color in BGR format (Blue, Green, Red)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class camClient(object):
    """ Virtual camera Interface module."""
    def __init__(self, fps=DEF_FPS):
        self.fpsNum = int(fps)
        self.capture = True     # Flag to capture image from camera
        self.fontColor = FONT_COLOR
        self.terminate = False  # Flag to terminate the get frame loop
        # Flag to identify whether show timestamp on picture.
        self.showTimestamp = False

    #-----------------------------------------------------------------------------
    def getOneFrame(self):
        """ An interface function for different type of camera to get one frame. the 
            return value need to be a cv2 image."""
        return None 
    
    def getFrames(self):
        """ Get frame one by one from camera based on the fps rate the children class 
            need to overwrite this function to add the detail function.
            Returns:
                _type_: Use yield to return byte video frame stream. None if video source 
                        is not available.
                Yields:
                    byte: Video bytes wrapped by html iframe to plug in ajax. 
        """
        while not self.terminate:
            if not self.capture:
                time.sleep(1.0/self.fpsNum)
                continue  # skip if the capture flag is false
            # capture one jpeg frame
            frame = self.getOneFrame()
            if frame is None:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                time.sleep(1.0/self.fpsNum)
                continue
            # Add the capture time stamp
            if self.showTimestamp: cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
                                                (10, 30), FONT_TYPE, FONT_SIZE, self.fontColor, thickness=1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
            time.sleep(1.0/self.fpsNum)
        # default no video image place holder return None
        return None
    
    #-----------------------------------------------------------------------------
    def setCaptureFlag(self, flag):
        self.capture = bool(flag)

    def setTextColor(self, color):
        self.fontColor = color

    def setShowTimestamp(self, flag):
        self.showTimestamp = bool(flag)

    def stop(self):
        self.terminate = True

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class camClientReal(camClient):
    """ Web video camera to fetch the video frame from a web-cam/live video 
        source then generate the motion jpeg video stream.
    """
    def __init__(self, videoSrc, fps=DEF_FPS):
        """ init example : camObj = cam.camClientReal(0)
            Args:
                videoSrc (int/str):
                    - for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
                    - for local webcam use integer 0, 1, 2, ... for multiple cameras
                fps (int, optional): video stream frame rate. Defaults to DEF_FPS.
        """
        super().__init__(fps)
        try:
            self.camera = cv2.VideoCapture(videoSrc) # use 0 for default web camera
            print("Linked to real camera src=%s" %str(videoSrc))
        except:
            print("Error: Can't open camera src=%s" %str(videoSrc))
            return None

    #-----------------------------------------------------------------------------
    def getOneFrame(self):
        success, frame = self.camera.read()  # read the camera frame
        return frame if success else None 
    
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class camClientSimu(camClient):
    """ Web video camera to fetch the file from an image data set in local folder 
        and generate the motion jpeg video stream.
    """
    def __init__(self, imageFolder, imageName, imageType='jpeg', fps=DEF_FPS):
        """ Init Example: camObj = cam.camClientSimu(os.path.dirname(os.path.abspath(__file__)), 'test-',fps=2)
            Args:
                imageFolder (str): Image folder path.
                imageName (str): Image name prefix.
                imageType (str, optional): Image name postfix. Defaults to 'jpeg'.
                fps (_type_, optional): video stream frame rate. Defaults to DEF_FPS.
        """
        super().__init__(fps)
        if not os.path.exists(imageFolder):
            print("Error: Image folder %s does not exist" %imageFolder)
            return None
        self.imgFolder = imageFolder
        self.imageName = imageName
        self.imageType = imageType
        self.showIndex = 0      # Current image index to show
        self.testMode = False   # Flag to identify auto loop all the image files in data set.

    #-----------------------------------------------------------------------------
    def getOneFrame(self):
        imageName = self.imageName+str(self.showIndex)+".%s" %str(self.imageType)
        imagePath = os.path.join(self.imgFolder, imageName)
        #print('get new image %s' %str(self.showIndex))
        if not os.path.exists(imagePath): return None
        frame = cv2.imread(imagePath)
        if self.testMode: self.showIndex = (self.showIndex + 1) % self.testMode
        return frame

    #-----------------------------------------------------------------------------
    def setTestMode(self, flag):
        self.testMode = int(flag)

    def setNextFrameIndex(self, index):
        self.showIndex = int(index)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class camClientScreen(camClient):
    """ Web video camera to fetch the video frame from a web-cam/live video 
        source then generate the motion jpeg video stream.
    """
    def __init__(self, region=None, fps=DEF_FPS):
        """ init example : camObj = cam.camClientScreen(0)
                region (tuple, optional): region=(x, y, width, height) to crop the video frame. 
                    Defaults to None. Example:(100, 100, 500, 500)
                fps (int, optional): video stream frame rate. Defaults to DEF_FPS.
        """
        super().__init__(fps)
        self.captureRegion = region

    #-----------------------------------------------------------------------------
    def getOneFrame(self):
        screenshot = pyautogui.screenshot() if self.captureRegion is None else pyautogui.screenshot(region=self.captureRegion)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return frame
   
    #-----------------------------------------------------------------------------
    def setCaptureRegion(self, region):
        self.captureRegion = region

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class camClientWinApp(camClient):
    """ Web video camera to fetch the video frame from another program's window
        and generate the motion jpeg video stream.This is a windows OS only feature.
        - Important: the window need to be at desktop (no need at top layer) but can 
            not be hide or minimized.
    """
    def __init__(self, windowName, fps=DEF_FPS):
        """ init example : camObj = cam.camClientProgram(0)
            Args:
                videoSrc (str): video source path. 
                fps (int, optional): video stream frame rate. Defaults to DEF_FPS.
        """
        super().__init__(fps)
        self.windowName = str(windowName)

    #-----------------------------------------------------------------------------
    def getOneFrame(self):
        # Find the window by its title
        hwnd = win32gui.FindWindow(None, self.windowName)
        if not hwnd:
            print("Error: Windows App GUI=[%s] not found" %self.windowName)
            return None 
        # Get window rect
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width, height = right - left, bottom - top
        # Get device contexts
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        # Create a compatible bitmap
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        # Copy window contents
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY) 
        #result = win32gui.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
        # Convert to PIL Image
        bmpinfo = saveBitMap.GetInfo()
        bmpstr  = saveBitMap.GetBitmapBits(True)
        #pilImg = Image.frombuffer(
        #     'RGB',
        #     (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        #     bmpstr, 'raw', 'BGRX', 0, 1
        #)
        #cv2Img = cv2.cvtColor(np.array(pilImg), cv2.COLOR_RGB2BGR)
        img = np.frombuffer(bmpstr, dtype=np.uint8)
        img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
        cv2Img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # Free resources
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        return cv2Img