#-----------------------------------------------------------------------------
# Name:        webCamDataMgr.py
#
# Purpose:     Data manager module for connect to the physical world to fetch 
#              the plan position data.
#              
# Author:      Yuancheng Liu, Foo Shi Wan
#
# Created:     2025/10/15
# version:     v_0.1.5
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import time
import threading
import webCamGlobal as gv
import physicalWorldComm

CAM_REQ_KEY = 'CAM_REQ_KEY'
CAM_ID_KEY = 'CAM_ID'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class CamDataMgr(threading.Thread):
    """ Data manager module for connect to the physical world to fetch the plane 
        position data and set the 
    """
    def __init__(self, cameraID, physicalWorldAddr):
        threading.Thread.__init__(self)
        self.cameraID = str(cameraID).strip()
        self.terminate = False
        self.pwConnector = physicalWorldComm.PhysicalWorldConnector(self, physicalWorldAddr, 
                                                                    deviceID=self.cameraID,
                                                                    reconnectCount=gv.gRW_RECONN_TIME)
        gv.gDebugPrint('Data manager init finished', logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def getRWInputInfo(self):
        """ Get sensors state from the physical world simulator app. """
        requestDict = {CAM_ID_KEY : self.cameraID}
        result = self.pwConnector.getPWItemData(requestType=CAM_REQ_KEY, dataDict=requestDict)
        return result

    #-----------------------------------------------------------------------------
    def run(self):
        time.sleep(1) # sleep 1 sec to wait the flask app start to host web cam web.
        while not self.terminate:
            cameraInfo = self.getRWInputInfo()
            if cameraInfo is None: return
            print(cameraInfo)
            _, _, frameDict = cameraInfo
            frameVal = max(0, frameDict['result']) # if return negative value, set to 0.
            frameIdx = int(gv.gCamDataIdxStart + (gv.gCamDataIdxEnd - gv.gCamDataIdxStart) * frameVal)
            if gv.iCamMgr: gv.iCamMgr.setNextFrameIndex(frameIdx)
            time.sleep(gv.gRW_REF_TIME)
