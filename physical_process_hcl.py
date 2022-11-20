import sys
import time
import threading
import logging
import sqlite3

MV201 = ('MV201', 2)

P203 = ('P203', 2)
LS202 = ('LS202', 2)

LIT101 = ('LIT101', 1)
LIT301 = ('LIT301', 3)
LIT401 = ('LIT401', 4)

# HCL TANK
HCl_TANK_HEIGHT = 1.750           # m
HCl_TANK_DIAMETER = 0.55          # m
HCl_TANK_SECTION = 0.24           # m^2
HCl_PUMP_FLOWRATE_OUT = 0.00078   # m^3/h
HCLT_INIT_LEVEL = 0.500     # m

#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES


class HClTank():

    def __init__(
             self,section,level):
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

        self.set(P203, 0)
        self.level = self.set(LS202, 1)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)            
            new_level = self.level
            p203 = self.get(P203)
            mv201 = self.get(MV201)
            hcl_volume = self.section * new_level
            logging.debug('HClTank count %d', count)
            if int(p203) == 1 and int(mv201)==1:
                outflow = HCl_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                hcl_volume -= outflow

            # compute new hcl_level
            new_level = hcl_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('HClTank new level %f with delta %f', new_level, new_level -self.level)
            self.level =  self.set(LS202, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':


    f = open("hcl.log", "w")
    f.close()
    logging.basicConfig(filename='hcl.log', level=logging.DEBUG)
    
    hclt = HClTank(
        section=HCl_TANK_SECTION,
        level=HCLT_INIT_LEVEL
    )
