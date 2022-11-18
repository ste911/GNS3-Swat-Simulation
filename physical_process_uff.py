import sys
import time
import threading
import logging
import sqlite3

MV201 = ('MV201', 2)
MV302 = ('MV302', 3)
MV501 = ('MV501', 5)

P101 = ('P101', 1)
P301 = ('P301', 3)

LIT301 = ('LIT301', 3)
                      
# UFF TANK
UFF_TANK_HEIGHT = 1.600           # m
UFF_TANK_DIAMETER = 1.38          # m
UFF_TANK_SECTION = 1.5            # m^2
UFF_PUMP_FLOWRATE_IN = 2.55       # m^3/h
UFF_PUMP_FLOWRATE_OUT = 2.45      # m^3/h
UFFT_INIT_LEVEL = 0.500     # m



#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

class UFFWaterTank():

    def __init__(
            self, section, level):
        """
        :param float section: cross section of the tank in m^2
        :param float level: current level in m
        """

        self.section = section
        self.level = level
        self.pre_loop()
        self.main_loop()

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

        self.set(MV201, 0)
        self.set(MV302,0)
        self.level = self.set(LIT301, 0.000)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)
            new_level = self.level
            
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            p101 = self.get(P101)
            mv201 = self.get(MV201)
            mv302 = self.get(MV302)
            mv501 = self.get(MV501)
            logging.debug('UFFTank count %d', count)
            if int(mv201) == 1 and int(p101): 
                inflow = UFF_PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                water_volume += inflow

            # outflows volumes
            p301 = self.get(P301)
            if int(p301) == 1 and int(mv302):
                outflow = UFF_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                water_volume -= outflow

            # compute new water_level
            new_level = water_volume / self.section
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            #logging.debug('UFFTank new level %f with delta %f', new_level, new_level -self.level)    
            self.level = self.set(LIT301, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

   # logging.basicConfig(filename='logs/physicalProc.log', encoding ='utf-8', level=logging.DEBUG)


    ufft  = UFFWaterTank(
        name='ufft',
        section=UFF_TANK_SECTION,
        level=UFFT_INIT_LEVEL
    )
