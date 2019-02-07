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

import re

from bluetooth import *

# btserver.py
# - Bluetooth Enable
# - Wifi Enable
# - Android Device Connect


SUPPLICANT_LOG_FILE = "wpa_supplicant.log"

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


advertise_service( server_sock, "BTServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ] 
                    )

BASE_PATH = "../"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_PATH+'log/btserver.log')

#LOCAL_JSON = "list.json"
LOCAL_SETTING = "setting.json"


FILE_JSON = "btserver.json"
LOCAL_JSON = BASE_PATH + "job/" + FILE_JSON





def command(cmd):
    logd("executer", "executer "+ cmd)
    # os.system("python "+BASE_PATH+"job/"+file+" &")
    os.system("nohup "+cmd+" &")


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

def run_program(rcmd):
    cmd = shlex.split(rcmd)
    executable = cmd[0]
    executable_options=cmd[1:]

    try:
        proc  = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
        response = proc.communicate()
        response_stdout, response_stderr = response[0], response[1]
    except OSError, e:
        if e.errno == errno.ENOENT:
            logging.debug( "Unable to locate '%s' program. Is it in your path?" % executable )
        else:
            logging.error( "O/S error occured when trying to run '%s': \"%s\"" % (executable, str(e)) )
    except ValueError, e:
        logging.debug( "Value error occured. Check your parameters." )
    else:
        if proc.wait() != 0:
            logging.debug( "Executable '%s' returned with the error: \"%s\"" %(executable,response_stderr) )
            return response
        else:
            logging.debug( "Executable '%s' returned successfully. First line of response was \"%s\"" %(executable, response_stdout.split('\n')[0] ))
            return response_stdout


def logd(tag, msg):
    localtime   = time.localtime()
    timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
    logging.debug("[%s][%s][%s]" %(tag,timeString,msg) )
    #print "[%s][%s][%s]" %(tag,localtime,msg) 






# Wifi function
def start_wpa(_iface):
    run_program("wpa_cli terminate")
    time.sleep(1)
    run_program("wpa_supplicant -B -Dwext -i %s -C /var/run/wpa_supplicant -f %s" %(_iface, SUPPLICANT_LOG_FILE))

def get_wnics():
    r = run_program("iwconfig")
    ifaces=[]
    for line in r.split("\n"):
        if "IEEE" in line:
            ifaces.append( line.split()[0] )
    return ifaces

def get_networks(iface, retry=10):
    while retry > 0:
        if "OK" in run_program("wpa_cli -i %s scan" % iface):
            networks=[]
            r = run_program("wpa_cli -i %s scan_result" % iface).strip()
            if "bssid" in r and len ( r.split("\n") ) >1 :
                for line in r.split("\n")[1:]:
                    b, fr, s, f = line.split()[:4]
                    ss = " ".join(line.split()[4:]) #Hmm, dirty
                    networks.append( {"bssid":b, "freq":fr, "sig":s, "ssid":ss, "flag":f} )
                return networks
        retry-=1
        logging.debug("Couldn't retrieve networks, retrying")
        time.sleep(0.5)
    logging.error("Failed to list networks")


def _disconnect_all(_iface):
    """
    Disconnect all wireless networks.
    """
    lines = run_program("wpa_cli -i %s list_networks" % _iface).split("\n")
    if lines:
        for line in lines[1:-1]:
            run_program("wpa_cli -i %s remove_network %s" % (_iface, line.split()[0]))

def connect_to_network(_iface, _ssid, _type, _pass=None):

    _disconnect_all(_iface)
    time.sleep(1)
    if run_program("wpa_cli -i %s add_network" % _iface) == "0\n":
        logging.debug("add_network")
        if run_program('wpa_cli -i %s set_network 0 ssid \'"%s"\'' % (_iface,_ssid)) == "OK\n":
            logging.debug('wpa_cli -i %s set_network 0 ssid \'"%s"\'' % (_iface,_ssid))
            if _type == "OPEN":
                run_program("wpa_cli -i %s set_network 0 auth_alg OPEN" % _iface)
                run_program("wpa_cli -i %s set_network 0 key_mgmt NONE" % _iface)
            elif _type == "WPA" or _type == "WPA2":
                run_program('wpa_cli -i %s set_network 0 psk \'"%s"\'' % (_iface,_pass))
                logging.debug('wpa_cli -i %s set_network 0 psk \'"%s"\'' % (_iface,_pass))
                print "WPA"
            elif _type == "WEP":
                run_program("wpa_cli -i %s set_network 0 wep_key %s" % (_iface,_pass))
            else:
                logging.error("Unsupported type")

            run_program("wpa_cli -i %s select_network 0" % _iface)

def is_associated(_iface):
    """
    Check if we're associated to a network.
    """
    if "wpa_state=COMPLETED" in run_program("wpa_cli -i %s status" % _iface):
        return True
    return False





def has_ip(_iface):
    status = run_program("wpa_cli -i %s status" % _iface)
    r = re.search("ip_address=(.*)", status)
    if r:
        return r.group(1)
    return False

def do_dhcp(_iface):
    run_program("dhclient %s" % _iface)

######







def main():

    # Bluetooth Enable
    logd("main", "start");

    logd("main","hciconfig hci0 up")
    run_program("hciconfig hci0 up")
    #time.sleep(2)
    logd("main","hciconfig hci0 piscan")
    run_program("hciconfig hci0 piscan")

    logd("main","hciconfig hci0 name WANTREEZ")
    run_program("hciconfig hci0 name WANTREEZ")

    #time.sleep(2)
    logd("main", "python btserver.py")



    # Wifi Connect 
    # 이전에 연결된 WIfi

    local_json = None 
    #Server Local Json
    if os.path.isfile( LOCAL_JSON )  == True:
        local_file=open(LOCAL_JSON, 'r')
        local_json=json.load(local_file)
        logd("main","local %s " % local_json)

        ssid = local_json['ssid']
        type = local_json['type']
        passw = local_json['passw']

        print('sudo ifconfig wlan0 up')
        os.system('sudo ifconfig wlan0 up')
        print('sudo iwconfig wlan0 essid '+ssid+' key s:'+passw)
        # os.system('sudo iwconfig wlan0 essid '+ssid+' key s:'+passw)
        connect_to_network("wlan0", ssid, type, passw)
        cnt = 0
        while not is_associated("wlan0"):
            time.sleep(1)
            cnt+=1
            print "check."
            if cnt >5 :
                print "fail."
                break
            print "wlan0."
            do_dhcp("wlan0")
            print "has_ip."
            while not has_ip("wlan0"):
                print "Success."
                time.sleep(1)
                cnt+=1
                if cnt >6 :
                    print "fail."
                    break
            ip = has_ip("wlan0") 
            print "wifi_status [%s]" % ip
                # client_sock.send( has_ip("wlan0") )
                # client_sock.send(";");




    # Bluetooth 접속 대기
    # Android Connection
    # Android Command Process

    while True:
        print "Waiting for connection on RFCOMM channel %d" % port
        client_sock, client_info = server_sock.accept()
        print "Accepted connection from ", client_info
    
        try:
            while True:
                data = client_sock.recv(1024)
                if len(data) == 0: break
                data = data.rstrip()


                # Command 별 처ㄹ
                print "received [%s]" % data
                if "wifi_list" in data :
                    start_wpa("wlan0")
                    networks = get_networks("wlan0")
                    if networks:
                        networks = sorted(networks, key=lambda k: k['sig'])
                        print "[+] Networks in range:" + "".join([str(i) for i in  networks])
                        for network in networks:
                            # print " SSID:\t%s" % network['ssid']
                            # print ",".join([str(i) for i in  networks])
                            client_sock.send( ",".join([str(i) for i in  networks]))
                            client_sock.send(";");
                elif "wifi_connect" in data :
                    print "wifi_connect [%s]" % data
                    arr = data.split(":")
                    ssid = arr[1]
                    ty = arr[2]
                    passw = arr[3]
                    connect_to_network("wlan0", ssid, ty, passw)

                    ap = {"ssid":ssid,"type":ty,"passw":passw}
                    logd("main","--Save--")
                    output_file=open( LOCAL_JSON, 'w')
                    json.dump(ap, output_file)
                    output_file.close() 

                    cnt = 0
                    while not is_associated("wlan0"):
                        time.sleep(1)
                        cnt+=1
                        if cnt >5 :
                            print "fail."
                            break
                        print "Success."
                        do_dhcp("wlan0")
                        while not has_ip("wlan0"):
                            time.sleep(1)
                        client_sock.send( has_ip("wlan0") )
                        client_sock.send(";");
                elif "wifi_status" in data :
                    print "wifi_status [%s]" % data
                    ip = has_ip("wlan0") 
                    print "wifi_status [%s]" % ip
                    if not ip :
                        print "wifi_status [%s]" % "fail"
                        client_sock.send("FAIL")
                        client_sock.send(";");
                    else : 
                        print "wifi_status send [%s]" % ip
                        client_sock.send( ip )
                        client_sock.send(";");
                elif "reboot" in data :
                    print "reboot [%s]" % data
                    command("reboot")
                    client_sock.send("SUCCESS")
                    client_sock.send(";");
                else :
                    clinet_sock.send("FAIL;")


        except IOError:
            pass

        finally:
            print "disconnected"
            client_sock.close()
#            server_sock.close()
#	    continue 

    print "all done"

if __name__ == "__main__":
    main()

