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
import datetime


# Play List Play Module
 # - Play List play


BASE_PATH = "../"

FILE_JSON = "play.json"
FILE_LIST_JSON = "list.json"
FILE_STATUS_JSON = "status.json"
# FILE_MEMBER = "member.json"
# URL_PATH = SERVER + "movie/" + FILE_JSON
LOCAL_PATH = BASE_PATH + "movie/"
LOCAL_JSON = BASE_PATH + "job/" + FILE_JSON
LOCAL_LIST_JSON = BASE_PATH + "job/" + FILE_LIST_JSON
LOCAL_STATUS_JSON = BASE_PATH + "job/" + FILE_STATUS_JSON


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/player.log')

#Single Instance
fh=8
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
    #print "[%s][%s][%s]" %(tag,localtime,msg) 

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
    # kill("player.py")
    kill("omxplayer")


    while True:
        if os.path.isfile( LOCAL_JSON )  == False and  os.path.isfile( LOCAL_LIST_JSON )  == False:
            logd("main", " no json sleep 10")
            time.sleep(10)
            # executeDownloader()
            continue


        local_file=open(LOCAL_JSON, 'r')
        local_json=json.load(local_file)
        logd("main","local %s " % local_json)
        PLAYLIST_ID = local_json['data']['list'][0]['playlist_id']
        mod_ts = local_json['data']['list'][0]['mod_ts']

        input_file=open(LOCAL_LIST_JSON, 'r')
        local_json=json.load(input_file)
        play_list = local_json['data']['list']

        status_json = None
        last =0
        if os.path.isfile( LOCAL_STATUS_JSON )  == True:

            input_file=open(LOCAL_STATUS_JSON, 'r')
            status_json=json.load(input_file)
            last = status_json["last"]
            last = last + 1
            if last >= len(play_list):
                last = 0
            print    status_json

        print "play start  "+str(last)
        # for for i in range(len(play_list)):
        for i in range (last,len(play_list)) :

            item = play_list[i]
            logd("main",item)

            logd("main","--Save--")
            output_file=open( LOCAL_STATUS_JSON, 'w')
            json.dump({"last":i}, output_file)
            output_file.close() 

            date_mod_ts = datetime.datetime.strptime(mod_ts, '%Y-%m-%d %H:%M:%S')
            str_mod_ts = date_mod_ts.strftime('%Y%m%d%H%M%S')
            directory_name = LOCAL_PATH + str( PLAYLIST_ID )+"_"+str_mod_ts
            print directory_name

            if os.path.isdir(directory_name) == True :
                url = item['route']
                filename = url.split('/')[-1]
                
                # print directory_name+"/"+filename
                # Play
                if os.path.isfile( directory_name+"/"+filename )  == True  :
                    logd("main", "omxplayer %s" % (directory_name+"/"+filename) )
                    subprocess.call("omxplayer %s" % (directory_name+"/"+filename), shell=True)
            else :
                break

if __name__ == "__main__":
    main()


