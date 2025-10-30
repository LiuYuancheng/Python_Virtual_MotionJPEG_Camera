#------------------------------------------------------------------------------
# Name:        webCamApp.py
#
# Purpose:     A Flask IoT virtual Motion-JPEG camera simulation program with a 
#              web page interface, it can load the video source from real camera, 
#              pre-saved video files or screen capture.
#
# Author:      Yuancheng Liu
#
# Created:     2025/10/15 
# version:     v_0.0.2
# Copyright:   Copyright (c) 2025 LiuYuancheng
# License:     MIT License
#------------------------------------------------------------------------------

from datetime import timedelta

import cv2
import secrets
# import flask module to create the server.
from flask import Flask, Response, render_template, flash, url_for, redirect, request
from flask_login import LoginManager, login_required

import webCamGlobal as gv
import virtualCamera as cam
import webCamAuth
#import webCamDataMgr

# -----------------------------------------------------------------------------
# Init the flask web app program.
def createApp():
    """ Create the flask App."""
    # init the web host
    app = Flask(__name__)
    app.config['SECRET_KEY'] = gv.APP_SEC_KEY
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=gv.COOKIE_TIME)
    app.config['TOKENS'] = {'fixed': gv.gflaskToken}
    from webCamAuth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # Create the user login manager
    loginMgr = LoginManager()
    loginMgr.loginview = 'auth.login'
    loginMgr.init_app(app)
    @loginMgr.user_loader
    def loadUser(userID):
        return webCamAuth.User(userID)
    return app

# -----------------------------------------------------------------------------
# Init the user manager
gv.iUserMgr = webCamAuth.userMgr(gv.gUsersRcd)
# use real camera
if gv.gCamMode == 0:
    gv.iCamMgr = cam.camClientReal(gv.gCamSrc, fps=gv.gCamFps)
elif gv.gCamMode == 1:
    gv.iCamMgr = cam.camClientSimu(gv.gCamDir, gv.gCamFilePrefix, fps=gv.gCamFps)
    gv.iCamMgr.setShowTimestamp(True)
    gv.iCamMgr.setTestMode(56)
elif gv.gCamMode == 2:
    gv.iCamMgr = cam.camClientScreen(fps=gv.gCamFps)
else:
    windowName = "templates - File Explorer"
    windowName = "2D Airport CAT-II Runway Light System Simulation"
    camObj = cam.camClientWinApp(windowName)

app = createApp()

# -----------------------------------------------------------------------------
# page 0: index page
@app.route('/')
@app.route('/index')
def index():
    # page index is used to highlight the left page slide bar.
    posts = {'page': 0}
    if gv.iCamMgr:
        gv.iCamMgr.setCaptureFlag(False)
    return render_template('index.html', posts=posts)

# -----------------------------------------------------------------------------
@app.route('/liveview')
@login_required
def liveview():
    posts = {'page': 1,
             'users': gv.iUserMgr.getUserInfo(),
             'src': 'video_feed'
             }
    if gv.iCamMgr:
        gv.iCamMgr.setCaptureFlag(True)
    return render_template('liveview.html', posts=posts)

@app.route('/video_feed')
def video_feed():
    if gv.iCamMgr:
        #Video streaming route. Put this in the src attribute of an img tag
        return Response(gv.iCamMgr.getFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(None, mimetype='multipart/x-mixed-replace; boundary=frame')

# -----------------------------------------------------------------------------
# page 3 admin user account's request handling function.
@app.route('/accmgmt')
@login_required
def accmgmt():
    posts = {'page': 3,
             'users': gv.iUserMgr.getUserInfo()
            }
    if gv.iCamMgr:gv.iCamMgr.setCaptureFlag(False)
    return render_template('accmgmt.html', posts=posts)

@app.route('/accmgmt/<string:username>/<string:action>', methods=('POST',))
@login_required
def changeAcc(username, action):
    """ Handle the user account's POST request.
        Args:
            username (str): user name string
            action (str): action tag.
    """
    if action == 'delete':
        if gv.iUserMgr.removeUser(str(username).strip()):
            flash('User [ %s ] has been deleted.' % str(username))
        else:
            flash('User not found.')
    return redirect(url_for('accmgmt'))

@app.route('/addnewuser', methods=['POST', ])
@login_required
def addnewuser():
    """ Addd a new user in the IoT system."""
    if request.method == 'POST':
        tgttype = request.form.getlist('optradio')
        tgtUser = request.form.get("username")
        tgtPwd = request.form.get("password")
        # print((tgttype, tgtUser, tgtPwd))
        if not gv.iUserMgr.userExist(tgtUser):
            userType = 'admin' if 'option1' in tgttype else 'user'
            if gv.iUserMgr.addUser(tgtUser, tgtPwd, userType):
                flash('User [ %s ] has been added.' % str(tgtUser))
            else:
                flash('User [ %s ] can not be added.' % str(tgtUser))
        else:
            flash('User [ %s ] has been exist.' % str(tgtUser))
    return redirect(url_for('accmgmt'))

@app.route('/setpassword/<string:username>', methods=['POST', ])
@login_required
def setpassword(username):
    """ Update the user password."""
    if request.method == 'POST':
        newPassword = str(request.form.get("newpassword")).strip()
        if newPassword:
            rst = gv.iUserMgr.updatePwd(username, newPassword)
            if rst:
                flash('Password of user [ %s ] has been changed.' % str(username))
            else:
                flash('Password of user [ %s ] can not be changed.' % str(username))
        else:
            flash('Password can not be empty.')
    return redirect(url_for('accmgmt'))

#-----------------------------------------------------------------------------
@app.route('/cgi-bin/mjpg/<string:token>', methods=['GET','POST'])
def transfer_image(token):
    """ Handle file upload from web UI."""
    if token in app.config['TOKENS'].values():
        cv2Frame = gv.iCamMgr.getOneFrame()
        if cv2Frame is not None:
            ret, buffer = cv2.imencode('.jpg', cv2Frame)
            response = Response(buffer.tobytes(), mimetype='image/jpeg')
            response.headers['Content-Disposition'] = 'attachment; filename=flask_image.jpg'
            return response
    return "404 Image Not Found"

#-----------------------------------------------------------------------------
@app.route('/accconfig')
@login_required
def accconfig():
    posts = {'page': 2,
             'tokens': app.config['TOKENS']
            }
    return render_template('accconfig.html', posts=posts)

@app.route('/temptoken/<string:action>', methods=['POST', ])
@login_required
def temp_token(action):
    """ For handling temporary token"""
    if action == 'generate':
        temp_token = secrets.token_hex(16)
        app.config['TOKENS']['temp'] = temp_token
    elif action == 'delete':
        del app.config['TOKENS']['temp']
    return redirect(url_for('accconfig'))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host=gv.gflaskHost, port=gv.gflaskPort, debug=gv.gflaskDebug, threaded=gv.gflaskMultiTH)
