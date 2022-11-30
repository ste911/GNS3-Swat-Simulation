import sys
import time
import threading
import logging
import sqlite3

MV101 = ('MV101', 1)
MV201 = ('MV201', 2)

P101 = ('P101', 1)


LIT101 = ('LIT101', 1)

# RWT TANK
TANK_HEIGHT = 1.600           # m
TANK_DIAMETER = 1.38          # m
TANK_SECTION = 1.5            # m^2
PUMP_FLOWRATE_IN = 2.55       # m^3/h
PUMP_FLOWRATE_OUT = 2.45      # m^3/h
RWT_INIT_LEVEL = 0.500     # m

#utils values
PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.40  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES


# TODO: implement orefice drain with Bernoulli/Torricelli formula
class RawWaterTank():

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

        self.set(MV101, 0)
        self.set(P101, 1)
        self.level = self.set(LIT101, 0.300)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            print (count,"/", PP_SAMPLES)
            new_level = self.level
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            mv101 = self.get(MV101)
            logging.debug('RawWaterTank count %d', count)
            if int(mv101) == 1:
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                water_volume += inflow

            # outflows volumes
            p101 = self.get(P101)
            mv201 = self.get(MV201)

            if int(p101) == 1 and int(mv201) == 1:
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                water_volume -= outflow

            # compute new water_level
            new_level = water_volume / self.section
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('RawWaterTank new level %f with delta %f', new_level, new_level -self.level)   
            
            self.level = self.set(LIT101, new_level)


            count += 1
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    f=open("rwt.log","w")
    f.close()

    logging.basicConfig(filename='rwt.log', level=logging.DEBUG)
    rwt  = RawWaterTank(
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )
