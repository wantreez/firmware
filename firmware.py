#-*- coding: utf-8 -*-
from subprocess import Popen, call, PIPE
import errno
from types import *
import logging
import os, sys
import time
import urllib, json
import urllib2
import shutil
import fcntl
import socket
import tarfile
import random


# Firmware Download Module
# - Version Check
# - Firmware Download
# - Firmware tar gzip Extract
# - Version upload


BASE_PATH = "../"
# SERVER = "http://150.95.156.112/"

URL_CDN = "http://cdn2.rhymeduck.com/etvapi.txt"
URL_INFO = "a/v1/member/info/"
URL_VERSION_UPDATE = "a/v1/member/update"
URL_VERSION_INFO = "a/v1/member/linux_update_info"

FILE_MEMBER = "member.json"

# URL_PATH = SERVER + "firmware/" + FILE_JSON
LOCAL_PATH = BASE_PATH + "firmware/"
LOCAL_JOB_PATH = BASE_PATH + "job/"
LOCAL_JSON = BASE_PATH + "job/" + FILE_MEMBER

ID = "test_cosfa"
PASS = "12345"

DEBUG = True
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/firmware.log',
                    filemode='w')

# {"result":{"ret":"success","msg":"리눅스 플레이어의 버전이 전송되었습니다"},"data":{"event":[],"url":"http://4497.co.kr/settop/20.02.tgz","servertime":"2017-11-22 22:21:01"}}
# {"result":{"ret":"success","msg":"member 정보를 업데이트하였습니다"},"data":{"event":[],"servertime":"2017-11-22 22:20:00"}}



#Single Instance
fh=1
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

#Log Function
def logd(tag, msg):
    localtime   = time.localtime()
    timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
    logging.debug("[%s][%s][%s]" %(timeString,tag,msg) )
    if DEBUG :
        print("[%s][%s][%s]" %(timeString,tag,msg) )


#File Download
def download(path, url):
    filename = url.split('/')[-1]
    
    try:
        f = urllib2.urlopen(url, timeout = 1)
    except urllib2.URLError, e:
        logd("main", "timeout %r" % e)
        exit()

    logd( "download", "%s %sjob/%s/%s" % ( url, BASE_PATH, path, filename ) );
    data = f.read()
    with open(BASE_PATH+"job/"+path + "/" + filename, "wb") as code:
        code.write(data)


def req(url):
    #Server Json Download :
    try:
        logd("req", url);
        response = urllib2.urlopen(url, timeout = 30)
    except urllib2.URLError, e:
        logd("main", "timeout %r" % e)
        exit()

    res = response.read()
    
    #Server Json Fail
    if response.getcode() != 200 :
        logd("main","URL Fail : "+str(response.getcode()))
        exit()

    print res
    return res


def post(url, data):
    #Server Json Download :
    print data
    try:
        data = urllib.urlencode(data)
        logd("post", url);
        response = urllib2.urlopen(url,data, timeout = 30)
    except urllib2.URLError, e:
        logd("post", "timeout %r" % e)
        exit()

    res = response.read()
    
    #Server Json Fail
    if response.getcode() != 200 :
        logd("main","URL Fail : "+str(response.getcode()))
        exit()

    print res
    return res

def main():

    logd("main", "START");
    # run_once()
    # mkdir()

    # get host url
    res = req(URL_CDN)
    cdns = res.split("\n")
    cdns.pop()
    HOST = "http://%s/" %(random.choice(cdns))

    data = {"id":ID, "password" : PASS}
    res = post(HOST + URL_INFO,data)
    member_json = json.loads(res)

    if member_json['result']['ret'] == "success" : 
        MEMBER_ID = member_json['data']['info']['member_id']
        contract_state = member_json['data']['info']['contract_state']
    else :
        return

    if MEMBER_ID <= 0 or contract_state <= 0 :
        exit()

    local_json = None 
    if os.path.isfile( LOCAL_JSON )  == True:
        local_file=open(LOCAL_JSON, 'r')
        local_json=json.load(local_file)
        logd("main","local %s " % local_json)

    #Version Check 
    if local_json is None or float(member_json['data']['info']['version_check']) > float(local_json['data']['info']['version_check']) :

        VERSION = member_json['data']['info']['version_check']
        #UPDATE INFO
        data = {'member_id':MEMBER_ID, "version": VERSION }
        res = post(HOST + URL_VERSION_INFO,data)
        info = json.loads(res)

        if info['result']['ret'] == "success" : 

            #make directory
            logd("main","--Make Directory--")
            directory_name = LOCAL_PATH + str( VERSION )
            if os.path.isdir(directory_name) == True :
                shutil.rmtree(directory_name)
            os.mkdir( directory_name , 0755 );


            #Downalod Firmware
            url = info['data']['url']
            logd("main","--Download--")
            download( directory_name , url)

            file =  url.split('/')[-1]
            logd("main",directory_name +"/"+ file)
            logd("main",file)

            tar = tarfile.open(directory_name +"/"+ file)
            tar.extractall(path=LOCAL_JOB_PATH )
            tar.close()

            # shutil.copyfile( directory_name +"/"+ file,  file)

            #UPDATE INFO
            data = {'member_id':MEMBER_ID, "version": VERSION }
            res = post(HOST + URL_VERSION_UPDATE,data)
            info = json.loads(res)

            if info['result']['ret'] == "success" : 

                #Save Last Version
                logd("main","--Save--")
                output_file=open( LOCAL_JSON, 'w')
                json.dump(member_json, output_file)
                output_file.close() 

        else :
            return

    logd("main", "END");

if __name__ == "__main__":
    main()

