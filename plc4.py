"""
swat-s1 plc4.py
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

PLC4_ADDR = '192.168.1.40:44818'
PLC6_ADDR = '192.168.1.60:44818'

PLC4_TAGS = (
    ('P401', 4, 'INT'),
    ('P403', 4, 'INT'),
    ('FIT401', 4, 'REAL'),
    ('LIT401', 4, 'REAL'),
    ('LS401', 4 , 'REAL'),
    ('LS601', 4 , 'REAL')
)

LIT_401_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.40,
    'H': 1.000,
    'HH': 1.200,
}

LS_401_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.400,
    'H': 1.000,
    'HH': 1.200,
}

LS_601_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.400,
    'H': 1.000,
    'HH': 1.200,
}

LIT401_4 = ('LIT401', 4)
LS401_4 = ('LS401', 4)
#LS601_4 = ('LS601', 4)

P401 = ('P401', 4)
P403 = ('P403', 4)

LS601_6 = ('LS601', 6)

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

# TODO: real value tag where to read/write flow sensor
class SwatPLC4():
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
           ADDRESS = '--address 192.168.1.40:44818 '
           TAGS=''
           for tag in PLC4_TAGS:
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
           # '--log ' + self._client_log +
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
            print(raw_out)
            raw_string = raw_out[0]
            print(type(raw_string))
            out = raw_string[(raw_string.find(b'[') + 1):raw_string.find(b']')]
            
            return out

        except Exception as error:
            print ('ERROR enip _receive: ', error)

    def pre_loop(self, sleep=0.2):
       # print 'DEBUG: swat-s1 plc1 enters pre_loop'
        #logging.basicConfig(filename='logs/plc1log.log', encoding ='utf-8', level=logging.DEBUG, filemode = 'w', format='%(asctime)s %(levelname)-8s %(message)s')
        time.sleep(sleep)

    def main_loop(self):
        """plc4 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

      #  print 'DEBUG: swat-s1 plc4 enters main_loop.'

        count = 0
        while(count <= PLC_SAMPLES):
            #logging.debug('plc 4 count : %d', count)
            lit401 = float(self.get(LIT401_4))
            self.send(LIT401_4, lit401, PLC4_ADDR)
            #logging.debug("PLC4 - get lit401: %f",lit401)

            ls401 = float(self.get(LS401_4))
            self.send(LS401_4, ls401, PLC4_ADDR)
            #logging.debug("PLC4 - get ls401: %f",ls401)

            ls601 = float(self.receive(LS601_6, PLC6_ADDR))
            #self.send(LS601_4, ls601, PLC4_ADDR)
            #logging.debug("PLC4 - receive ls601: %f", ls601)

            if  lit401 <= LIT_401_M['L'] or ls401 <= LS_401_M['L'] or ls601 >= LS_601_M['H']:
                 # CLOSE MV201
                 self.set(P401, 0)
                 self.send(P401, 0, PLC4_ADDR)
                 self.set(P403, 0)
                 self.send(P403, 0, PLC4_ADDR)
                 #logging.info("PLC4 - LIT401 under LIT401_L or LIT401 under LIT401_L  -> close p401 and p403")
            else:
                 # OPEN MV201
                 self.set(P401, 1)
                 self.send(P401, 1, PLC4_ADDR)
                 self.set(P403, 1)
                 self.send(P403, 1, PLC4_ADDR)
                 #logging.info("PLC4 - lit401 over LIT_401_M['L'] and LS401 over LS401_L  -> open p401 and p403")

            

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        #logging.debug('Swat PLC4 shutdown')


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc4 = SwatPLC4()
        #name='plc1',
        #state=STATE,
        #protocol=PLC1_PROTOCOL,
        #memory=PLC1_DATA,
        #disk=PLC1_DATA)
