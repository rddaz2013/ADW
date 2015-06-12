# -*- coding:utf-8 -*-
"""
Created on 31.05.2011

@author: rened
"""
from  scipy.integrate import simps

from  helper.AuswertH import *
from  vorlage import *

def plot_kin_dat(filename,factor):
    mydescr = N.dtype([('Zeit', 'float'), ('Delta', 'float'),('T1', 'float'), ('T2', 'float'), ('T3', 'float'),('T4', 'float'),('T5', 'float'), ('T6', 'float'), ('T7', 'float'),('T8', 'float'),('CO', 'float')])
    myrecarray = read_array(filename, mydescr)
    timeline  = myrecarray['Zeit']
    
    T1 = myrecarray['T1']
    T2 = myrecarray['T2']
    T3 = myrecarray['T3']
    T4 = myrecarray['T4']
    T5 = myrecarray['T5']
    T6 = myrecarray['T6']
    T7 = myrecarray['T7']
    T8 = myrecarray['T8']
    
    timeline_d = savitzky_golay(myrecarray['Zeit'], window_size=31, order=3,deriv=1)  
    T3_d = savitzky_golay(myrecarray['T3'], window_size=31, order=3,deriv=1)  
     
    Ableit = T3_d/timeline_d
    
    p.xlabel(r"1000/Temp [K]", fontsize = 12)
    #p.ylabel(r"ln [K/s / T]", fontsize = 12)
    p.ylabel(r"ln [K/s]", fontsize = 12)

    #p.plot(1000/(T3+273.)[1:],N.log(Ableit/(T3+273.15)[1:])*factor,lw=2,label=filename)
    p.plot(1000./(T3+273.15),N.log(Ableit)*factor,lw=2,label=filename)
    #p.legend(bbox_to_anchor=(0.75, 0.55), loc=2, borderaxespad=0.)
    #p.plot(1000/(T2+273.)[1:],N.log(Ableit2/(T2+273.15)[1:]),'k--',lw=2)
    #af =  AnnoteFinder(1000/(T3+273.)[1:],N.log(Ableit/(T3+273.15)[1:]), T3[1:])
    #p.connect('button_press_event', af)
    #p.show()

    
def plot_time_dat(filename,offset):
    mydescr = N.dtype([('Zeit', 'float'), ('Delta', 'float'),('T1', 'float'), ('T2', 'float'), ('T3', 'float'),('T4', 'float'),('T5', 'float'), ('T6', 'float'), ('T7', 'float'),('T8', 'float'),('CO', 'float')])
    myrecarray = read_array(filename, mydescr)
    timeline  = myrecarray['Zeit']
    
    T1 = myrecarray['T1']
    T2 = myrecarray['T2']
    T3 = myrecarray['T3']
    T4 = myrecarray['T4']
    T5 = myrecarray['T5']
    T6 = myrecarray['T6']
    T7 = myrecarray['T7']
    T8 = myrecarray['T8']
    CO = myrecarray['CO']
    
    p.xlabel(r"Time [s]", fontsize = 12)
    p.ylabel(r"Temp [Celsius]", fontsize = 12)
    #p.plot(timeline,CO_Value(CO),lw=2)
   # p.plot(timeline,T2,lw=2)
    p.plot(timeline+offset,T3,lw=2)
    #p.plot(timeline+offset,T1,lw=2)
    #p.plot(timeline+offset,T5,lw=2)
    #p.plot(timeline+offset,T6,lw=2)
    #p.plot(timeline+offset,T5,lw=2)
    p.plot(timeline+offset,T1,lw=2)
    #p.plot(timeline+offset,T8,lw=2)
    #p.plot(timeline,T5,lw=2)
    
    #p.plot(timeline,T3,lw=2,label=filename)
    #data=column_stack((timeline,T3))
    #savetxt('temp.txt', data, delimiter=',',fmt='%0.8e')  
    #p.legend(bbox_to_anchor=(0.55, 0.95), loc=2, borderaxespad=0.)


    
    #print integrate_Peak(timeline,CO_Value(CO),350,550)
    #print integrate_Peak(timeline,CO_Value(CO),160000,265000)
    #print integrate_Peak(timeline,CO_Value(CO),424800,425200)
    #print integrate_Peak(timeline,CO_Value(CO),67600,67900)
    #print integrate_Peak(timeline,CO_Value(CO),38800,50300)

datei_name = "../Test60.asc"
plot_time_dat(datei_name,0)

#datei_name = "Stahl_60.asc" # alter T60 Versuch andere Einstellung Lueftung
#plot_time_dat(datei_name,4450)

datei_name = "../Test30.asc"
plot_time_dat(datei_name,0)


 

p.show()



