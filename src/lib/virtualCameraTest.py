
#------------------------------------------------------------------------------
# Name:        virtualCameraTest.py
#
# Purpose:     This module is the test case module for the motion JPEG streaming
#              camera <virtualCamera.py>
#
# Author:      Yuancheng Liu
#
# Created:     2025/10/15 
# version:     v_0.0.1
# Copyright:   Copyright (c) 2025 LiuYuancheng
# License:     GNU General Public License V3
#------------------------------------------------------------------------------

import os
from flask import Flask, Response, render_template
import virtualCamera as cam

#-----------------------------------------------------------------------------
print("Run the web virtual camera module with video source:\n\
    \t (0) Real stream from camera \n\
    \t (1) Image data set in folder\n\
    \t (2) Screen capture\n\
    \t (3) exit")
testCase = int(input('Input your choice:'))

#-----------------------------------------------------------------------------
camObj = None 
if testCase == 0:
    camObj = cam.camClientReal(0)
elif testCase == 1:
    dirpath = os.path.dirname(os.path.abspath(__file__))
    imgDir = os.path.join(dirpath, 'templates')
    camObj = cam.camClientSimu(imgDir, 'test-',fps=2)
elif testCase == 2:
    camObj = cam.camClientScreen()
elif testCase == 3:
    exit()

print("[o] Enable the timestamp on the image")    
camObj.setShowTimestamp(True)

#-----------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    """ route to introduction index page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(camObj.getFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)