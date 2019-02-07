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
import random
import datetime

# Play List, File Download Module
 # - Verion check
 # - Download

# URL_CDN = "http://150.95.156.112/etvapi.txt"
# URL_INFO = "info.php"
# URL_LIST = "list.php"
# URL_DETAIL = "detail.php"

URL_CDN = "http://cdn2.rhymeduck.com/etvapi.txt"
URL_INFO = "a/v1/member/info/"
URL_LIST = "a/v1/playlist/list"
URL_DETAIL = "a/v1/playlist/detail"

# INFO_TEST = {"result":{"ret":"success","msg":"member 정보가 전송되었습니다"},"data":{"event":[],"info":{"member_id":26165,"mac_num":2,"mac_address":null,"contract_state":1,"rand_play":1,"controlable":0,"type":1,"music_src":"?","cm_type":0,"service_ready":"","service_ready_start":"","service_ready_end":"","notice_id":0,"version_check":"0.000","expiration_date":"2017-10-11T16:38:50.000Z","auto_pay":3,"NOW()":"2017-11-21T05:38:07.000Z","enterprise_id":154,"member_info":"","name":"이랜드쥬얼리","phone":"1566-2864"},"servertime":"2017-11-21 14:38:07"}}
# LIST_TEST = {"result":{"ret":"success","msg":"playlist가 전송되었습니다"},"data":{"event":[],"list":[{"title":"영상방송테스트","playlist_id":3241,"mood":"","mod_ts":"2017-09-29 18:39:42","new_count":0,"new":false}]}}
# DETAIL_TEST = {"result":{"ret":"success","msg":"playlist의 music 목록이 전송되었습니다"},"data":{"event":[],"list":[{"music_id":5428727,"title":"Cheer up MV","artist_name":"twice","route":"http://cdn2.rhymeduck.com/video/18471.mp4","duration":"00:04:00"},{"music_id":5428728,"title":"miniskirt MV","artist_name":"AOA","route":"http://cdn2.rhymeduck.com/video/18472.mp4","duration":"00:03:41"},{"music_id":5428729,"title":"You and I MV","artist_name":"IU","route":"http://cdn2.rhymeduck.com/video/18473.mp4","duration":"00:08:54"},{"music_id":5428730,"title":"Like a Cat MV","artist_name":"AOA","route":"http://cdn2.rhymeduck.com/video/18474.mp4","duration":"00:05:26"}]}}


MEMBER_ID = 0
PLAYLIST_ID = 0
ROUTE = ""
HOST = "";

ID = "test_cosfa"
PASS = "12345"


BASE_PATH = "../"
# SERVER = "http://150.95.156.112/"

FILE_JSON = "play.json"
FILE_LIST_JSON = "list.json"
# FILE_MEMBER = "member.json"
# URL_PATH = SERVER + "movie/" + FILE_JSON
LOCAL_PATH = BASE_PATH + "movie/"
LOCAL_JSON = BASE_PATH + "job/" + FILE_JSON
LOCAL_LIST_JSON = BASE_PATH + "job/" + FILE_LIST_JSON

DEBUG = False
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/movie.log')

#Single Instance
fh=3
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


def executer(file):
    logd("executer", "executer "+ file)
    # os.system("python "+BASE_PATH+"job/"+file+" &")
    os.system("nohup python "+BASE_PATH+"job/"+file+" &")


def kill(file):
    logd("executer", "kill "+ file)
    # os.system("kill -9 ps -ef | grep '"+file+"' | grep python | awk '{print $2}' ")
    # os.system("ps aux | grep python | grep -v \"grep "+file+"\" | awk '{print $2}' | xargs kill -9")
    print("ps aux | grep  "+file+" | awk '{print $2}' | xargs kill -9")
    os.system("ps aux | grep  "+file+" | awk '{print $2}' | xargs kill -9")


#File Download
def download(path, url):
    filename = url.split('/')[-1]

    try:
        f = urllib2.urlopen(url, timeout = 30)
    except urllib2.URLError, e:
        logd("main", "timeout %r" % e)
        exit()

    logd( "download", "%s %sjob/%s/%s start" % ( url, BASE_PATH, path, filename ) );
    data = f.read()
    with open(BASE_PATH+"job/"+path + "/" + filename, "wb") as code:
        code.write(data)
    logd( "download", "%s %s/%s end" % ( url, path, filename ) );

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

    logd("req", res)
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

    logd("post", res)
    return res


def main():

    logd("main", "START");
    run_once()
    # mkdir()

    # randome host url
    res = req(URL_CDN)
    cdns = res.split("\n")
    cdns.pop()
    HOST = "http://%s/" %(random.choice(cdns))
    # print(HOST)

    data = {"id":ID, "password" : PASS}
    res = post(HOST + URL_INFO,data)
    info = json.loads(res)

    if info['result']['ret'] == "success" : 
        MEMBER_ID = info['data']['info']['member_id']
        contract_state = info['data']['info']['contract_state']
    else :
        return

    if MEMBER_ID <= 0 or contract_state <= 0 :
        exit()


    data = {'member_id':MEMBER_ID}
    res = post(HOST + URL_LIST,data)
    list = json.loads(res)
    if info['result']['ret'] == "success" : 
        PLAYLIST_ID = list['data']['list'][0]['playlist_id']
    else :
        return

    if PLAYLIST_ID <= 0 :
        exit()

    local_json = None 
    #Server Local Json
    if os.path.isfile( LOCAL_JSON )  == True:
        local_file=open(LOCAL_JSON, 'r')
        local_json=json.load(local_file)
        logd("main","local %s " % local_json)

    #Version 
    if local_json is None or PLAYLIST_ID > local_json['data']['list'][0]['playlist_id'] or list['data']['list'][0]['mod_ts'] > local_json['data']['list'][0]['mod_ts'] :

        data = {"playlist_id":PLAYLIST_ID}
        res = post(HOST + URL_DETAIL,data)

        # print (res)
        detail = json.loads(res)
        if detail['result']['ret'] == "success" : 
            play_list = detail['data']['list']


        #make directory
        logd("main","--Make Directory--")

        mod_ts = list['data']['list'][0]['mod_ts']
        date_mod_ts = datetime.datetime.strptime(mod_ts, '%Y-%m-%d %H:%M:%S')
        str_mod_ts = date_mod_ts.strftime('%Y%m%d%H%M%S')

        directory_name = LOCAL_PATH + str( PLAYLIST_ID )+"_"+str_mod_ts
        if os.path.isdir(directory_name) == True :
            shutil.rmtree(directory_name)
        os.mkdir( directory_name , 0755 );

        #Download
        logd("main","--Download--")
        for item in play_list:
            logd("main",item)
            download( directory_name , item['route'] )

        # #file copy
        # logd("main","--File Copy--")
        # for item in data.get('list'):
        #     logd("main",item)
        #     file =  item.split('/')[-1]
        #     logd("main",directory_name + file)
        #     logd("main",file)
        #     shutil.copyfile( directory_name +"/"+ file,  file)

        #Save Last Version
        logd("main","--Save--")
        output_file=open( LOCAL_JSON, 'w')
        json.dump(list, output_file)
        output_file.close() 

        logd("main","--Save--")
        output_file=open( LOCAL_LIST_JSON, 'w')
        json.dump(detail, output_file)
        output_file.close() 

        kill("player.py")
        kill("player_cm.py")
        kill("omxplayer")
        executer("player.py")

    else :
        return

    logd("main", "END");

if __name__ == "__main__":
    main()

