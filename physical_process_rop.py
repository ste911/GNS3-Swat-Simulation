import sys
import time
import threading
import logging
import sqlite3

MV501 = ('MV501', 5)
P401 = ('P401', 4)
P501 = ('P501', 5)
P601 = ('P601', 6)


LS601 = ('LS601', 6)

# ROP TANK
ROP_TANK_HEIGHT = 1.24           # m
ROP_TANK_DIAMETER = 1.16          # m
ROP_TANK_SECTION = 1.05            # m^2
ROP_PUMP_FLOWRATE_IN = 2.55       # m^3/h
ROP_PUMP_FLOWRATE_OUT = 2.45      # m^3/h
ROPT_INIT_LEVEL = 0.500     # m

#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

class ROPWaterTank():

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

        self.level=self.set(LS601,0.5)
        
    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)
            new_level = self.level
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            mv501 = self.get(MV501)
            p401 = self.get(P401)
            p501 = self.get(P501)
            logging.debug('ROPTank count %d', count)
            if int(mv501) == 1 and int(p401)==1 and int(mv501)==1:
                inflow = ROP_PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                water_volume += inflow
                

            # outflows volumes
            p601 = self.get(P601)
            if int(p601) == 1:
                outflow = ROP_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                water_volume -= outflow

            # compute new water_level
            new_level = water_volume / self.section
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            #logging.debug('ROPTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS601, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)

if __name__ == '__main__':

   # logging.basicConfig(filename='logs/physicalProc.log', encoding ='utf-8', level=logging.DEBUG)


    ropt  = ROPWaterTank(
        name='ropt',
        section=ROP_TANK_SECTION,
        level=ROPT_INIT_LEVEL
    )
