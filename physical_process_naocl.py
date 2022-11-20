import sys
import time
import threading
import logging
import sqlite3


MV201 = ('MV201', 2)
P205 = ('P205', 2)
LS203 = ('LS203', 2)


# NAOCL TANK
NaOCl_TANK_HEIGHT = 1.750           # m
NaOCl_TANK_DIAMETER = 0.55          # m
NaOCl_TANK_SECTION = 0.24           # m^2
NaOCl_PUMP_FLOWRATE_OUT = 0.065   # m^3/h
NAOCLT_INIT_LEVEL = 0.500     # m

#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

class NaOClTank():
   
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

        self.set(P205, 0)
        self.level = self.set(LS203, 1)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)
            new_level = self.level
            p205 = self.get(P205)
            mv201 = self.get(MV201)
            logging.debug('NaOClTank count %d', count)
            naocl_volume = self.section * new_level
            
            if int(p205) == 1 and int(mv201) ==1:
                outflow = NaOCl_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                naocl_volume -= outflow

            # compute new naocl_level
            new_level = naocl_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('NaOClTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS203, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)                           

if __name__ == '__main__':

    f=open("naocl.log","w")
    f.close()
    logging.basicConfig(filename='naocl.log', encoding ='utf-8', level=logging.DEBUG)

    naoclt = NaOClTank(
        section=NaOCl_TANK_SECTION,
        level=NAOCLT_INIT_LEVEL
    )
