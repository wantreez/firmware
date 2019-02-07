from subprocess import Popen, call, PIPE
import errno
from types import *
import logging
import os, sys
import time
import urllib, json
import shutil
import shlex
import subprocess
import time

# CM List Play Module
 # - CM List play


BASE_PATH = "../"

FILE_JSON = "cm.json"
# URL_PATH = SERVER + "movie/" + FILE_JSON
LOCAL_PATH = BASE_PATH + "cm/"
LOCAL_JSON = BASE_PATH + "job/" + FILE_JSON


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/player_cm.log')


#Single Instance
fh=12
def run_once():
    global fh
    logd("run_once", __file__)
    fh=open(os.path.realpath(__file__),'r')
    try:
        logd("run_once", "RUN")
        fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except:
        logd("run_once", "fexit")
        os._exit(0)
        

def logd(tag, msg):
    #localtime = time.localtime(time.time())
    localtime   = time.localtime()
    timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
    logging.debug("[%s][%s][%s]" %(tag,timeString,msg) )
    print "[%s][%s][%s]" %(tag,localtime,msg) 

def executer(file):
    logd("executer", "executer "+ file)
    # os.system("python "+BASE_PATH+"job/"+file+" &")
    os.system("nohup python "+BASE_PATH+"job/"+file+" &")

def kill(file):
    logd("executer", "kill "+ file)
    # os.system("kill -9 ps -ef | grep '"+file+"' | grep python | awk '{print $2}' ")
    # print("ps aux | grep python | grep -v \"grep "+file+"\" | awk '{print $2}' | xargs kill -9")
    # os.system("ps aux | grep python | grep -v \"grep "+file+"\" | awk '{print $2}' | xargs kill -9")
    print("ps aux | grep  "+file+" | awk '{print $2}' | xargs kill -9")
    os.system("ps aux | grep  "+file+" | awk '{print $2}' | xargs kill -9")


def main():
    logd("main", __file__)
    # run_once()

    local_json = None 
    #Server Local Json
    if os.path.isfile( LOCAL_JSON )  == True:
        local_file=open(LOCAL_JSON, 'r')
        local_json=json.load(local_file)
        logd("main","local %s " % local_json)


    TODAY = local_json["date"]
    directory_name = LOCAL_PATH + TODAY
    if os.path.isdir(directory_name) == True :
            cm_list = local_json['data']['list']
            localtime   = time.localtime()
            # timeString  = time.strftime("%H:%M:%S", localtime)
            # timeString  = time.strftime("00:%M:%S", localtime)
            timeString  = time.strftime("%H:%M:00", localtime)

            for item in cm_list:
                logd("main",item)
                url = item['route']
                item_time = item['time']
                filename = url.split('/')[-1]

                print directory_name+"/"+filename

                print timeString
                print item_time

                if os.path.isfile( directory_name+"/"+filename )  == True and timeString == item_time :
                    print ""

                    logd("main", "omxplayer %s" % (directory_name+"/"+filename) )
                    print("main", "cm omxplayer %s" % (directory_name+"/"+filename) )
                    subprocess.call("omxplayer %s" % (directory_name+"/"+filename), shell=True)
                    break
                    
    # kill("player.py")
    # kill("player_cm.py")
    # kill("omxplayer")
    # sleep(1)
    executer("player.py")
    exit()

if __name__ == "__main__":
    main()


