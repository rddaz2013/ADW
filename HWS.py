# -*- coding:utf-8 -*-
"""
Created on 06.06.2011

@author: rened
@version:
"""
__author__ = "Rene Dworschak"
__copyright__ = "Copyright 2015, The WL/CO Project"
__credits__ = ["MG", "Inburex"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Rene Dworschak"
__email__ = "r7.dworschak@googlemail.com"
__status__ = "Dev"

import sys

plat={"win32":"\r\n","linux":"\n","linux2":"\n"}
platform = sys.platform
print platform        
from time import sleep

import time
import threading
from threading import Thread,Lock
from Queue import Queue

import numpy as N
from helper.regler import PID
from helper.AuswertH import read_array2, GetData

import platform

DatenQueue = Queue()
SPQueue = Queue()
lock = Lock()

class I7017_Getdata(Thread):
    def __init__ (self,ip,port,delta_temp):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.status = 1
        self.pid = 1.
        self.running = True
        self.delta_temp=delta_temp
        self.kick = 0
        self.stoprequest = threading.Event()
        self.plat={"win32":"\r","linux":"\n","linux2":"\n"}
        self.platform = sys.platform
        self.PID_Error = 0.
        self.SP_Point = 0.


    def change_delta(self,new_temp):
        self.delta_temp = new_temp
    
    def stop_Rec(self):
        self.running = False
        
    def join(self, timeout=None):
        #print ' Data_Ende '
        self.stoprequest.set()

    def run(self):
        if platform.system()=='Windows':
             starttime = time.clock()

        if platform.system()=='Linux':
             starttime = time.time()
        
        step=0
        now_time=0
        # Aenderung von p1=PID(2,3/160,4/40)
        p1=PID(3,3/160,50)
        while self.status==1:
            # Checking State
            step = step +1
            time.sleep(5.)

            #Daten ueber IP besorgen
            lock.acquire()
            daten_IP = GetData(self.ip,self.port,"#02"+chr(13))
            #print daten_IP
            lock.release()
            time.sleep(2.)

            lock.acquire()
            data_Linseis   = GetData('192.168.8.190',10001,'DATA'+chr(13))
            #print data_Linseis   
            lock.release()

            if data_Linseis[0] != 'A':
                    my_Linseis    = N.dtype([('Value1', 'int'),('Value2', 'int'),('Value3', 'int'),('Value4', 'int'),('Value5', 'int'),('Value6', 'int'),
                                             ('Value7', 'int'),('Value8', 'int'),('Value9', 'int'),('Value10', 'int'),('Value11', 'int'),('Value12', 'int'),
                                             ('Value13', 'int'),('Value14', 'int'),('Value15', 'int'),('Value16', 'int'),('Value17', 'int'),('Value18', 'int'),
                                             ('Value19', 'int'),('Value20', 'int'),('Value21', 'int'),('Value22', 'int'),('Value23', 'int'),('Value24', 'int'),
                                             ('Value25', 'int'),('Value26', 'int'),('Value27', 'int'),('Value28', 'int'),('Value29', 'int'),('Value30', 'int'),
                                             ('Value31', 'int'),('Value32', 'int'),('Value33', 'int'),('Value34', 'int'),('Value35', 'int'),('Value36', 'int')])

                    if data_Linseis[0] !='T':
                        Linseis = read_array2(data_Linseis, my_Linseis,separator=',')

            # echte Zeit als Datensatz verwenden, da die Übertragung eventuell gestört sein könnte

            if platform.system()=='Windows':
                now_time = time.clock() -starttime

            if platform.system()=='Linux':
                now_time = time.time() -starttime

            # Formatierung des Datenstring + Zeitstempel
            data_str= '%.1f ; %.1f %s '%(now_time,self.delta_temp+self.kick,daten_IP)
            #print data_str
            data_str= data_str.replace('+',' ; +')
            data_str= data_str.replace('-',' ; -')

            # Fuer Debug-Zwecke Daten nochmal auf die Konsole posten
            #print Linseis[0][0]

            #T1 - Ofenheizung
            #T2 - Probe Halb
            #T3 - Probe Mitte
            #T4 - Abluft-Temp
            
            #T5 - T8 Ofenelemente
            # CO-Rechnungswert (Umrechnung muss erfolgen)
            mydescr = N.dtype([('Zeit', 'float'), ('Delta', 'float'),('T1', 'float'), ('T2', 'float'), ('T3', 'float'),('T4', 'float'),('T5', 'float'), ('T6', 'float'), ('T7', 'float'),('T8', 'float')])
            myrecarray = read_array2(data_str, mydescr)

            # T3 Probe
            # T4 Regelthermoelement
            # T1 Heizung
            # T7 Probe Rand
            # T2 Probe Halb


            # Änderung des PID reglers
            # wenn myrecarray['T3'][0]+self.delta_temp > myrecarray['T4'][0]
            # dann neuen Setpoint ..sonst nur updaten.
            Check_delta = myrecarray['T1'][0] - myrecarray['T3'][0]
            # Änderung myrecarray['T4'][0] ist jetzt Ablufttemp!!.
            Med_Temp = (myrecarray['T8'][0] +5 +myrecarray['T6'][0])/2

            # Aenderung keine Kickwert-Mehr
            # Wenn die all. Ofentemperatur die Probentemperatur unterschreitet
            # ein wenig mehr Temperaturoffset und schneller Nachregeln
            #if myrecarray['T1'][0]>50:
            #    if (Med_Temp-5) < ((myrecarray['T3'][0]+myrecarray['T2'][0])/2):
            #        self.kick = self.kick + 1
            #        p1.setKp(3)
            #        p1.setKi(3/160)
            #        if self.kick > 50:
            #            self.kick = 50
            #    else:
            #        self.kick = 0


            p1.setPoint2(self.delta_temp + self.kick)
            self.PID_Error = p1.update(Check_delta)
            SP_Point = (myrecarray['T3'][0] + self.delta_temp + self.kick + self.PID_Error)

            if SP_Point<10:
                SP_Point = 10
            if SP_Point>350:
                SP_Point=350

            #print SP_Point,PID_Error,Check_delta,self.kick,Med_Temp

            data_str1= '%s ; %.1f'%(data_str[:len(data_str)-2],Linseis[0][1])
            #print Linseis[0][0],Linseis[0][1]
            SPQueue.put(SP_Point)
            DatenQueue.put(data_str1+self.plat[self.platform])

            print data_str1+self.plat[self.platform]
            #print step, data_str1

            if step > 2000000:
                DatenQueue.put('STOP')
                SPQueue.put('STOP')
                self.status=0
            #    #DatenQueue
                self.join()
        print 'Main-Thread_Ende'


class Save_data(Thread):
    def __init__ (self,filename,probe,data_me):
        Thread.__init__(self)
        self.filename = filename
        self.probe = probe
        self.data_me = data_me
        self.status = 0
        self.running = True
        self.datastr = ''
        self.stoprequest = threading.Event()
        self.plat={"win32":"\r","linux":"\n","linux2":"\n"}
        self.platform = sys.platform
        
        # Datenkopfschreiben
        savefile=open(self.filename, 'a')

        savefile.write('" Probenname : '+probe+self.plat[self.platform])
        savefile.write('" Datum : '+time.strftime("%d.%m.%Y um %H:%M:%S Uhr")+self.plat[self.platform])
        savefile.write('" ------------------------------------------------'+self.plat[self.platform])
        savefile.write('"1 : Zeit in Sekunden'+self.plat[self.platform])
        savefile.write('"2 : Temperaturdifferenz zwischen Ofen und Probe (die Regelgröße NICHT die tatsächliche Differenz)'+self.plat[self.platform])
        savefile.write('"3 : T1 Ofentemperatur direkt an der Heizung'+self.plat[self.platform])
        savefile.write('"4 : T2 Temperatur in der Probenhälfte'+self.plat[self.platform])
        savefile.write('"5 : T3 Temperatur in der Probenmitte'+self.plat[self.platform])
        savefile.write('"6 : T4 Ablufttemperatur'+chr(10))
        savefile.write('"7 : T5 Temperatur irgendwo im Ofenraum'+self.plat[self.platform])
        savefile.write('"8 : T6 Temperatur irgendwo im Ofenraum'+self.plat[self.platform])
        savefile.write('"9 :  T7 Temperatur irgendwo im Ofenraum'+self.plat[self.platform])
        savefile.write('"10 : frei'+chr(10))
        savefile.write('"11 : CO-Wert (muss noch umgerechnet werden)'+self.plat[self.platform])
        savefile.write('" ---Keine Steuerung--------------------------------'+self.plat[self.platform])
        savefile.close()
        
    def join(self, timeout=None):     
        self.stoprequest.set()

    def stop_Rec(self):
        self.running = False

    def run(self):
        
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stoprequest.isSet():
            try:
                self.datastr = DatenQueue.get(True,timeout=25)
                if self.datastr<>'STOP':
                    savefile=open(self.filename, 'a')
                    savefile.write(self.datastr.strip()+self.plat[self.platform])
                    savefile.close()
                    #print self.datastr.strip()
                else:
                    self.join() 
                   
                self.status=0
                
                #dirname = self.dir_q.get(True, 0.05)
                #filenames = list(self._files_in_dir(dirname))
                #self.result_q.put((self.name, dirname, filenames))
            except Queue.empty:
                pass
        print ' Save_Ende '
            
class Set_SP(Thread):
    def __init__ (self):
        Thread.__init__(self)
        self.status = 0.
        self.running = True
        self.datastr=0.
        self.datastr_dummy=0.
        self.Value=0.
        self.OldData=0.
        self.plat={"win32":"\r","linux":"\n","linux2":"\n"}
        self.platform = sys.platform
        self.stoprequest = threading.Event()

        if platform.system()=='Windows':
             self.starttime0 = time.clock()

        if platform.system()=='Linux':
             self.starttime0 = time.time()

        #self.Prog = [3000,40]

    def join(self, timeout=None):
        self.stoprequest.set()

    def run(self):
        self.datastr = 40.0
        while not self.stoprequest.isSet():
            try:
                if platform.system()=='Windows':
                    self.starttime1 = time.clock()
                if platform.system()=='Linux':
                    self.starttime1 = time.time()

                self.datastr_dummy = SPQueue.get(True,timeout=15)

                if (self.starttime1-self.starttime0)>2*60*60:
                    self.datastr = SPQueue.get(True,timeout=15)
                    self.datastr = self.datastr + 20.
                    self.starttime0 = self.starttime1

                if self.datastr<>'STOP':
                    self.Value = '#010%0.3f'%(((self.datastr+1.4)/28.677)*0.70)
                else:
                    self.join()

                # Umrechnen'X' auf Spannung
                #self.Value = '#010%0.3f'%((self.datastr+1.4)/28.677)
                # Prüfung dass 10V nicht überschritten wird
               
                
                if self.Value<>self.OldData:
                    lock.acquire()
                    test = GetData('192.168.8.190',10002,self.Value+chr(13))
                    lock.release()
                    
                    self.OldData=self.Value
                sleep(3.0)
                    
            except Queue.empty:
                pass
               #self.join()

            print ' SP_Ende '

# default adresse of the I-7188E is 192.168.255.1
# for LAN-Inburex umgestellt
HOST = '192.168.8.190'    # The remote host
PORT = 10000              # The same port as used by the server
PORT_COM = 10002

"""
Datakomunikation mit dem I-7188E Hauptmodul über Port 10000
Datakomunikation mit dem I-7188E Slavemodulen über Port 10002
(Temperaturmessung und Temperatursteuerung)
"""

#print GetData('192.168.8.190',10000,'10')
#print GetData('192.168.8.190',10002,'$01M'+chr(13))
#print GetData('192.168.8.190',10002,'$02M'+chr(13))
#print GetData('192.168.8.190',10002,'$02M'+chr(13))

""" Ausgangsspannung fuer die Ofenregelung auf 0 setzen"""
print GetData('192.168.8.190',10000,'01'+chr(13))

from vorlage import *
the= I7017_Getdata(HOST ,PORT_COM ,temp_diff)
""" Dateiname + Headerkommentar """
the_2=Save_data(datei_name,datei_beschreib,'adiabate Messung+CO')

""" Aktiviert die Software PID Regelung
    Die Hardwareregelung des Warmlagerofens ist immer aktiv
"""
the_3=Set_SP()
""" Threads starten """
the.start()
the_2.start()
the_3.start()

print GetData('192.168.8.190',10002,'#0100.000'+chr(13))
print "Done!"
