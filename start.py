#-*- coding: utf-8 -*-
from subprocess import Popen, call, PIPE
import logging
import os, sys
import firmware
import looper
import time
import urllib, json
import shutil
import datetime
import time


# Device Boot Start Module
# - Remove Files ( Play list, CM list, Firmware )
# - Firmware update start
# - Start Play List
# - Start Looper


BASE_PATH = "../"
DEBUG = False
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/start.log')

#Single Instance
fh=0
def run_once():
    global fh
    logd("run_once", __file__)
    fh=open(os.path.realpath(__file__),'r')
    try:
        logd("run_once", "RUN")
        fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except:
        logd("run_once", "EXIT")
        os._exit(0)


def executer(file):
    logd("executer", "executer "+ file)
    # os.system("python "+BASE_PATH+"job/"+file+" &")
    os.system("nohup python "+BASE_PATH+"job/"+file+" &")

#Log Function
def logd(tag, msg):
    localtime   = time.localtime()
    timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
    logging.debug("[%s][%s][%s]" %(timeString,tag,msg) )
    if DEBUG :
        print("[%s][%s][%s]" %(timeString,tag,msg) )


FILE_CM_JSON = "cm.json"
LOCAL_CM_JSON = BASE_PATH + "job/" + FILE_CM_JSON
PATH_CM = BASE_PATH + "cm/"
FILE_PLAY_JSON = "play.json"
LOCAL_PLAY_JSON = BASE_PATH + "job/" + FILE_PLAY_JSON
PATH_PLAY = BASE_PATH + "movie/"
FILE_FIRMWARE_JSON = "member.json"
LOCAL_FIRMWARE_JSON = BASE_PATH + "job/" + FILE_FIRMWARE_JSON
PATH_FIRMWARE = BASE_PATH + "firmware/"

def removeFileHistory(path, version):
    for file_object in os.listdir(path):
        if version != file_object :
            print file_object
            file_object_path = os.path.join(path, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

def removeSystems():
        #file remove
    local_json = None 
    #Server Local Json
    if os.path.isfile( FILE_CM_JSON )  == True:
        local_file=open(FILE_CM_JSON, 'r')
        local_json=json.load(local_file)
        removeFileHistory(PATH_CM, local_json['date'])

    if os.path.isfile( FILE_PLAY_JSON )  == True:
        local_file=open(FILE_PLAY_JSON, 'r')
        local_json=json.load(local_file)

        mod_ts = local_json['data']['list'][0]['mod_ts']
        date_mod_ts = datetime.datetime.strptime(mod_ts, '%Y-%m-%d %H:%M:%S')
        str_mod_ts = date_mod_ts.strftime('%Y%m%d%H%M%S')

        removeFileHistory(PATH_PLAY, str(local_json['data']['list'][0]['playlist_id'])+"_"+str_mod_ts)

    if os.path.isfile( FILE_FIRMWARE_JSON )  == True:
        local_file=open(FILE_FIRMWARE_JSON, 'r')
        local_json=json.load(local_file)
        removeFileHistory(PATH_FIRMWARE, local_json['data']['info']['version_check'])

def main():
    logd("main", "START");

    try:
        removeSystems()
        # TODAY = datetime.date.today().strftime('%Y-%m-%d')

        # Network connection
        time.sleep(5)
        
        # # run_once()
        firmware.main()
        executer("player.py")
        looper.main()
    except:
        e = sys.exc_info()[0]
        # write_to_page( "<p>Error: %s</p>" % e )
        logd("error", e);


    logd("main", "END");

if __name__ == "__main__":
    main()

