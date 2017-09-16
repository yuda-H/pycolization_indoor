#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 14:23:40 2017
@author: yuda
"""

import pyrebase
import operator
import numpy
import matplotlib.pyplot as plt
from offline import rssi_to_cell

# ==================================================================================
def filter_no_N_term(AP_info):
    length = len(AP_info)
    for i in range(length):
        if 'n' not in list(AP_info[list(AP_info.keys())[length-i-1]].keys()):
            del AP_info[list(AP_info.keys())[length-i-1]]
            i-=1
    return AP_info


def filter_not_in_ApInfo(AP_info,realtime):
    length = len(realtime)
    for i in range(length):
        if list(realtime.keys())[length-i-1] not in list(AP_info.keys()):
            del realtime[list(realtime.keys())[length-i-1]]
            i-=1
    return realtime

def triangle_acute_or_not(ApInfo, realtimeDatas):
    largest_three_rssi = list(dict(sorted(realtimeDatas.items(),
                               key=operator.itemgetter(1))[-3::]).keys())
    x = []
    y = []
    l = []
    for i in range(3):
        x.append(ApInfo[largest_three_rssi[i]]['x'])
        y.append(ApInfo[largest_three_rssi[i]]['y'])
    for i in range(3):
        l.append(((x[i-1]-x[i-2])**2+(y[i-1]-y[i-2])**2)**0.5)
    for i in range(3):
        angle_i = (l[i-1]**2+l[i-2]**2-l[i]**2) / (2*l[i-1]*l[i-2])
        if angle_i>-1 and angle_i<0:
            return False
    return True

def getWeightAvgPossition(coordinate_3,weight):
    # [[x0,x1,x2], [y0,y1,y2]]
    avg = [numpy.sum(coordinate_3[0][::])/3,numpy.sum(coordinate_3[1][::])/3]
    numerator_x = 0
    numerator_y = 0
    denominator = 0
    
    for i in range(3):
        dx = coordinate_3[0][i]-avg[0]
        dy = coordinate_3[1][i]-avg[1]
        length = (dx**2+dy**2)**-0.5
        denominator += length**weight
        numerator_x += coordinate_3[0][i]*length**weight
        numerator_y += coordinate_3[1][i]*length**weight
    avg = [numerator_x/denominator,numerator_y/denominator]
    print(avg)
    return 0

def localization_by_4(ApInfo, realtimeDatas, weight):
    if len(realtimeDatas)<4:
        print('Less then 4 points.')
        return False
    largest_3_rssi = list(dict(sorted(realtimeDatas.items(),
                               key=operator.itemgetter(1))[-3::]).keys())
    smallest_1_rssi = list(dict(sorted(realtimeDatas.items(),
                               key=operator.itemgetter(1))[0:1]).keys())
    for i in range(3):
        ApInfo[largest_3_rssi[i]]['realtime']=realtimeDatas[largest_3_rssi[i]]
    ApInfo[smallest_1_rssi[0]]['realtime']=realtimeDatas[smallest_1_rssi[0]]
    
    coordinate_6 = [[],[],[]]
    for i in range(3):
        dx = ApInfo[largest_3_rssi[i]]['x']-ApInfo[largest_3_rssi[i-1]]['x']
        dy = ApInfo[largest_3_rssi[i]]['y']-ApInfo[largest_3_rssi[i-1]]['y']
        d  = (dx**2+dy**2)**0.5
        r1  = rssi_to_cell(ApInfo[largest_3_rssi[i]]['n'], 
                           ApInfo[largest_3_rssi[i]]['realtime'],
                           ApInfo[largest_3_rssi[i]]['rssiAvg'])
        r  = rssi_to_cell(ApInfo[largest_3_rssi[i-1]]['n'], 
                           ApInfo[largest_3_rssi[i-1]]['realtime'],
                           ApInfo[largest_3_rssi[i-1]]['rssiAvg'])
        a  = (r**2-r1**2+d**2)/(2*d)
        h  = (numpy.abs(r**2-a**2))**0.5
        xl = ApInfo[largest_3_rssi[i-1]]['x']+a/d*dx
        yl = ApInfo[largest_3_rssi[i-1]]['y']+a/d*dy
        x0 = xl+h/d*dy
        y0 = yl-h/d*dx
        x1 = xl-h/d*dy
        y1 = yl+h/d*dx
        coordinate_6[0].append(x0)
        coordinate_6[0].append(x1)
        coordinate_6[1].append(y0)
        coordinate_6[1].append(y1)
    
    for i in range(6):
        length_x = coordinate_6[0][i]-ApInfo[smallest_1_rssi[0]]['x']
        length_y = coordinate_6[1][i]-ApInfo[smallest_1_rssi[0]]['y']
        length = numpy.abs((length_x**2+length_y**2)**0.5-
                           rssi_to_cell(ApInfo[smallest_1_rssi[0]]['n'],
                                     ApInfo[smallest_1_rssi[0]]['realtime'],
                                     ApInfo[smallest_1_rssi[0]]['rssiAvg']))
        coordinate_6[2].append(length)
        
    
    for i in range(5):
        for j in range(5-i):
            if coordinate_6[2][j] > coordinate_6[2][j+1]:
                for k in range(3):
                    temp = coordinate_6[k][j]
                    coordinate_6[k][j] = coordinate_6[k][j+1]
                    coordinate_6[k][j+1] = temp       
    #print(coordinate_6)
    
    fig, ax = plt.subplots()
    plt.xlim(-50,100)
    plt.ylim(-50,100)
    for i in range(3):
        r = rssi_to_cell(ApInfo[largest_3_rssi[i]]['n'],
                         ApInfo[largest_3_rssi[i]]['realtime'],
                         ApInfo[largest_3_rssi[i]]['rssiAvg'])
        circle = plt.Circle((ApInfo[largest_3_rssi[i]]['x'], 
                             ApInfo[largest_3_rssi[i]]['y']),r,fill=False)
        ax.add_artist(circle)
    for i in range(6):
        if i < 3 : clr = 'r'
        else : clr = 'k'
        point = plt.Circle((coordinate_6[0][i],coordinate_6[1][i]),1,
                           color=clr,fill=False)
        ax.add_artist(point)
    
    r = rssi_to_cell(ApInfo[smallest_1_rssi[0]]['n'],
                     ApInfo[smallest_1_rssi[0]]['realtime'],
                     ApInfo[smallest_1_rssi[0]]['rssiAvg'])
    circle = plt.Circle((ApInfo[smallest_1_rssi[0]]['x'], 
                         ApInfo[smallest_1_rssi[0]]['y']),r,
                        color='b',fill=False)
    ax.add_artist(circle)
    
    coordinate_3 = [coordinate_6[0][0:3],coordinate_6[1][0:3]]
    getWeightAvgPossition(coordinate_3,weight)
    avg_position = [numpy.sum(coordinate_6[0][0:3])/3,numpy.sum(coordinate_6[1][0:3])/3]
    print('平均座標為',avg_position)
    
    return 0

def localization(ApInfo, realtimeDatas, weight):

    if triangle_acute_or_not(ApInfo, realtimeDatas):
        print('TTT')
    else:
        print('FFF get 4 points')
        localization_by_4(ApInfo, realtimeDatas, weight)
    
    return 0

# ==================================================================================

if __name__ == '__main__':
    
    config = {
      "apiKey": "apiKey",
      "authDomain": "projectId.firebaseapp.com",
      "databaseURL": "https://wifiinfobycoordinate.firebaseio.com/",
      "storageBucket": "projectId.appspot.com"
    }
    
    # connect to firebase and get AP_Info, realtimedatas
    firebase = pyrebase.initialize_app(config).database()
    ApInfo = list(firebase.child("AP_Info").get().val().keys())[0]
    ApInfo = dict(firebase.child("AP_Info").child(ApInfo).get().val())
    ApInfo = filter_no_N_term(ApInfo)
    realtimeDatas = list(firebase.child("realtime").get().val().keys())[0]
    realtimeDatas = dict(firebase.child("realtime").child(realtimeDatas).get().val())
    realtimeDatas = filter_not_in_ApInfo(ApInfo, realtimeDatas)
    
    largest_three_rssi = list(dict(sorted(realtimeDatas.items(),
                               key=operator.itemgetter(1))[-3::]).keys())

    localization(ApInfo, realtimeDatas,2)
    
    
    
    
    
    
    