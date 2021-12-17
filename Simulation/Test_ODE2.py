'''
Created on 26.08.2011

@author: rene
'''

from scipy import *
from matplotlib.pylab import *
import scipy.integrate as itg
import numpy as np


Stoffdaten = {'beta':0.0001*60.,
              'LnA':2.52,
              'Ea':6353.,
              'Model':'Ozawa',
              'O_factor':1.,
              'Reac_Heat':350.,
              'cp':1.8}

Simdaten   = {'Probe_T0':20.,
              'Ausen_T0':21.,
              'Heat_Flow_0':0.,
              'Umsatz_0':0.,
              'End_Time':2000,
              'Step_Time':10,
              'Ofen_mx':0.2}

def Kin_Umsatz(temp):
    '''
    Berechnet die Fortschritt des Reaktionsumsatzes dU/dt bei einer Temperatur
     Auswertung von LnA und Ea geschieht durch ASTM E698-05 mit Anpassung von LnA
     LnA (ODE) = LnA(ASTM_Ozawa) * T**2
     LnA (ODE) = LnA(ASTM_Kissinger)

     Einheit der Ausgabe ist k = [1/min]

    :param temp:
    '''
    return (
        np.exp(Stoffdaten['LnA'])
        * (temp + 273) ** Stoffdaten['O_factor']
        * np.exp(-Stoffdaten['Ea'] / (temp + 273.15))
        if Stoffdaten['Model'] == 'Ozawa'
        else np.exp(Stoffdaten['LnA'])
        * np.exp(-Stoffdaten['Ea'] / (temp + 273.15))
    )

def f(y,t):
    Probe_T = y[0]
    Ausen_T = y[1]
    beta = y[2]
    f3 = Kin_Umsatz(Probe_T)*(1-y[3])
    '''
     Einheit der Ausgabe ist f0 = k in [K/min] * Reaktionswaerme/cp fuer Umsatz !
     '''
    f0 = (beta * (Ausen_T-Probe_T)) + (f3 * Stoffdaten['Reac_Heat']/Stoffdaten['cp'])
    f1 = Simdaten['Ofen_mx'] if t>233 else 0.
    f2 = 0
    return [f0,f1,f2,f3]

def Sim_Block(filename,Save_File):
    t=arange(0.0,Simdaten['End_Time'],Simdaten['Step_Time'])
    y0 = [Simdaten['Probe_T0'],Simdaten['Ausen_T0'],Stoffdaten['beta'],Simdaten['Umsatz_0']]
    ww = itg.odeint(f,y0,t,hmin=0.0001,atol=.0001)
    ww2 = np.column_stack((ww,t))

    if Save_File:
        savetxt(filename, ww2,delimiter=',' )

    return ww2

ww = Sim_Block('XXX',False)

#ww.tofile('foo.csv',sep=',',format='%10.5f')
#savetxt('foo.csv', ww,delimiter=',' )

T_Probe = ww[:,0]
T_Ofen =ww[:,1]
Umsatz =ww[:,3]
t = ww[:,4]
#ddy = 1.0-sin(ww[:,0])

plot(t,T_Probe,label='dy')
plot(t,T_Ofen,label='dy')

Stoffdaten = {'beta':0.0001*60.,
              'LnA':9.68922,
              'Ea':6826.64,
              'Model':'XXX',
              'O_factor':1.6,
              'Reac_Heat':350.,
              'cp':1.8}

ww = Sim_Block('XXX',False)

#ww.tofile('foo.csv',sep=',',format='%10.5f')
#savetxt('foo.csv', ww,delimiter=',' )

T_Probe = ww[:,0]
T_Ofen =ww[:,1]
Umsatz =ww[:,3]
t = ww[:,4]
#ddy = 1.0-sin(ww[:,0])

plot(t,T_Probe,label='dy')
plot(t,T_Ofen,label='dy')

#Simdaten['Ofen_mx']=0.6
#ww = Sim_Block('XXX',False)
show()