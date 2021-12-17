# -*- coding:utf-8 -*-
"""
Created on 31.05.2011

@author: rened
"""
from  helper.AuswertH import *
#from  vorlage import *
from  scipy.integrate import simps

from rdp import rdp

def Reduce_data(data_X,data_Y,x1):
    Mx = N.column_stack((data_X[:,N.newaxis],data_Y[:,N.newaxis]))
    M2 = rdp(Mx,x1)

    data_X2 = M2[:,0].transpose()
    data_Y2 = M2[:,1].transpose()
    return data_X2,data_Y2

def integrate_Peak(x,y,startx,endx):
    start_idx = N.where(x > startx)[0][0]
    end_idx = N.where(x > endx)[0][0]
    piece_x = x[start_idx:end_idx]
    piece_y= y[start_idx:end_idx]
    return simps(piece_y,piece_x)

def CO_Value(Li_Wert):
    return ((0.00028*Li_Wert+4.5)*10.0)+0.85

    #return -0.00268*Li_Wert+43.809520+0.05 Old Values
def reduce_data(filename):
    mydescr = N.dtype([('Zeit', 'float'), ('Delta', 'float'),('T1', 'float'), ('T2', 'float'), ('T3', 'float'),('T4', 'float'),('T5', 'float'), ('T6', 'float'), ('T7', 'float'),('T8', 'float'),('CO', 'float')])
    myrecarray = read_array(filename, mydescr)

    ar_size=N.size(myrecarray, 0)

    del_value=False
    time_value = myrecarray[0][0]
    temp_value = myrecarray[0][4]

    d=0
    while N.size(myrecarray, 0)-2>d:
        d += 1
        del_value=True

        if abs(myrecarray[d][4]-temp_value)>3:
            temp_value = myrecarray[d][4]
            del_value=False

        if myrecarray[d][0]-time_value>60:
            time_value = myrecarray[d][0]
            del_value=False

        if del_value:
            myrecarray = N.delete(myrecarray, d, 0)
            d -= 1 

    T3 = myrecarray['T3']
    T3_k =  1000/(T3+273.15)
    """Ableitung direkt berechnen"""
    timeline_d = savitzky_golay(myrecarray['Zeit'], window_size=31, order=3,deriv=1)
    T3_d = savitzky_golay(myrecarray['T3'], window_size=31, order=3,deriv=1)  

    Ableit = T3_d/timeline_d
    p.plot(T3_k,N.log(Ableit),lw=2,label=filename)

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
    
    timeline_d = savitzky_golay(myrecarray['Zeit'], window_size=161, order=5,deriv=1)
    T3_d = savitzky_golay(myrecarray['T3'], window_size=161, order=5,deriv=1)
     
    Ableit = T3_d/timeline_d
    
    p.xlabel(r"1000/Temp [K]", fontsize = 12)
    p.ylabel(r"ln [K/s]", fontsize = 12)

    p.plot(1000./(T3+273.15),N.log(Ableit)*factor,lw=2,label=filename)

def plot_time_dat(filename):
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

    gh = ((T8-T1)/1.5)+T1 # Anpassung der Heizungstemperatur gegen Regeltemp

    p.xlabel(r"Time [s]", fontsize = 12)
    p.ylabel(r"Temp [Celsius]", fontsize = 12)

    from scipy.ndimage import gaussian_filter1d

    #logx, logy = N.log(timeline), N.log(gh)
    #model = N.polyfit(logx, logy, 2)
    #trend = N.polyval(model, logx)

    #smooth = gaussian_filter1d(logy - trend, 10)
    #smooth = N.exp(smooth + trend)

    #p.plot(timeline,smooth,lw=2)
    p.plot(timeline,T3,lw=2,label=filename+' Probe')
    p.plot(timeline,(T8+5+T6)/2,lw=4,label=filename+'_Ofen')
    p.plot(timeline,T1,lw=2,label=filename+' Heizung')

    #p.plot(timeline,N.log(T3-((T8+5+T6)/2)),lw=2,label=filename+' lnK')
    p.legend(loc='lower right')
    #p.plot(timeline,T7,lw=2,label=filename)


plot_time_dat('Test30c_k.asc')
plot_time_dat('Test60_k.asc')

p.show()



