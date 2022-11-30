"""
swat-s1 plc4.py
"""

import time
import logging
import cpppo
import subprocess
import shlex
from pwn import *
import string

HOST='192.168.1.1'
PORT=3001 

PLC6_ADDR = '192.168.1.60:44818'

PLC6_TAGS = (
    ('LS601', 6, 'REAL'),
    ('P601', 6, 'INT'),
)

LS_601_M = {  # ROP tank m
    'LL': 0.250,
    'L': 0.300,
    'H': 1.000,
    'HH': 1.200,
}

LS601_6 = ('LS601', 6)
P601 = ('P601',6)

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

class SwatPLC6():
    def __init__(self):

        try:
            log = open("plc6log.log","w")
            log.close()
            self.server = self.start_server()
            time.sleep(20)
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
           ADDRESS = '--address 192.168.1.60:44818 '
           TAGS=''
           for tag in PLC6_TAGS:
                 TAGS+=str(tag[0])
                 for field in tag[1:-1]:
                    TAGS+= ':' +str(field)

                 TAGS+='='
                 TAGS+=str(tag[-1])
                 TAGS+= ' '
           cmd = shlex.split( CMD+ PRINT_Stdout + ADDRESS +TAGS)
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
            '--address ' + address +
            ' ' + tag_string
        )
        # print 'DEBUG enip _send cmd shlex list: ', cmd

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
        logging.basicConfig(filename='plc6log.log', level=logging.DEBUG, filemode = 'w', format='%(asctime)s %(levelname)-8s %(message)s')
        time.sleep(sleep)

    def main_loop(self):
        """plc6 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

       # print 'DEBUG: swat-s1 plc6 enters main_loop.'
 
        count = 0
        while(count <= PLC_SAMPLES):
            #logging.debug('plc 6 count : %d', count)
            ls601 = float(self.get(LS601_6))
            self.send(LS601_6, ls601, PLC6_ADDR)
            logging.debug("PLC6 - get lit601: %f", ls601)


            if ls601 <= LS_601_M['L'] :
                self.set(P601,0)
                logging.info("PLC6 - LS601 under LS601_M['L'] or  -> close p601")
            else :
                self.set(P601,1)
                logging.info("PLC6 - LS601 under LS601_M['L'] or  -> open p601")
         
            time.sleep(PLC_PERIOD_SEC)
            count += 1

        logging.debug('Swat PLC6 shutdown')


if __name__ == "__main__":

    plc6 = SwatPLC6()
