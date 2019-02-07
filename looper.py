import time
from threading import Timer
import logging
import os, sys
import datetime
import urllib, json
import subprocess

# Looper Timer Module
# - 10 sec, 10min check
# - 10 sec : CM List Time check
# - 10 min : Play List, CM List check


INTERVAL_MIN = 10
INTERVAL_10MIN = 60*10

BASE_PATH = "../"

FILE_JSON = "cm.json"
# URL_PATH = SERVER + "movie/" + FILE_JSON
LOCAL_PATH = BASE_PATH + "cm/"
LOCAL_JSON = BASE_PATH + "job/" + FILE_JSON


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/looper.log')


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

def check(file):
    logd("executer", "kill "+ file)
    print("ps aux | grep  "+file+" | awk '{print $2}' ")
    os.system("ps aux | grep  "+file+" | awk '{print $2}'")


def logd(tag, msg):
    #localtime = time.localtime(time.time())
    localtime   = time.localtime()
    timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
    logging.debug("[%s][%s][%s]" %(tag,timeString,msg) )




def do1min():
    print "do1min Time:", time.time()
    Timer(INTERVAL_MIN, do1min, ()).start()

    #Server Local Json
    local_json = None
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
            # timeString  = time.strftime("00:20:00", localtime)

            for item in cm_list:
                logd("main",item)
                url = item['route']
                item_time = item['time']
                filename = url.split('/')[-1]

                print directory_name+"/"+filename
                print timeString+"/"+item_time

                # timeString= "00:10:00"
                if os.path.isfile( directory_name+"/"+filename )  == True and timeString == item_time :
                    kill("player.py")
                    kill("player_cm.py")
                    # kill("omxplayer")
                    print( " excuter plyer_cm.py")
                    executer("player_cm.py")
                    break




def do10min():
	print "do10min Time:", time.time()
	Timer(INTERVAL_10MIN, do10min, ()).start()
	print("----------wanteez-----")
	executer("movie_wantreez.py")
	print("----------cm-----")
	executer("movie_cm.py")

	localtime  = time.localtime()

	print(time.strftime("%M", localtime))
	print(time.strftime("%M", localtime)[0])
	if(time.strftime("%M", localtime)[0] == "0") :
		print(time.strftime("%M", localtime)[0])




def main():
	print "looper start:", time.time()
	Timer(INTERVAL_MIN, do1min, ()).start()
	Timer(INTERVAL_10MIN, do10min, ()).start()

if __name__ == "__main__":
    main()
