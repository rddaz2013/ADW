# -*- coding:utf-8 -*-
"""
Created on 31.05.2011

@author: rened
"""

from  helper.AuswertH import *
from  vorlage import *

def plot_time_dat2(filename):
    mydescr = N.dtype([('Zeit', 'float'), ('Delta', 'float'),('T1', 'float'), ('T2', 'float'), ('T3', 'float'),('T4', 'float'),('T5', 'float'), ('T6', 'float'), ('T7', 'float'),('T8', 'float'),('CO', 'float')])

    myrecarray = read_array(filename, mydescr)
    timeline  = myrecarray['Zeit']
    
    T1 = myrecarray['T1'] # Heizung
    T2 = myrecarray['T2'] # Probe Halbmitte
    T3 = myrecarray['T3'] # Probe Mitte
    T4 = myrecarray['T4'] # Abluft/Raumtemp
    T5 = myrecarray['T5'] # Heizung B
    T6 = myrecarray['T6'] #
    T7 = myrecarray['T7'] # Probe Ausen
    T8 = myrecarray['T8'] # Ofenmitte (dickes Thermoelement)
    CO = myrecarray['CO']
    
    p.xlabel(r"Time [s]", fontsize = 12)
    p.ylabel(r"CO [ppm]", fontsize = 12)

    p.plot(timeline,T1,lw=3)
    #p.plot(timeline,T2,lw=3)
    p.plot(timeline,T3,lw=2)
    #p.plot(timeline,T4,lw=2)
    #p.plot(timeline,T5,lw=1)
    #p.plot(timeline,T6,lw=1)
    #p.plot(timeline,T7,lw=1)
    p.plot(timeline,(T8+5+T6)/2.,lw=1) # (T8+5+T6)/2 Neue Leittemperatur!!
    LeitTemp = (T8+5+T6)/2
    dT1 = T1-LeitTemp
    dT2 = LeitTemp-T3
    p.plot(timeline, (dT1-dT2)/N.log(N.abs(dT1/dT2)))
    #p.plot(timeline,CO_Value(CO)*3,lw=1)


    #p.plot(timeline,T3)
    #schnitt = N.log(T3-T7)
    #p.plot(timeline[1000:],schnitt[1000:])

    #slope, intercept, r_value, p_value, std_err = stats.linregress(timeline[1000:],schnitt[1000:])

    #print N.log(-slope), slope, intercept, r_value, p_value, std_err

    #print integrate_Peak(timeline,CO_Value(CO),150,300)   # Hohe Luefterstufe + 800L/h zuluft
    #print integrate_Peak(timeline,CO_Value(CO),16650,16800) # halbe Luefterstufe + 800L/h zuluft
    #print integrate_Peak(timeline,CO_Value(CO),19400,19600) # halbe Luefterstufe + 400L/h zuluft
    #print integrate_Peak(timeline,CO_Value(CO),19700,19850) # niedrige Luefterstufe + 400L/h zuluft
    #print integrate_Peak(timeline,CO_Value(CO),20000,20300) # niedrige Luefterstufe + 400L/h zuluft + Dämpfer
    #print integrate_Peak(timeline,CO_Value(CO),21400,21700) # niedrige Luefterstufe + 400L/h zuluft + Dämpfer + Umbau Lüfterleitung
    #print integrate_Peak(timeline,CO_Value(CO),22000,22200) # niedrige Luefterstufe + Umbau Lüfterleitung


datei_name = "TL9582_3x.asc"
plot_time_dat2(datei_name)
p.show()



