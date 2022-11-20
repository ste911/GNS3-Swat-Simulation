import sys
import time
import threading
import logging
import sqlite3

# SPHINX_SWAT_TUTORIAL TAGS(
MV201 = ('MV201', 2)
P201 = ('P201', 2)
LS201 = ('LS201', 2)

# NaCL TANK
NaCl_TANK_HEIGHT = 1.750           # m
NaCl_TANK_DIAMETER = 0.55          # m
NaCl_TANK_SECTION = 0.24           # m^2
NaCl_PUMP_FLOWRATE_OUT = 0.05   # m^3/h
NACLT_INIT_LEVEL = 0.500     # m

#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

class NaClTank():
    
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

        self.set(P201, 0)
        self.level = self.set(LS201, 1)

    def main_loop(self):
        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)
            new_level = self.level
            p201 = self.get(P201)
            mv201 = self.get(MV201)
            nacl_volume = self.section * new_level
            logging.debug('NaClTank count %d', count)
            if int(p201) == 1 and int(mv201) == 1:
                outflow = NaCl_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                nacl_volume -= outflow

            # compute new nacl_level
            new_level = nacl_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('NaClTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS201, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)           


if __name__ == '__main__':
    
    f= open("nacl.log","w")
    f.close()
    logging.basicConfig(filename='nacl.log', level=logging.DEBUG)

    naclt = NaClTank(
        section=NaCl_TANK_SECTION,
        level=NACLT_INIT_LEVEL
    )
