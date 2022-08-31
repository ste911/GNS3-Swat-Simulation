#from utils import  NaHSO3_PUMP_FLOWRATE_OUT
#from utils import NaHSO3_TANK_HEIGHT, NaHSO3_TANK_SECTION, NaHSO3_TANK_DIAMETER
#from utils import  NAHSO3T_INIT_LEVEL
#from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES


import sys
import time
import threading
import logging
import sqlite3

# SPHINX_SWAT_TUTORIAL TAGS(
MV501 = ('MV501', 5)

P401 = ('P401', 4)
P403 = ('P403', 4)
P501 = ('P501', 5)

LS401 = ('LS401', 4)


# NaHSO3 TANK
NaHSO3_TANK_HEIGHT = 1.750           # m
NaHSO3_TANK_DIAMETER = 0.55          # m
NaHSO3_TANK_SECTION = 0.24           # m^2
NaHSO3_PUMP_FLOWRATE_OUT = 0.00078   # m^3/h
NAHSO3T_INIT_LEVEL = 0.500     # m

#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

class NaHSO3Tank():

    def __init__(
            self, name,
            section, level):
        """
        :param str name: device name
        :param float section: cross section of the tank in m^2
        :param float level: current level in m
        """

        self.section = section
        self.level = level
        self.name = name
        self.pre_loop()
        self.main_loop()
    #def _start(self):
     #   self.pre_loop()
      #  self.main_loop()
    def get(self, what):
        get_query = 'SELECT value FROM swat_s1 WHERE name = ? AND pid = ?'
        with sqlite3.connect("swat_s1_db.sqlite") as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(get_query, what )
                record = cursor.fetchone()
                return record[0] 
            except sqlite3.Error as e:
                print('_get ERROR: %s: ' % e.args[0])

    def set(self, what, value):
        set_query = 'UPDATE  swat_s1 SET value = ? WHERE name = ? AND pid = ?'
        what = tuple([value,what[0],what[1]])
        with sqlite3.connect("swat_s1_db.sqlite") as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(set_query, what )
                conn.commit()
                return value
            except sqlite3.Error as e:
                print('_get ERROR: %s: ' % e.args[0])

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.level = self.set(LS401, 0.800)
        
        # SPHINX_SWAT_TUTORIAL STATE INIT)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)
            new_level = self.level
            p403 = self.get(P403)
            p401 = self.get(P401)
            p501 = self.get(P501)
            mv501 = self.get(MV501)
            
            nahso3_volume = self.section * new_level
            logging.debug('NaHSO3Tank count %d', count)
            if int(p403) == 1 and int(p501)==1 and int(mv501)==1 :
                outflow = NaHSO3_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                nahso3_volume -= outflow

            # compute new hcl_level
            new_level = nahso3_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            #logging.debug('NaHSO3Tank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS401, new_level)

            if int(p401) ^ int(p403):
                self.set(P403,p401)

            count += 1
            time.sleep(PP_PERIOD_SEC)



if __name__ == '__main__':

   # logging.basicConfig(filename='logs/physicalProc.log', encoding ='utf-8', level=logging.DEBUG)


    nahso3t = NaHSO3Tank(
        name='nahso3t',
        section=NaHSO3_TANK_SECTION,
        level=NAHSO3T_INIT_LEVEL
    )
