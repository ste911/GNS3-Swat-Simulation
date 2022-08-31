from minicps.devices import Tank

from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES

from utils import  NaCl_PUMP_FLOWRATE_OUT
from utils import NaCl_TANK_HEIGHT, NaCl_TANK_SECTION, NaCl_TANK_DIAMETER
from utils import  NACLT_INIT_LEVEL

from utils import  HCl_PUMP_FLOWRATE_OUT
from utils import  HCl_TANK_HEIGHT, HCl_TANK_SECTION, HCl_TANK_DIAMETER
from utils import  HCLT_INIT_LEVEL

from utils import  NaOCl_PUMP_FLOWRATE_OUT
from utils import NaOCl_TANK_HEIGHT, NaOCl_TANK_SECTION, NaOCl_TANK_DIAMETER
from utils import  NAOCLT_INIT_LEVEL

from utils import UFF_PUMP_FLOWRATE_IN, UFF_PUMP_FLOWRATE_OUT
from utils import UFF_TANK_HEIGHT, UFF_TANK_SECTION, UFF_TANK_DIAMETER
from utils import UFFT_INIT_LEVEL

from utils import ROF_PUMP_FLOWRATE_IN, ROF_PUMP_FLOWRATE_OUT
from utils import ROF_TANK_HEIGHT, ROF_TANK_SECTION, ROF_TANK_DIAMETER
from utils import ROFT_INIT_LEVEL

from utils import  NaHSO3_PUMP_FLOWRATE_OUT
from utils import NaHSO3_TANK_HEIGHT, NaHSO3_TANK_SECTION, NaHSO3_TANK_DIAMETER
from utils import  NAHSO3T_INIT_LEVEL

from utils import ROP_PUMP_FLOWRATE_IN, ROP_PUMP_FLOWRATE_OUT
from utils import ROP_TANK_HEIGHT, ROP_TANK_SECTION, ROP_TANK_DIAMETER
from utils import ROPT_INIT_LEVEL

import sys
import time
import threading
import logging


# SPHINX_SWAT_TUTORIAL TAGS(
MV101 = ('MV101', 1)
MV201 = ('MV201', 2)
MV302 = ('MV302', 3)
MV501 = ('MV501', 5)

P101 = ('P101', 1)
P201 = ('P201', 2)
P203 = ('P203', 2)
P205 = ('P205', 2)
P301 = ('P301', 3)
P401 = ('P401', 4)
P403 = ('P403', 4)
P501 = ('P501', 5)
P601 = ('P601', 6)

LS201 = ('LS201', 2)
LS202 = ('LS202', 2)
LS203 = ('LS203', 2)
LS401 = ('LS401', 4)
LS601 = ('LS601', 6)

LIT101 = ('LIT101', 1)
LIT301 = ('LIT301', 3)
LIT401 = ('LIT401', 4)

FIT101 = ('FIT101', 1)
FIT201 = ('FIT201', 2)
FIT301 = ('FIT301', 3)
FIT401 = ('FIT401', 4)
FIT501 = ('FIT501', 5)
FIT502 = ('FIT502', 5)

# SPHINX_SWAT_TUTORIAL TAGS)


# TODO: implement orefice drain with Bernoulli/Torricelli formula
class RawWaterTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(MV101, 1)
        self.set(P101, 1)
        self.level = self.set(LIT101, 0.300)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

        # test underflow
        # self.set(MV101, 0)
        # self.set(P101, 1)
        # self.level = self.set(LIT101, 0.500)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            
            new_level = self.level
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            mv101 = self.get(MV101)
            logging.debug('\t\tcount %d', count)
            if int(mv101) == 1:
                self.set(FIT101, PUMP_FLOWRATE_IN)
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank inflow: ", inflow
                water_volume += inflow
                #print 'water_volume: %f' %water_volume
            else:
                self.set(FIT101, 0.00)

            # outflows volumes
            p101 = self.get(P101)
            mv201 = self.get(MV201)

            if int(p101) == 1 and int(mv201) == 1:
                self.set(FIT201, PUMP_FLOWRATE_OUT)
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank outflow: ", outflow
                water_volume -= outflow
            else:
                self.set(FIT201, 0.00)

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

class NaClTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(P201, 0)
        self.level = self.set(LS201, 1)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

    def main_loop(self):
        count = 0
        while(count <= PP_SAMPLES):
            
            new_level = self.level
            p201 = self.get(P201)
            mv201 = self.get(MV201)
            nacl_volume = self.section * new_level
            logging.debug('\t\tcount %d', count)
            if int(p201) == 1 and int(mv201) == 1:
                outflow = NaCl_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                nacl_volume -= outflow

            # compute new nacl_level
            new_level = nacl_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('\tNaClTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS201, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)           

class HClTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(P203, 0)
        self.level = self.set(LS202, 1)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            
            new_level = self.level
            p203 = self.get(P203)
            mv201 = self.get(MV201)
            hcl_volume = self.section * new_level
            logging.debug('\t\tcount %d', count)
            if int(p203) == 1 and int(mv201)==1:
                outflow = HCl_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                #print ' outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS %f = %f * %f' %(outflow, PUMP_FLOWRATE_OUT ,PP_PERIOD_HOURS)
                # print "DEBUG RawWaterTank outflow: ", outflow
                hcl_volume -= outflow

            # compute new hcl_level
            new_level = hcl_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
                logging.debug('\t\tHClTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS202, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)

class NaOClTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(P205, 0)
        self.level = self.set(LS203, 1)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            
            new_level = self.level
            p205 = self.get(P205)
            mv201 = self.get(MV201)
            logging.debug('\t\tcount %d', count)
            naocl_volume = self.section * new_level
            
            if int(p205) == 1 and int(mv201) ==1:
                outflow = NaOCl_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                #print ' outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS %f = %f * %f' %(outflow, PUMP_FLOWRATE_OUT ,PP_PERIOD_HOURS)
                # print "DEBUG RawWaterTank outflow: ", outflow
                naocl_volume -= outflow

            # compute new naocl_level
            new_level = naocl_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('\t\t\tNaOClTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS203, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)                           

class UFFWaterTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(MV201, 0)
        self.level = self.set(LIT301, 0.000)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

        # test underflow
        # self.set(MV101, 0)
        # self.set(P101, 1)
        # self.level = self.set(LIT101, 0.500)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            
            new_level = self.level
            
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            p101 = self.get(P101)
            mv201 = self.get(MV201)
            mv302 = self.get(MV302)
            mv501 = self.get(MV501)
            logging.debug('\t\tcount %d', count)
            if int(mv201) == 1 and int(p101):                
                #self.set(FIT301, UFF_PUMP_FLOWRATE_IN)
                inflow = UFF_PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank inflow: ", inflow
                water_volume += inflow
                #print 'water_volume: %f' %water_volume
            else:
                self.set(FIT301, 0.00)

            # outflows volumes
            p301 = self.get(P301)
            if int(p301) == 1 and int(mv302):
                self.set(FIT301, UFF_PUMP_FLOWRATE_OUT)
                outflow = UFF_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank outflow: ", outflow
                water_volume -= outflow
                #print 'water_volume: %f' %water_volume
            else:
                self.set(FIT301, 0.00)

            # compute new water_level
            new_level = water_volume / self.section
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('\t\t\t\tUFFTank new level %f with delta %f', new_level, new_level -self.level)    
            self.level = self.set(LIT301, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)

class ROFWaterTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        # SPHINX_SWAT_TUTORIAL STATE INIT)

        # test underflow
        
         self.level = self.set(LIT401, 0.9)
         self.set(P301, 0)
         self.set(MV302,0)
        # self.level = self.set(LIT101, 0.500)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            
            new_level = self.level
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            mv302 = self.get(MV302)
            p301 = self.get(P301)
            mv501 = self.get(MV501)
            logging.debug('\t\tcount %d', count)
            if int(mv302) == 1 and int(p301) == 1 :                
                #self.set(FIT301, UFF_PUMP_FLOWRATE_IN)
                inflow = ROF_PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank inflow: ", inflow
                water_volume += inflow
                #print 'water_volume: %f' %water_volume
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
                # print "DEBUG RawWaterTank outflow: ", outflow
                water_volume -= outflow
                #print 'water_volume: %f' %water_volume
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
            logging.debug('\t\t\t\t\tROFTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LIT401, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)

class NaHSO3Tank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.level = self.set(LS401, 0.800)
        
        # SPHINX_SWAT_TUTORIAL STATE INIT)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            new_level = self.level
            p403 = self.get(P403)
            p401 = self.get(P401)
            p501 = self.get(P501)
            mv501 = self.get(MV501)
            
            nahso3_volume = self.section * new_level
            logging.debug('\t\tcount %d', count)
            if int(p403) == 1 and int(p501)==1 and int(mv501)==1 :
                outflow = NaHSO3_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                #print ' outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS %f = %f * %f' %(outflow, PUMP_FLOWRATE_OUT ,PP_PERIOD_HOURS)
                # print "DEBUG RawWaterTank outflow: ", outflow
                nahso3_volume -= outflow

            # compute new hcl_level
            new_level = nahso3_volume / self.section
           
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('\t\t\t\t\t\tNaHSO3Tank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS401, new_level)

            if int(p401) ^ int(p403):
                self.set(P403,p401)

            count += 1
            time.sleep(PP_PERIOD_SEC)

class ROPWaterTank(Tank):

    #def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
       
        # SPHINX_SWAT_TUTORIAL STATE INIT)

        # test underflow
        # self.set(MV101, 0)
        # self.set(P101, 1)
        # self.level = self.set(LIT101, 0.500)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):
            
            new_level = self.level
            # compute water volume
            water_volume = self.section * new_level
            # inflows volumes
            mv501 = self.get(MV501)
            p401 = self.get(P401)
            p501 = self.get(P501)
            logging.debug('\t\tcount %d', count)
            if int(mv501) == 1 and int(p401)==1 and int(mv501)==1:
                
                #self.set(FIT301, UFF_PUMP_FLOWRATE_IN)
                inflow = ROP_PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank inflow: ", inflow
                water_volume += inflow
                #print 'water_volume: %f' %water_volume
                

            # outflows volumes
            p601 = self.get(P601)
            if int(p601) == 1:
                outflow = ROP_PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank outflow: ", outflow
                water_volume -= outflow
                #print 'water_volume: %f' %water_volume

            # compute new water_level
            new_level = water_volume / self.section
            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            logging.debug('\t\t\t\t\t\t\tROPTank new level %f with delta %f', new_level, new_level -self.level)
            self.level = self.set(LS601, new_level)

            count += 1
            time.sleep(PP_PERIOD_SEC)

if __name__ == '__main__':

    logging.basicConfig(filename='logs/physicalProc.log', encoding ='utf-8', level=logging.DEBUG)

    rwt = threading.Thread(target=RawWaterTank,
        kwargs={
            'name':'rwt', 
            'state': STATE, 
            'protocol': None,
            'section': TANK_SECTION,
            'level': RWT_INIT_LEVEL
            })
    
    naclt = threading.Thread(target=NaClTank, 
       kwargs={
            'name': 'naclt',
            'state': STATE,
            'protocol': None,
            'section': NaCl_TANK_SECTION,
            'level': NACLT_INIT_LEVEL
            })

    hclt = threading.Thread(target=HClTank,
        kwargs={
            'name':'hclt',
            'state': STATE,
            'protocol': None,
            'section': HCl_TANK_SECTION,
            'level': HCLT_INIT_LEVEL
            })
    
    naoclt = threading.Thread(target=NaOClTank,
        kwargs={
            'name': 'naoclt',
            'state': STATE,
            'protocol': None,
            'section': NaOCl_TANK_SECTION,
            'level': NAOCLT_INIT_LEVEL
            })

    ufft = threading.Thread(target=UFFWaterTank,
        kwargs={
            'name':'ufft', 
            'state': STATE, 
            'protocol': None,
            'section': UFF_TANK_SECTION,
            'level': UFFT_INIT_LEVEL
            }) 

    roft = threading.Thread(target=ROFWaterTank,
        kwargs={
            'name':'roft', 
            'state': STATE, 
            'protocol': None,
            'section': ROF_TANK_SECTION,
            'level': ROFT_INIT_LEVEL
            })  

    nahso3t = threading.Thread(target=NaHSO3Tank,
        kwargs={
            'name': 'nahso3t',
            'state': STATE,
            'protocol': None,
            'section': NaHSO3_TANK_SECTION,
            'level': NAHSO3T_INIT_LEVEL
            })        

    ropt = threading.Thread(target=ROPWaterTank,
        kwargs={
            'name':'ropt', 
            'state': STATE, 
            'protocol': None,
            'section': ROP_TANK_SECTION,
            'level': ROPT_INIT_LEVEL
            }) 
    
    
    rwt.start()
    naclt.start()
    hclt.start()
    naoclt.start()
    ufft.start()
    roft.start()
    nahso3t.start()
    ropt.start()
    rwt.join()
    naclt.join()
    hclt.join()
    naoclt.join() 
    ufft.join()
    roft.join()
    nahso3t.join()
    ropt.join()
