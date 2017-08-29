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

def localization_by_4(ApInfo, realtimeDatas):
    largest_three_rssi = list(dict(sorted(realtimeDatas.items(),
                               key=operator.itemgetter(1))[-3::]).keys())

    return 0

def localization(ApInfo, realtimeDatas):

    if triangle_acute_or_not(ApInfo, realtimeDatas):
        print('TTT')
    else:
        print('FFF get 4 points')
        localization_by_4(ApInfo, realtimeDatas)
    
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

    localization(ApInfo, realtimeDatas)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    