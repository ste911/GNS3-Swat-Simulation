"""
swat-s1 plc2.py
"""


#from utils import PLC1_DATA, STATE, PLC1_PROTOCOL
#from utils import PLC_PERIOD_SEC, PLC_SAMPLES
#from utils import IP, LIT_101_M, LIT_301_M, FIT_201_THRESH,LS_201_M,LS_202_M,LS_203_M

import time
import logging
import cpppo
import subprocess
import shlex
from pwn import *
import string

HOST='192.168.1.1'
PORT=3001 

PLC2_TAGS = (
    ('FIT201', 2, 'REAL'),
    ('MV201', 2, 'INT'),
    ('P201', 2, 'INT'),
    ('LS201', 2, 'REAL'),
    ('P203', 2, 'INT'),
    ('LS202', 2, 'REAL'),
    ('P205', 2, 'INT'),
    ('LS203', 2, 'REAL'),
    ('LIT301', 2 , 'REAL')
    # no interlocks
)


LIT_301_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.400,
    'H': 1.000,
    'HH': 1.200,
}

LS_201_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.400,
    'H': 1.000,
    'HH': 1.200,
}

LS_202_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.400,
    'H': 1.000,
    'HH': 1.200,
}

LS_203_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.400,
    'H': 1.000,
    'HH': 1.200,
}
PLC1_ADDR = '192.168.1.10:44818'
PLC2_ADDR = '192.168.1.20:44818'
PLC3_ADDR = '192.168.1.30:44818'

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

FIT201_2 = ('FIT201', 2)
LS201_2 = ('LS201', 2)
LS202_2 = ('LS202', 2)
LS203_2 = ('LS203', 2)

P201 = ('P201', 2)
P203 = ('P203', 2)
P205 = ('P205', 2)
MV201 = ('MV201', 2)

#LIT301_2 = ('LIT301', 2)

LIT301_3 = ('LIT301', 3)

# TODO: real value tag where to read/write flow sensor
class SwatPLC2():
    def __init__(self):

        try:
            self.server = self.start_server()
            #self.server.wait()
            time.sleep(10)
            self.pre_loop()
            print('pre_loop end')
            self.main_loop()
        except Exception as e:
            print(e)
            self.stop_server()

        self.stop_server()

    def start_server(self):
        """Start a cpppo enip server.

        The command used to start the server is generated by
        ``_start_server_cmd``.

        Notice that the client has to manage the new process,
        eg:kill it after use.

        :address: to serve
        :tags: to serve
        """

        try:
           CMD = 'python3 -m cpppo.server.enip '
           PRINT_Stdout = '--print '
           ADDRESS = '--address 192.168.1.20:44818 '
           TAGS=''
           for tag in PLC2_TAGS:
                 TAGS+=str(tag[0])
                 for field in tag[1:-1]:
                    TAGS+= ':' +str(field)

                 TAGS+='='
                 TAGS+=str(tag[-1])
                 TAGS+= ' '
           cmd = shlex.split( CMD+ PRINT_Stdout + ADDRESS +TAGS)
           # cmd = EnipProtocol._start_server_cmd(address, tags)
           server = subprocess.Popen(cmd, shell=False)
           return server

        except Exception as error:
            print ('ERROR enip _start_server: ', error)

    def stop_server(self):
        try:
           self.server.kill()
           print('Enip server killed')

        except Exception as error:
             print("Error in stopping enip server: ",error)

    def set (self, field, val):
      msg = 'SET:'
      msg+= field[0]+':'
      msg+= str(field[1])+':'
      msg += str(val)
      server = remote(HOST, PORT)
      server.send(msg.encode())
      server.close()
      return val

    def get (self, field):
      msg = 'GET:'
      msg+= field[0]+':'
      msg+= str(field[1])+':'
      server = remote(HOST, PORT)
      server.send(msg.encode())
      resp = server.recv(1024)
      server.close()
      return resp


    def send(self, what, value, address, **kwargs):
        """Send (write) a value to another host.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        :what: tuple addressing what
        :value: sent
        :address: ip[:port]
        """


        tag_string = ''
        tag_string += str(what[0])

        if len(what) >1:
          for field in what[1:]:
            tag_string += ':'
            tag_string += str(field)

        if value is not None:
           tag_string+= '='
           tag_string+= str(value)

        # print 'DEBUG enip _send tag_string: ', tag_string

        cmd = shlex.split(
            'python3 -m cpppo.server.enip.client ' +
            #'--log ' + self._client_log +
            '--address ' + address +
            ' ' + tag_string
        )
        # print 'DEBUG enip _send cmd shlex list: ', cmd

        # TODO: pipe stdout and return the sent value
        try:
            client = subprocess.Popen(cmd, shell=False)
            client.wait()

        except Exception as error:
            logging.debug('Exeption error %s', str(error))
            print ('ERROR enip _send: ', error)

    def receive(self, what, address, **kwargs):
        """Receive (read) a value from another host.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        :what: to ask for
        :address: to receive from

        :returns: tag value as a `str`
        """

        tag_string = ''
        tag_string += str(what[0])

        if len(what) >1:
          for field in what[1:]:
            tag_string += ':'
            tag_string += str(field)

        cmd = shlex.split(
            'python3 -m cpppo.server.enip.client ' + '--print ' +
            #'--log ' + self._client_log +
            '--address ' + address +
            ' ' + tag_string
        )
        # print 'DEBUG enip _receive cmd shlex list: ', cmd

        try:
            client = subprocess.Popen(cmd, shell=False,
                stdout=subprocess.PIPE)

            # client.communicate is blocking
            raw_out = client.communicate()
            # print 'DEBUG enip _receive raw_out: ', raw_out

            # value is stored as first tuple element
            # between a pair of square brackets
            raw_string = raw_out[0]
            out = raw_string[(raw_string.find(b'[') + 1):raw_string.find(b']')]

            return out

        except Exception as error:
            print ('ERROR enip _receive: ', error)

    def pre_loop(self, sleep=0.2):
       # print 'DEBUG: swat-s1 plc1 enters pre_loop'
        #logging.basicConfig(filename='logs/plc1log.log', encoding ='utf-8', level=logging.DEBUG, filemode = 'w', format='%(asctime)s %(levelname)-8s %(message)s')
        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - read flow level sensors #2
            - update interal enip server
        """

#        print 'DEBUG: swat-s1 plc2 enters main_loop.'


        count = 0
        while(count <= PLC_SAMPLES):
        #    logging.debug('PLC2 count : %d', count)
            #fit201 = float(self.get(FIT201_2))
            #logging.debug("PLC2 - get fit201: %f", fit201)
           # self.send(FIT201_2, fit201, PLC2_ADDR)
            
            ls201 = float(self.get(LS201_2))
            self.send(LS201_2, ls201, PLC2_ADDR)
       #     logging.debug('PLC2 LS201: %.5f', ls201)
            
            ls202 = float(self.get(LS202_2))
            self.send(LS202_2, ls202, PLC2_ADDR)
      #      logging.debug('PLC2 LS202: %.5f', ls202)

            ls203 = float(self.get(LS203_2))
            self.send(LS203_2, ls203, PLC2_ADDR)
     #       logging.debug('PLC2 LS203: %.5f', ls203)


            lit301 = float(self.receive(LIT301_3, PLC3_ADDR))
    #       logging.debug("PLC2 - receive lit301: %f", lit301)
            #self.send(LIT301_2, lit301, PLC2_ADDR)

            if lit301 <= LIT_301_M['L'] and ls201 >= LS_201_M['L'] and ls202 >= LS_202_M['L'] \
                        and ls203 >= LS_203_M['L']:
                 # OPEN MV201
                 self.set(MV201, 1)
                 self.send(MV201, 1, PLC2_ADDR)
                 self.set(P201, 1)
                 self.send(P201, 1, PLC2_ADDR)
                 self.set(P203, 1)
                 self.send(P203, 1, PLC2_ADDR)
                 self.set(P205, 1)
                 self.send(P205, 1, PLC2_ADDR)
                # print "INFO PLC1 - lit301 under LIT_301_M['L'] -> open p201/3/5 mv201."

 #                logging.info("PLC2 - lit301 under LIT_301_M['L'] -> open p201/3/5 mv201.")
            else:
                 # CLOSE MV201
                 self.set(MV201, 0)
                 self.send(MV201, 0, PLC2_ADDR)
                 self.set(P201, 0)
                 self.send(P201, 0, PLC2_ADDR)
                 self.set(P203, 0)
                 self.send(P203, 0, PLC2_ADDR)
                 self.set(P205, 0)
                 self.send(P205, 0, PLC2_ADDR)

  #               logging.info("PLC2 - fit201 under FIT_201_THRESH " \
   #                    "or over LIT_301_M['H']: -> close mv201 p201/3/5.")


            time.sleep(PLC_PERIOD_SEC)
            count += 1

        logging.debug('Swat PLC2 shutdown')

if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = SwatPLC2()
        #name='plc1',
        #state=STATE,
        #protocol=PLC1_PROTOCOL,
        #memory=PLC1_DATA,
        #disk=PLC1_DATA)
