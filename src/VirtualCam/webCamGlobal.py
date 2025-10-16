#-----------------------------------------------------------------------------
# Name:        railwayWebGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2025/01/21
# version:     v_0.0.1
# Copyright:   Copyright (c) 2025 LiuYuancheng
# License:     MIT License   
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os
import sys

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)
APP_NAME = ('WebCam', 'OpRoom')

TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)

#-----------------------------------------------------------------------------
# Init the logger
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100,
               fPutLogsUnderDate=True)
# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3

def gDebugPrint(msg, prt=True, logType=None):
    if prt: print(msg)
    if logType == LOG_WARN:
        Log.warning(msg)
    elif logType == LOG_ERR:
        Log.error(msg)
    elif logType == LOG_EXCEPT:
        Log.exception(msg)
    elif logType == LOG_INFO or DEBUG_FLG:
        Log.info(msg)

#-----------------------------------------------------------------------------
# load the config file.
import ConfigLoader
CONFIG_FILE_NAME = 'Config.txt'
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()

APP_SEC_KEY = 'Temporary_secret_key' 
COOKIE_TIME = 30

gUsersRcd = os.path.join(dirpath, CONFIG_DICT['USERS_RCD'])

#-------<GLOBAL VARIABLES (start with "g")>-------------------------------------
gCamMode = int(CONFIG_DICT['CAM_MD'])
# camera to real world connection parameters
gCamID = CONFIG_DICT['CAM_ID']
gRW_IP = CONFIG_DICT['RW_IP']
gRW_PORT = int(CONFIG_DICT['RW_PORT'])
gRW_REF_TIME = float(CONFIG_DICT['RW_REFRESH_TIME'])
gRW_RECONN_TIME = int(CONFIG_DICT['RW_RECONN_TIME'])

# camera config parameters
gCamSrc = int(CONFIG_DICT['CAM_IDX']) if 'CAM_IDX' in CONFIG_DICT.keys() else 0
gCamFps = int(CONFIG_DICT['CAM_FPS']) if 'CAM_FPS' in CONFIG_DICT.keys() else 10
gCamDir = os.path.join(dirpath, 'static', 'images', CONFIG_DICT['CAM_DATA_DIR'])
gCamFilePrefix = str(CONFIG_DICT['CAM_DATA_PREFIX']).strip()
gCamDataIdxStart = int(CONFIG_DICT['CAM_DATA_START_IDX']) if 'CAM_DATA_START_IDX' in CONFIG_DICT.keys() else 0
gCamDataIdxEnd = int(CONFIG_DICT['CAM_DATA_END_IDX']) if 'CAM_DATA_END_IDX' in CONFIG_DICT.keys() else 1

# Flask App parameters : 
gflaskHost = '0.0.0.0'
gflaskPort = int(CONFIG_DICT['FLASK_SER_PORT']) if 'FLASK_SER_PORT' in CONFIG_DICT.keys() else 5000
gflaskDebug = CONFIG_DICT['FLASK_DEBUG_MD']
gflaskMultiTH =  CONFIG_DICT['FLASK_MULTI_TH']

#-------<GLOBAL INSTANCES>-----------------------------------------------------
iUserMgr = None 
iDataMgr = None
iCamMgr = None
iDataMgr = None
