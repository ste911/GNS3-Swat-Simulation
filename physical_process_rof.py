#from utils import ROF_PUMP_FLOWRATE_IN, ROF_PUMP_FLOWRATE_OUT
#from utils import ROF_TANK_HEIGHT, ROF_TANK_SECTION, ROF_TANK_DIAMETER
#from utils import ROFT_INIT_LEVEL
#from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES

import sys
import time
import threading
import logging
import sqlite3

# SPHINX_SWAT_TUTORIAL TAGS(

MV302 = ('MV302', 3)
MV501 = ('MV501', 5)


P301 = ('P301', 3)
P401 = ('P401', 4)
P501 = ('P501', 5)

LIT401 = ('LIT401', 4)
FIT301 = ('FIT301', 3)
FIT401 = ('FIT401', 4)
FIT501 = ('FIT501', 5)
FIT502 = ('FIT502', 5)

# ROF TANK
ROF_TANK_HEIGHT = 1.600           # m
ROF_TANK_DIAMETER = 1.38          # m
ROF_TANK_SECTION = 1.5            # m^2
ROF_PUMP_FLOWRATE_IN = 2.55       # m^3/h
ROF_PUMP_FLOWRATE_OUT = 2.45      # m^3/h
ROFT_INIT_LEVEL = 0.500           # m


#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

class ROFWaterTank():
 
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

  #  def _start(self):
   #     self.pre_loop()
    #    self.main_loop()

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
        # SPHINX_SWAT_TUTORIAL STATE INIT)

        # test underflow
         self.level = self.set(LIT401, 0.9)
         self.set(P301, 0)
         self.set(MV302,0)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)
            new_level = self.level
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            mv302 = self.get(MV302)
            p301 = self.get(P301)
            mv501 = self.get(MV501)
            logging.debug('ROFTank count %d', count)
            if int(mv302) == 1 and int(p301) == 1 :
                inflow = ROF_PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                water_volume += inflow
            else:
                self.set(FIT301, 0.00)

            # outflows volumes
            p401 = self.get(P401)
            p501 = self.get(P501)
            mv501 = self.get(MV501)
            if int(p401) == 1 and int(p501)==1 and int(mv501)==1:
                self.set(FIT401, ROF_PUMP_FLOWRATE_OUT)
                self.set(FIT501, ROF_PUMP_FLOWRATE_OUT)
                self.set(FIT502, ROF_PUMP_FLOWRATE_OUT)
                outflow = ROF_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                water_volume -= outflow
            else:
                self.set(FIT401, 0.00)
                self.set(FIT501, 0.00)
                self.set(FIT502, 0.00)

            # compute new water_level
            new_level = water_volume / self.section
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
           # logging.debug('ROFTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LIT401, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    #logging.basicConfig(filename='logs/physicalProc.log', encoding ='utf-8', level=logging.DEBUG)


    roft  = ROFWaterTank(
        name='roft',
        section=ROF_TANK_SECTION,
        level=ROFT_INIT_LEVEL
    )
