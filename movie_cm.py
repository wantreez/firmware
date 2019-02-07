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

# CM List, File Download Module
 # - Verion check
 # - Download

# URL_CDN = "http://150.95.156.112/etvapi.txt"
# URL_INFO = "info.php"
# URL_LIST = "cm_list.php"

URL_CDN = "http://cdn2.rhymeduck.com/etvapi.txt"
URL_INFO = "a/v1/member/info/"
URL_LIST = "a/v1/cm/list"

# INFO_TEST {"result":{"ret":"success","msg":"member 정보가 전송되었습니다"},"data":{"event":[],"info":{"member_id":26152,"mac_num":2,"mac_address":null,"contract_state":1,"rand_play":1,"controlable":1,"type":0,"music_src":"?","cm_type":0,"service_ready":"","service_ready_start":"","service_ready_end":"","notice_id":0,"version_check":"0.000","expiration_date":"0000-00-00 00:00:00","auto_pay":3,"NOW()":"2017-11-21T06:16:31.000Z","enterprise_id":1,"member_info":"영상테스트용","name":"@test","phone":"1566-2864"},"servertime":"2017-11-21 15:16:31"}}
# LIST_TEST {"result":{"ret":"success","msg":"cm_list가 전송되었습니다"},
# "data":{"event":[],"list":[{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"00:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"00:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"00:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"00:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"00:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"00:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"01:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"01:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"01:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"01:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"01:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"01:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"02:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"02:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"02:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"02:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"02:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"02:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"03:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"03:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"03:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"03:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"03:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"03:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"04:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"04:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"04:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"04:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"04:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"04:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"05:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"05:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"05:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"05:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"05:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"05:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"06:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"06:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"06:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"06:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"06:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"06:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"07:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"07:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"07:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"07:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"07:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"07:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"08:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"08:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"08:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"08:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"08:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"08:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"09:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"09:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"09:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"09:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"09:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"09:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"10:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"10:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"10:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"10:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"10:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"10:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"11:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"11:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"11:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"11:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"11:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"11:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"12:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"12:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"12:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"12:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"12:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"12:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"13:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"13:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"13:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"13:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"13:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"13:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"14:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"14:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"14:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"14:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"14:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"14:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"15:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"15:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"15:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"15:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"15:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"15:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"16:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"16:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"16:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"16:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"16:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"16:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"17:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"17:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"17:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"17:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"17:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"17:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"18:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"18:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"18:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"18:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"18:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"18:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"19:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"19:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"19:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"19:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"19:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"19:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"20:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"20:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"20:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"20:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"20:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"20:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"21:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"21:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"21:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"21:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"21:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"21:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"22:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"22:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"22:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"22:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"22:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"22:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"},{"type":0,"cm_info":"Lovelyz - Ah Choo MV","time":"23:00:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18476.mp4","cm_id":18476,"duration":"00:03:38"},{"type":0,"cm_info":"Sistar - Touch My Body","time":"23:10:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18477.mp4","cm_id":18477,"duration":"00:03:32"},{"type":0,"cm_info":"AOA - Short Hair","time":"23:20:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18478.mp4","cm_id":18478,"duration":"00:04:40"},{"type":0,"cm_info":"GFriend - Me Gustas Tu","time":"23:30:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18479.mp4","cm_id":18479,"duration":"00:04:11"},{"type":0,"cm_info":"GFRIEND - Rough","time":"23:40:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18480.mp4","cm_id":18480,"duration":"00:04:46"},{"type":0,"cm_info":"BLACKPINK - PLAYING WITH FIRE","time":"23:50:00","wait_num":-1,"route":"http://cdn2.rhymeduck.com/video/18481.mp4","cm_id":18481,"duration":"00:03:28"}]}}


MEMBER_ID = 0
PLAYLIST_ID = 0
ROUTE = ""
HOST = "";

ID = "test_cosfa"
PASS = "12345"

WEEK   = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT','SUN']
BASE_PATH = "../"

FILE_JSON = "cm.json"
# URL_PATH = SERVER + "movie/" + FILE_JSON
LOCAL_PATH = BASE_PATH + "cm/"
LOCAL_JSON = BASE_PATH + "job/" + FILE_JSON

DEBUG = False
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/cm.log')

#Single Instance
fh=4
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


    logd( "download", "%s %sjob/%s/%s start" % ( url, BASE_PATH, path, filename ) );
    if os.path.isfile( BASE_PATH+"job/"+path + "/" + filename )  == True:
        logd("main", "exist file")
        return

    try:
        f = urllib2.urlopen(url, timeout = 10)
    except urllib2.URLError, e:
        logd("main", "timeout %r" % e)
        exit()

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

    local_json = None 
    #Server Local Json
    if os.path.isfile( LOCAL_JSON )  == True:
        local_file=open(LOCAL_JSON, 'r')
        local_json=json.load(local_file)
        # logd("main","local %s " % local_json)



    TODAY = datetime.date.today().strftime('%Y-%m-%d')
    #Version 
    if local_json is None or  TODAY > local_json['date'] :
        logd("main","--new version--"+TODAY)

        data = {"member_id":MEMBER_ID, "weekday":WEEK[datetime.date.today().weekday()], "date": TODAY }
        # print(data)
        res = post(HOST + URL_LIST,data)
        # print (res)
        list = json.loads(res)
        list['date'] = TODAY
        if list['result']['ret'] == "success" : 
            cm_list = list['data']['list']

            #make directory
            logd("main","--Make Directory--")
            directory_name = LOCAL_PATH + TODAY
            if os.path.isdir(directory_name) == True :
                shutil.rmtree(directory_name)
            os.mkdir( directory_name , 0755 );

            #Download
            logd("main","--Download--")
            count = 0
            for item in cm_list:
                logd("main",item)
                download( directory_name , item['route'] )
                # if count > 5 :
                #     break
                # count = count+1

            #Save Last Version
            logd("main","--Save--")
            output_file=open( LOCAL_JSON, 'w')
            json.dump(list, output_file)
            output_file.close() 


    logd("main", "END");

if __name__ == "__main__":
    main()

