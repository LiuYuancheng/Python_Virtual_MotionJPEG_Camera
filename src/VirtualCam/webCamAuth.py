#-----------------------------------------------------------------------------
# Name:        railwayWebAuth.py
#
# Purpose:     User authorization and management module used for handling the 
#              website user create, update, login and logout request.
#              
# Author:      Yuancheng Liu
#
# Created:     2025/10/15
# version:     v_0.1.5
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, UserMixin

import webCamGlobal as gv
from ConfigLoader import JsonLoader

auth = Blueprint('auth', __name__)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class userMgr(JsonLoader):
    """ User information manager module to handle add user, delete user, update 
        user, query user information. It is a child module inherted from  
        ConfigLoader.JsonLoader
    """
    
    def __init__(self, userRcd):
        """ userMgr class constructor. Init example mgr = userMgr("user.json")
            Args:
                userRcd (str): user record json file path.
        """
        super().__init__()
        self.loadFile(userRcd)

    # -----------------------------------------------------------------------------
    # user check function.
    def userExist(self, userID):
        if not self._haveData(): return False
        if userID in self.jsonData.keys(): return True
        return False

    def verifyUser(self, userName, userPwd):
        if self.userExist(userName):
            return self.jsonData[str(userName)]['password'] == userPwd
        return False
    
    # -----------------------------------------------------------------------------
    # Get() function
    def getUserInfo(self):
        if self._haveData():
            return self.getJsonData().values()
        return []

    # -----------------------------------------------------------------------------
    # user create, update and delete function.
    def addUser(self, userName, userPwd, userType, updateRcd=True):
        userName = str(userName).strip()
        if not self._haveData(): return False 
        if self.userExist(userName): return False
        data = {
            "username": str(userName),
            "password": str(userPwd),
            "usertype": str(userType)
        }
        self.jsonData[userName] = data
        if updateRcd: self.updateRcdFile()
        return True
    
    def updatePwd(self, userName, newPwd, updateRcd=True) :
        if self.userExist(userName):
            self.jsonData[userName]['password'] = str(newPwd)
            if updateRcd: self.updateRcdFile()
            return True 
        return False

    def removeUser(self, userName, updateRcd=True):
        print(userName)
        if self.userExist(userName):
            self.jsonData.pop(userName)
            if updateRcd: self.updateRcdFile()
            return True            
        return False
    
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class User(UserMixin):
    """ User object used to get the user info from backend during init.
        Args:
            UserMixin (_type_): _description_
    """
    def __init__(self, id):
        self.id = id
        self.name = id
        self.type = 'user'
        self.password = None

    def __repr__(self):
        return "%d/%s/%s" % (self.name, self.type, self.password)

#-----------------------------------------------------------------------------
# Handle login request.
"""
@auth.route('/login')
def login():
    return render_template('login.html')
"""
@auth.route('/login', methods=['POST'])
def login_post():
    account = request.form.get('account')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    print((account, password))
    if gv.iUserMgr.userExist(account):
        if gv.iUserMgr.verifyUser(str(account), str(password)):
            login_user(User(account), remember=remember)
            gv.gDebugPrint("User login detected: [account: %s, password: %s]" %(account,password),logType=gv.LOG_INFO)
            return redirect(url_for('index'))
        else:
            flash('User password incorrect!')
            gv.gDebugPrint("User login failed: [account: %s, password: %s]" %(account,password),logType=gv.LOG_INFO)
    else:
        flash('Login user does not exit!')
        gv.gDebugPrint("User does not exist: [account: %s, password: %s]" %(account,password),logType=gv.LOG_INFO)
    return redirect(url_for('auth.login'))

#-----------------------------------------------------------------------------
# Handle logout request.
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
