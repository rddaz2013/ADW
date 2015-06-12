# -*- coding:utf-8 -*-
"""
Created on 31.05.2011

@author: rened
"""
from  scipy.integrate import simps
from  helper.AuswertH import *

filename = "../Test60.asc"
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
p.ylabel(r"Temp [C]", fontsize = 12)

Diff_T1T3 = savitzky_golay((T1-T3), window_size=61, order=5,deriv=0)
dT_T3 = savitzky_golay((T3), window_size=161, order=5,deriv=1)

#p.plot(timeline,Diff_T1T3,lw=2)
p.plot(timeline,dT_T3/(Diff_T1T3),lw=2)
#p.plot(dT_T3,(Diff_T1T3),lw=2)
p.show()



