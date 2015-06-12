# -*- coding:utf-8 -*-
'''
Created on 14.02.2012

@author: admin
'''
import socket
import numpy as N
from matplotlib.mlab import normpdf
from numpy.core.umath import absolute
import pylab as p
from scipy import *
import sys
import types
from scipy.integrate import simps
import xlwt
from vorlage import CO_Value, datei_name


def writeCSV(f, list):
    """
    Write list items to file 'f' in
    comma-separated-value format.  Strings will be written as-is, and
    other types of objects will be converted to strings and then
    written. Each call to writeCSV writes one line of the file.
    """
    for item in list:
        if type(item) == types.StringType:
            f.write(item+', ')
        else:
            f.write(`item`+', ')
            
    f.write('\n')
    
def savitzky_golay(y, window_size, order, deriv=0):
    """Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techhniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    try:
        window_size = N.abs(N.int(window_size))
        order = N.abs(N.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = N.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = N.linalg.pinv(b).A[deriv]
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - N.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + N.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = N.concatenate((firstvals, y, lastvals))
    return N.convolve( m, y, mode='valid')

def read_array2(data_str, dtype, separator=';', linekick='"'):

    """ Read a file with an arbitrary number of columns.
        The type of data in each column is arbitrary
        It will be cast to the given dtype at runtime

        RD
        Modifiziert um String zu lesen
    """
    cast = N.cast
    data = [[] for dummy in xrange(len(dtype))]
    fields = data_str.strip().split(separator)
    for i, number in enumerate(fields):
        data[i].append(number)
    for i in xrange(len(dtype)):
        data[i] = cast[dtype[i]](data[i])
    return N.rec.array(data, dtype=dtype)

def read_array(filename, dtype, separator=';', linekick='"'):
    
    """ Read a file with an arbitrary number of columns.
        The type of data in each column is arbitrary
        It will be cast to the given dtype at runtime
        
        RD
        Modifiziert um SIPCON Daten zu lesen
        L�sst Kommentarzeilen raus und konvertiert Komma zu Punkt
    """
    cast = N.cast
    data = [[] for dummy in xrange(len(dtype))]
    for line in open(filename, 'r'):
        if line[0]<>linekick: 
            fields = line.strip().split(separator)
            for i, number in enumerate(fields):
                #number=number.replace(',', '.')
                data[i].append(number)
    for i in xrange(len(dtype)):
        data[i] = cast[dtype[i]](data[i])
    return N.rec.array(data, dtype=dtype)

def read_array_str(data_str, dtype, separator=';', linekick='"'):
  
    """ Read a file with an arbitrary number of columns.
        The type of data in each column is arbitrary
        It will be cast to the given dtype at runtime
        
        RD
        Modifiziert um String zu lesen
    """
    cast = N.cast
    data = [[] for dummy in xrange(len(dtype))]
    fields = data_str.strip().split(separator)
    for i, number in enumerate(fields):
        data[i].append(number)
    for i in xrange(len(dtype)):
        data[i] = cast[dtype[i]](data[i])
    return N.rec.array(data, dtype=dtype)


def reduce_data(filename):
    mydescr = N.dtype([('Zeit', 'float'), ('Delta', 'float'),('T1', 'float'), ('T2', 'float'), ('T3', 'float'),('T4', 'float'),('T5', 'float'), ('T6', 'float'), ('T7', 'float'),('T8', 'float'),('CO', 'float')])
    myrecarray = read_array(filename, mydescr)

    ar_size=N.size(myrecarray, 0)

    del_value=False
    time_value = myrecarray[0][0]
    temp_value = myrecarray[0][4]

    d=0
    while N.size(myrecarray, 0)-2>d:
        d = d + 1
        del_value=True

        if abs(myrecarray[d][4]-temp_value)>3:
            temp_value = myrecarray[d][4]
            del_value=False

        if myrecarray[d][0]-time_value>60:
            time_value = myrecarray[d][0]
            del_value=False

        if del_value:
            myrecarray = N.delete(myrecarray, d, 0)
            d = d - 1

    T3 = myrecarray['T3']
    T3_k =  1000/(T3+273.15)
    """Ableitung direkt berechnen"""
    timeline_d = savitzky_golay(myrecarray['Zeit'], window_size=31, order=3,deriv=1)
    T3_d = savitzky_golay(myrecarray['T3'], window_size=31, order=3,deriv=1)

    Ableit = T3_d/timeline_d
    p.plot(T3_k,N.log(Ableit),lw=2,label=filename)


def integrate_Peak(x,y,startx,endx):
    start_idx = N.where(x > startx)[0][0]
    end_idx = N.where(x > endx)[0][0]
    piece_x = x[start_idx:end_idx]
    piece_y= y[start_idx:end_idx]
    piece_area = simps(piece_y,piece_x)
    return piece_area


def export2xls(filename):
    mydescr = N.dtype([('Zeit', 'float'), ('Delta', 'float'),('T1', 'float'), ('T2', 'float'), ('T3', 'float'),('T4', 'float'),('T5', 'float'), ('T6', 'float'), ('T7', 'float'),('T8', 'float'),('CO', 'float')])
    myrecarray = read_array(filename, mydescr)

    ar_size=N.size(myrecarray, 0)

    del_value=False
    time_value = myrecarray[0][0]
    temp_value = myrecarray[0][4]

    d=0
    while N.size(myrecarray, 0)-2>d:
        d = d + 1
        del_value=True

        if abs(myrecarray[d][4]-temp_value)>1:
            temp_value = myrecarray[d][4]
            del_value=False

        if myrecarray[d][0]-time_value>120:
            time_value = myrecarray[d][0]
            del_value=False

        if del_value:
            myrecarray = N.delete(myrecarray, d, 0)
            d = d - 1

    T3 = myrecarray['T3']
    T1 = myrecarray['T1']
    CO = myrecarray['CO']
    T3_k =  1000/(T3+273.15)
    timeline= myrecarray['Zeit']

    """Ableitung direkt berechnen
    Durch die Datenreduzierung koennen die Zeitabstaende sehr
    """
    timeline_d = savitzky_golay(myrecarray['Zeit'], window_size=31, order=3,deriv=1)
    T3_d = savitzky_golay(myrecarray['T3'], window_size=31, order=3,deriv=1)
    CO_d = savitzky_golay(myrecarray['CO'], window_size=31, order=3,deriv=1)
    delta_rem = T1-T3


    Ableit = T3_d/timeline_d
    delta = myrecarray['Delta']
    #p.plot(timeline,T3,lw=1,label=filename)
    kine=N.log(Ableit/myrecarray['Delta'][0])
    kine_ok = N.isnan(kine)
    print 'reduzierte Daten',N.size(timeline)
    ezxf = xlwt.easyxf
    heading_xf = ezxf('font: bold on; align: wrap on, vert centre, horiz center')
    kind_to_xf_map = {
        'date': ezxf(num_format_str='yyyy-mm-dd'),
        'int': ezxf(num_format_str='#,##0'),
        'money': ezxf('font: italic on; pattern: pattern solid, fore-colour grey25',
            num_format_str='$#,##0.00'),
        'float': ezxf(num_format_str='#0.0'),
        'float2': ezxf(num_format_str='#0.000'),
        'floatE': ezxf(num_format_str='0.00E+00'),
        'text': ezxf(),
        }



    book = xlwt.Workbook()
    sheet = book.add_sheet('Zeit_Daten')
    rowx = 0

    hdngs = ['Zeit', 'Ofen', 'Proben_Temp','Delta','[1000/K]','Ln(dT/dt)','CO [ppm]']
    kinds =  'float    float   float float floatE float2 float'.split()
    data_xfs = [kind_to_xf_map[k] for k in kinds]

    for colx, value in enumerate(hdngs):
        sheet.write(rowx, colx, value, heading_xf)
    sheet.set_panes_frozen(True) # frozen headings instead of split panes
    sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
    sheet.set_remove_splits(True) # if user does unfreeze, don't leave a split there

    #hdngs = ['Zeit', 'Proben_H_Temp', 'Proben_Temp']
    #kinds =  'float    float   float'.split()

    dummy = 0
    for data in enumerate(T3):
        rowx += 1
        sheet.write(rowx, 0, timeline[dummy], data_xfs[0])
        sheet.write(rowx, 1, T1[dummy], data_xfs[1])
        sheet.write(rowx, 2, T3[dummy], data_xfs[2])
        sheet.write(rowx, 3, delta[dummy], data_xfs[3])
        sheet.write(rowx, 4, T3_k[dummy], data_xfs[4])
        if not kine_ok[dummy]:
            sheet.write(rowx, 5, kine[dummy], data_xfs[5])
        sheet.write(rowx, 6, CO_Value(CO[dummy]), data_xfs[6])
        dummy = dummy +1
    xls_name = datei_name.split('.')[0]+'.xls'
    book.save(xls_name)

    print N.min(kine)


def GetData(get_host,get_Port,send_data):
    # Sendet den Komandostring zum Modul
    # Wertet die Rueckantwort nicht aus!!
    data =''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((get_host, get_Port))
    s.send(send_data)
    data = s.recv(1024)
    s.close()
    return data[1:]