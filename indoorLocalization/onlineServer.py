# -*- coding: utf-8 -*-


import pyrebase
import operator
import numpy
from offline import rssi_to_cell



# ==================================================================================

def del_no_N_term(forN):
    length = len(forN)
    for i in range(length):
        if 'n' not in list(forN[list(forN.keys())[length-i-1]].keys()):
            del forN[list(forN.keys())[length-i-1]]
            i-=1
    return forN

def del_not_in_forN(realtime,forN):
    length = len(realtime)
    for i in range(length):
        if list(realtime.keys())[length-i-1] not in list(forN.keys()):
            del realtime[list(realtime.keys())[length-i-1]]
            i-=1
    return realtime

def choose_biggest_three_rssi_to_cell(realtime,forN):
    realtime = sorted(realtime.items(), key=operator.itemgetter(1))
    lenth = len(realtime)
    for i in range(lenth-3):
        del realtime[0]
    realtime =dict(realtime)
    for i in range(len(realtime)):
        realtime[list(realtime.keys())[i]] = numpy.round(rssi_to_cell(forN[list(realtime.keys())[i]]['n'],
                      realtime[list(realtime.keys())[i]], forN[list(realtime.keys())[i]]['rssiAvg']),5)
    return realtime


def getRealtimePosision(realtime_length_byCell,forN): # return [x, y]
    if len(realtime_length_byCell) < 3:
        return None
    ls4_save_coordinate = [[],[]]
    for i in range(len(realtime_length_byCell)): # take i-th and i+1-th to calculation one-set coordinates
        n = i
        n1 = i+1
        if n1 >= len(realtime_length_byCell):
            n1 = n1 - len(realtime_length_byCell)
        dx = forN[list(realtime_length_byCell.keys())[n1]]['x']-forN[list(realtime_length_byCell.keys())[n]]['x']
        dy = forN[list(realtime_length_byCell.keys())[n1]]['y']-forN[list(realtime_length_byCell.keys())[n]]['y']
        d  = (dx**2+dy**2)**0.5
        r  = realtime_length_byCell[list(realtime_length_byCell.keys())[n]]
        r1 = realtime_length_byCell[list(realtime_length_byCell.keys())[n1]]
        a  = (r**2-r1**2+d**2)/(2*d)
        h  = (numpy.abs(r**2-a**2))**0.5
        xl = forN[list(realtime_length_byCell.keys())[n]]['x']+a/d*dx
        yl = forN[list(realtime_length_byCell.keys())[n]]['y']+a/d*dy
        ls4_save_coordinate[0].append([xl+h/d*dy, yl-h/d*dx])
        ls4_save_coordinate[1].append([xl-h/d*dy, yl+h/d*dx])
    for i in range(len(ls4_save_coordinate[0])):
        n = i
        n1 = i+1
        if n1 >= len(ls4_save_coordinate[0]):
            n1 = n1 - len(ls4_save_coordinate[0])
        
    return ls4_save_coordinate
        
def getTriLength(points_3):
    sum = 0
    for i in range(len(points_3)) :
        n1 = i+1;
        if i == len(points_3)-1:
            n1 = 0;
        sum += ((points_3[i][0]-points_3[n1][0])**2+
                (points_3[i][1]-points_3[n1][1])**2)**0.5
    return round(sum,5)


def getSmallerRealtimePosision(two_set_coordinates):
    if getTriLength(two_set_coordinates[0]) > getTriLength(two_set_coordinates[1]):
        return two_set_coordinates[1]
    else:
        return two_set_coordinates[0]


def getAvgPossition(one_set_coordinate):
    x = 0
    y = 0
    for i in range(len(one_set_coordinate)):
        x += one_set_coordinate[i][0]
        y += one_set_coordinate[i][1]
    return [round(x/len(one_set_coordinate),5),round(y/len(one_set_coordinate),5)]

def getWeightAvgPossition(avgPossition_coordinate, weight, biggest_three_rssi_Info, forN):
    x = avgPossition_coordinate[0]
    y = avgPossition_coordinate[1]
    numerator_x = 0
    numerator_y = 0
    denominator = 0
    for i in range(len(biggest_three_rssi_Info)):
        xi = forN[list(biggest_three_rssi_Info.keys())[i]]['x']
        yi = forN[list(biggest_three_rssi_Info.keys())[i]]['y']
        _d = ((x-xi)**2+(y-yi)**2)**-0.5
        denominator += _d**weight
        numerator_x += xi*_d**weight
        numerator_y += yi*_d**weight
    print('加權平均後的座標為\n',numerator_x/denominator,numerator_y/denominator)
    return numerator_x
# ==================================================================================

if __name__ == '__main__':
    
    config = {
      "apiKey": "apiKey",
      "authDomain": "projectId.firebaseapp.com",
      "databaseURL": "https://wifiinfobycoordinate.firebaseio.com/",
      "storageBucket": "projectId.appspot.com"
    }
    firebase = pyrebase.initialize_app(config).database()
    forN = list(firebase.child("forN").get().val().keys())[0]
    forN = dict(firebase.child("forN").child(forN).get().val())
    forN = del_no_N_term(forN)
    realtime = list(firebase.child("realtime").get().val().keys())[0]
    realtime = dict(firebase.child("realtime").child(realtime).get().val())
    realtime = del_not_in_forN(realtime,forN)
    realtime = choose_biggest_three_rssi_to_cell(realtime,forN)
       
    
    a = getRealtimePosision(realtime, forN)
    a = getSmallerRealtimePosision(a)
    a = getAvgPossition(a)
    print('平均座標為\n',a[0],a[1])
    getWeightAvgPossition(a,2,realtime,forN)







