import tkinter as tk
import time
import threading
import sqlite3

#from  utils import TANK_HEIGHT, HCl_TANK_HEIGHT,NaCl_TANK_HEIGHT,NaOCl_TANK_HEIGHT
#from  utils import UFF_TANK_HEIGHT, ROF_TANK_HEIGHT,NaHSO3_TANK_HEIGHT,ROP_TANK_HEIGHT

TANK_HEIGHT = 1.600               # m
HCl_TANK_HEIGHT = 1.750           # m
NaCl_TANK_HEIGHT = 1.750          # m
NaOCl_TANK_HEIGHT = 1.750         # m
UFF_TANK_HEIGHT = 1.600           # m
ROF_TANK_HEIGHT = 1.600           # m
NaHSO3_TANK_HEIGHT = 1.750        # m
ROP_TANK_HEIGHT = 1.24            # m

class SwatGui:

    def __init__(self):
         
        widthTank = 70
        heightTank = 150
        RawTankLevel=.1
        NaClTankLevel=.1
        HClTankLevel=.1
        NaOClTankLevel=.1
        UFFTankLevel=.1
        NaHSO3TankLevel=.1
        ROFTankLevel=.1
        ROPTankLevel=.1
        
        MV101 = 0
        MV201 = 0
        MV302 = 0 
        MV501 = 0

        P101 = 0
        P201 = 0
        P201 = 0
        P203 = 0
        P205 = 0
        P301 = 0
        P401 = 0
        P403 = 0
        P501 = 0 
        P601 = 0


        self.window = tk.Tk()
        canvas = tk.Canvas(self.window, width=6000, height=10000)
        canvas.pack()


        ###############################################
        #################   PROCESS 1  ################
        ###############################################

        #Pipe
        canvas.create_rectangle(20,80, 80, 100)

        #RawWaterTank
        canvas.create_rectangle(80,30,80+widthTank, 30 + heightTank )
        canvas.create_rectangle(80,30+((1-RawTankLevel)*heightTank),80+widthTank, 30 +heightTank,fill='blue', tag= "rwt")
        canvas.create_line(75,30+(0.25*heightTank),85+widthTank,30+(0.25*heightTank) ,fill='red')
        canvas.create_line(75,30+(0.75*heightTank),85+widthTank,30+(0.75*heightTank) ,fill='red')
        RawTankLabel = canvas.create_text((110, 15), text="Raw Water Tank", tag = 'rwtl')

        #MV101
        canvas.create_rectangle(0,80-MV101, 30, 100-MV101, fill= 'black', tag = 'mv101')
        mv101Label = canvas.create_text((25, 60-MV101), text="MV101", tag = 'mv101l')

        #Pipe
        canvas.create_rectangle(150,150, 450, 170)
        #P101
        canvas.create_rectangle(100,150-P101, 170, 170-P101, fill= 'black', tag = 'p101')
        mv101Label = canvas.create_text((180, 130-P101), text="P101", tag = 'p101l')


        ###############################################
        #################   PROCESS 2  ################
        ###############################################


        #NaClTank
        canvas.create_rectangle(180,200,180+widthTank, 200 + heightTank )
        canvas.create_rectangle(180,200+((1-NaClTankLevel)*heightTank),180+widthTank, 200 +heightTank,fill='blue',tag = 'nacl')
        canvas.create_line(175,200+(0.75*heightTank),185+widthTank,200+(0.75*heightTank)  ,fill='red')
        canvas.create_line(175,200+(0.25*heightTank),185+widthTank,200+(0.25*heightTank)  ,fill='red')
        NaClLabel = canvas.create_text((215, 370), text="NaCl Tank", tag= 'nacll')

        #Pipe
        canvas.create_rectangle(190,170, 210, 200)
        #P201
        canvas.create_rectangle(190+P201,180, 210+P201, 190, fill= 'black', tag = 'p201')
        p201Label = canvas.create_text((230+P201, 185), text="P201", tag = 'p201l')

        #HClTank
        canvas.create_rectangle(260,200,260+widthTank, 200 + heightTank )
        canvas.create_rectangle(260,200+((1-HClTankLevel)*heightTank),260+widthTank, 200 +heightTank,fill='blue', tag= 'hcl')
        canvas.create_line(255,200+(0.75*heightTank),265+widthTank,200+(0.75*heightTank)  ,fill='red')
        canvas.create_line(255,200+(0.25*heightTank),265+widthTank,200+(0.25*heightTank)  ,fill='red')
        HClLabel = canvas.create_text((295, 380), text="HCl Tank", tag = 'hcll')

        #Pipe
        canvas.create_rectangle(270,170, 290, 200)
        #P203
        canvas.create_rectangle(270+P203,180, 290+P203, 190, fill= 'black', tag = 'p203')
        p203Label = canvas.create_text((310+P203, 185), text="P203", tag = 'p203l')
 
        #NaOCl
        canvas.create_rectangle(340,200,340+widthTank, 200 + heightTank )
        canvas.create_rectangle(340,200+((1-NaOClTankLevel)*heightTank),340+ widthTank, 200 +heightTank,fill='blue', tag = 'naocl')
        canvas.create_line(335,200+(0.75*heightTank),345+widthTank,200+(0.75*heightTank)  ,fill='red')
        canvas.create_line(335,200+(0.25*heightTank),345+widthTank,200+(0.25*heightTank)  ,fill='red')
        NaOClLabel = canvas.create_text((375, 370), text="NaOcl Tank", tag = 'naocll')

        #Pipe
        canvas.create_rectangle(350,170, 370, 200)
        #P205
        canvas.create_rectangle(350+P205,180, 370+P205, 190, fill= 'black', tag = 'p205')
        p205Label = canvas.create_text((390+P205, 185), text="P205", tag = 'p205l')

        #MV201
        canvas.create_rectangle(400,150-MV201, 410, 170-MV201, fill= 'black', tag = 'mv201')
        mv201Label = canvas.create_text((420, 130-MV201), text="MV201", tag = 'mv201l')

        ###############################################
        #################   PROCESS 3  ################
        ###############################################
        
        #UFFeedTank
        canvas.create_rectangle(450,30,450+widthTank, 30 + heightTank )
        canvas.create_rectangle(450,30+((1-UFFTankLevel)*heightTank),450+widthTank, 30 +heightTank,fill='blue', tag = 'uff')
        canvas.create_line(445,30+(0.25*heightTank),455+widthTank,30+(0.25*heightTank) ,fill='red')
        canvas.create_line(445,30+(0.75*heightTank),455+widthTank,30+(0.75*heightTank) ,fill='red')
        RawTankLabel = canvas.create_text((480, 15), text="UF Feed Tank", tag = 'uffl')

        #Pipe
        canvas.create_rectangle(520,150, 620, 170)
        #P301
        canvas.create_rectangle(540,150-P301, 550, 170-P301, fill= 'black', tag = 'p301')
        P301Label = canvas.create_text((540, 130-P301), text="P301", tag = 'p301l')

        #MV302
        canvas.create_rectangle(580,150-MV302, 590, 170-MV302, fill= 'black', tag = 'mv302')
        MV302Label = canvas.create_text((595, 130-MV302), text="MV302", tag = 'mv302l')

        ###############################################
        #################   PROCESS 4  ################
        ###############################################

        #ROFeedTank
        canvas.create_rectangle(620,30,620+widthTank, 30 + heightTank )
        canvas.create_rectangle(620,30+((1-ROFTankLevel)*heightTank),620+widthTank, 30 +heightTank,fill='blue', tag = 'rof')
        canvas.create_line(615,30+(0.25*heightTank),625+widthTank,30+(0.25*heightTank) ,fill='red')
        canvas.create_line(615,30+(0.75*heightTank),625+widthTank,30+(0.75*heightTank) ,fill='red')
        RawTankLabel = canvas.create_text((650, 15), text="ROF Tank", tag = 'rofl')

        #Pipe
        canvas.create_rectangle(690,150, 980, 170)
        #P401
        canvas.create_rectangle(710,150-P401, 720, 170-P401, fill= 'black', tag = 'p401')
        P401Label = canvas.create_text((730, 130-P401), text="P401", tag = 'p401l')

        #NaHSO3Tank
        canvas.create_rectangle(710,200,710+widthTank, 200 + heightTank )
        canvas.create_rectangle(710,200+((1-NaHSO3TankLevel)*heightTank),710+widthTank, 200 +heightTank,fill='blue', tag= 'nahso3')
        canvas.create_line(705,200+(0.25*heightTank),715+widthTank,200+(0.25*heightTank) ,fill='red')
        canvas.create_line(705,200+(0.75*heightTank),715+widthTank,200+(0.75*heightTank) ,fill='red')
        NaClLabel = canvas.create_text((745, 360), text="NaHSO3 Tank", tag= 'nahso3l')

        #Pipe
        canvas.create_rectangle(730,170, 750, 200)
        #P403
        canvas.create_rectangle(730+P403,180, 750+P403, 190, fill= 'black', tag = 'p403')
        p403Label = canvas.create_text((770+P403, 185), text="P403", tag = 'p403l')

        ###############################################
        #################   PROCESS 5  ################
        ############################################### 

        #P501
        p501=canvas.create_rectangle(810,150-P501, 820, 170-P501, fill= 'black', tag = 'p501')
        P501Label = canvas.create_text((830, 130-P501), text="P501", tag = 'p501l')

        #MV501
        canvas.create_rectangle(900,150-MV501, 910, 170-MV501, fill= 'black', tag = 'mv501')
        P301Label = canvas.create_text((920, 130-MV501), text="MV501", tag = 'mv501l')

        ###############################################
        #################   PROCESS 6  ################
        ###############################################

        #ROPTank
        canvas.create_rectangle(980,30,980+widthTank, 30 + heightTank )
        canvas.create_rectangle(980,30+((1-ROPTankLevel)*heightTank),980+widthTank, 30 +heightTank,fill='blue', tag='rop')
        canvas.create_line(975,30+(0.25*heightTank),985+widthTank,30+(0.25*heightTank) ,fill='red')
        canvas.create_line(975,30+(0.75*heightTank),985+widthTank,30+(0.75*heightTank) ,fill='red')
        RawTankLabel = canvas.create_text((1020, 15), text="RO Permeate Tank", tag = 'ropl')

        #Pipe
        canvas.create_rectangle(1050,150, 1100, 170)
        #P601
        canvas.create_rectangle(1070,150-P601, 1080, 170-P601, fill= 'black', tag = 'p601')
        P401Label = canvas.create_text((1090, 130-P601), text="P601", tag = 'p601l')
    
        while 1 :
            
            with sqlite3.connect("swat_s1_db.sqlite") as conn:
                try:
                    cursor = conn.cursor()
                    #print("SELECT value FROM swat_s1 where name = 'MV101'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'MV101'", )
                    MV101 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'LIT101'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LIT101'", )
                    RawTankLevel =float(cursor.fetchone()[0]) / TANK_HEIGHT

                    #print("SELECT value FROM swat_s1 where name = 'P101'")
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P101'", )
                    P101 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'LS201'")
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LS201'", )
                    NaClTankLevel = float(cursor.fetchone()[0]) / NaCl_TANK_HEIGHT

                    #print("SELECT value FROM swat_s1 where name = 'P201'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P201'", )
                    P201 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'LS202'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LS202'", )
                    HClTankLevel = float(cursor.fetchone()[0]) / HCl_TANK_HEIGHT

                    #print("SELECT value FROM swat_s1 where name = 'P203'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P203'", )
                    P203 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'LS203'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LS203'", )
                    NaOClTankLevel = float(cursor.fetchone()[0]) / NaOCl_TANK_HEIGHT

                    #print("SELECT value FROM swat_s1 where name = 'P205'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P205'", )
                    P205 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'MV201'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'MV201'", )
                    MV201 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'MV302'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'MV302'", )
                    MV302 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'LIT301'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LIT301'", )
                    UFFTankLevel = float(cursor.fetchone()[0]) / UFF_TANK_HEIGHT

                    #print("SELECT value FROM swat_s1 where name = 'P301'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P301'", )
                    P301 = int(cursor.fetchone()[0])*20
                    
                   # print("SELECT value FROM swat_s1 where name = 'LIT401'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LIT401'", )
                    ROFTankLevel = float(cursor.fetchone()[0]) / ROF_TANK_HEIGHT

                   # print("SELECT value FROM swat_s1 where name = 'P401'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P401'", )
                    P401 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'LS401'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LS401'", )
                    NaHSO3TankLevel = float(cursor.fetchone()[0]) / NaHSO3_TANK_HEIGHT

                    #print("SELECT value FROM swat_s1 where name = 'P403'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P403'", )
                    P403 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'P501'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P501'", )
                    P501 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'MV501'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'MV501'", )
                    MV501 = int(cursor.fetchone()[0])*20

                    #print("SELECT value FROM swat_s1 where name = 'LS601'", )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'LS601'", )
                    ROPTankLevel=float(cursor.fetchone()[0]) / ROP_TANK_HEIGHT

                    # print("SELECT value FROM swat_s1 where name = 'P601'" )
                    cursor.execute("SELECT value FROM swat_s1 where name = 'P601'", )
                    P601 = int(cursor.fetchone()[0])*20
                except sqlite3.Error as e:
                    print('_get ERROR: %s: ' % e.args[0])
            
            #MV101 update
            canvas.coords('mv101',20,80-MV101, 30, 100-MV101)
            canvas.coords('mv101l',(25, 60-MV101))
            
            #RawWaterTank update
            canvas.coords('rwt',80,30+((1-RawTankLevel)*heightTank),80+widthTank, 30 +heightTank)
            canvas.itemconfig('rwtl', text = str("Raw Tank"+str(round(RawTankLevel*TANK_HEIGHT,3))))

            #P101 update
            canvas.coords('p101',160,150-P101, 170, 170-P101)
            canvas.coords('p101l',(180, 130-P101))

            #NaClWaterTank update
            canvas.coords('nacl',180,200+((1-NaClTankLevel)*heightTank),180+widthTank, 200 +heightTank)
            canvas.itemconfig('nacll', text = str("NaCl Tank\n"+str(round(NaClTankLevel*NaCl_TANK_HEIGHT,3))))
            
            #P201 update
            canvas.coords('p201',190+P201,180, 210+P201, 190)
            canvas.coords('p201l',(230+P201, 185))

            #HClWaterTank update
            canvas.coords('hcl',260,200+((1-HClTankLevel)*heightTank),260+widthTank, 200 +heightTank)
            canvas.itemconfig('hcll', text = str("HCl Tank\n\n"+str(round(HClTankLevel*HCl_TANK_HEIGHT,3))))

            #P203 update
            canvas.coords('p203',270+P203,180, 290+P203, 190)
            canvas.coords('p203l',(310+P203, 185))

            #NaOClWaterTank update
            canvas.coords('naocl', 340,200+((1-NaOClTankLevel)*heightTank),340+ widthTank, 200 +heightTank)
            canvas.itemconfig('naocll', text = str("NaOCl Tank\n"+str(round(NaOClTankLevel*NaOCl_TANK_HEIGHT,3))))
            
            #P205 update
            canvas.coords('p205',350+P205,180, 370+P205, 190)
            canvas.coords('p205l',(390+P205, 185))

 
           #mv201 update
            canvas.coords('mv201',400,150-MV201, 410, 170-MV201)
            canvas.coords('mv201l',(420, 130-MV201))

            #UFFWaterTank update
            canvas.coords('uff',450,30+((1-UFFTankLevel)*heightTank),450+widthTank, 30 +heightTank)   
            canvas.itemconfig('uffl', text = str("UFF Tank"+str(round(UFFTankLevel*UFF_TANK_HEIGHT,3))))

            #P301 update
            canvas.coords('p301',540,150-P301, 550, 170-P301)
            canvas.coords('p301l',(540, 130-P301))

            #mv302 update
            canvas.coords('mv302',580,150-MV302, 590, 170-MV302)
            canvas.coords('mv302l',(595, 130-MV302))

            #ROFWaterTank update
            canvas.coords('rof',620,30+((1-ROFTankLevel)*heightTank),620+widthTank, 30 +heightTank)
            canvas.itemconfig('rofl', text = str("ROF Tank"+str(round(ROFTankLevel*ROF_TANK_HEIGHT,3))))

            #P401 update
            canvas.coords('p401',710,150-P401, 720, 170-P401)
            canvas.coords('p401l',(730, 130-P401))

            #NaHSO3WaterTank update
            canvas.coords('nahso3',710,200+((1-NaHSO3TankLevel)*heightTank),710+widthTank, 200 +heightTank)
            canvas.itemconfig('nahso3l', text = str("NaHSO3 Tank "+str(round(NaHSO3TankLevel*NaHSO3_TANK_HEIGHT,3))))
            
            #P403 update
            canvas.coords('p403',730+P403,180, 750+P403, 190)
            canvas.coords('p403l',(770+P403, 185))

            #P501 update
            canvas.coords('p501',810,150-P501, 820, 170-P501)
            canvas.coords('p501l',(830, 130-P501))
            
            #MV501 update
            canvas.coords('mv501',900,150-MV501, 910, 170-MV501)
            canvas.coords('mv501l',(920, 130-MV501))
            
            #ROPWaterTank update
            canvas.coords('rop',980,30+((1-ROPTankLevel)*heightTank),980+widthTank, 30 +heightTank)
            canvas.itemconfig('ropl', text = str("ROP Tank "+str(round(ROPTankLevel*ROP_TANK_HEIGHT,3))))
            
            #P501 update
            canvas.coords('p601',1070,150-P601, 1080, 170-P601)
            canvas.coords('p601l',(1090, 130-P601))

            self.window.update_idletasks()
            time.sleep(0.4)

if __name__ == '__main__':
    app = SwatGui() 
    i=1
    while i==1:
        i=1
