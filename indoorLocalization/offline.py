# -*- coding: utf-8 -*-


import pyrebase
import pandas
import numpy
import os

# ==================================================================================

def calWeightAverage(dataList,weight):
    # dataList : [rssi1, rssi2, ..... ]
    # weight : The type is "int"
    sizeDataList = len(dataList)
    for i in range(sizeDataList):
        if numpy.isnan(dataList[sizeDataList-i-1]):
            del dataList[sizeDataList-i-1]
    if not dataList:
        return None
    else:
        dataMin = int(numpy.min(dataList))
        dataMax = int(numpy.max(dataList))
        appearanceTimes = []
        for i in range(dataMin,dataMax+1):
            appearanceTimes.append([i,dataList.count(i)])
        weight_sum = 0
        total_sum = 0
        for i in range(len(appearanceTimes)):
            weight_sum += appearanceTimes[i][1]**weight
            total_sum += appearanceTimes[i][0]*(appearanceTimes[i][1]**weight)
        return round(total_sum/weight_sum , 5)

def distance_to_rssi(n,distance,_1mRssiAvg):
    return numpy.round(-(10*n*numpy.log10(distance)-_1mRssiAvg), 5)

def rssi_to_distance(n,rssi,_1mRssiAvg):
    return numpy.round(10**((_1mRssiAvg-rssi)/(10*n)), 5)

def rssi_to_cell(n,rssi,_1mRssiAvg):
    return numpy.round(rssi_to_distance(n,rssi,_1mRssiAvg)/0.403, 5)

def calErrorSumOfSquares(AP_information, measure_posiANDavg, nValue):
    # AP_information : ['rssiAvg':__, 'x':__, 'y':__ ]
    # measure_posiANDavg : [[position],[weightAverage],[wifiData]]...]
    if not measure_posiANDavg:
        return None
    else:
        errSum = 0
        for i in range(len(measure_posiANDavg)):
            if not measure_posiANDavg[i][1]:
                break
            # unit of distance is 'm' ->  0.403m per cell
            distance = (((AP_information['x']-measure_posiANDavg[i][0][0])**2+
                        (AP_information['y']-measure_posiANDavg[i][0][1])**2
                        )**0.5)*0.403
            #rssi = -(10*nValue*numpy.log10(distance)-AP_information['rssiAvg'])
            rssi = distance_to_rssi(nValue,distance,AP_information['rssiAvg'])
            errSum += numpy.abs(measure_posiANDavg[i][1]-rssi)
        #print(AP_information,errSum)#,measure_posiANDavg)
        return errSum

def calValueOfN(AP_information, measure_posiANDavg):
    # AP_information : ['rssiAvg':__, 'x':__, 'y':__ ]
    # measure_posiANDavg : [[position],[weightAverage],[wifiData]]...]
    if not measure_posiANDavg:
        return None
    else:
        step = 0.01
        n_init = 0
        sqrErrRegister = 0
        while n_init<10:
            #print(n_init-step,sqrErrRegister)
            if n_init == 0:
                sqrErrRegister = calErrorSumOfSquares(AP_information, measure_posiANDavg,n_init)
                n_init += step
            elif sqrErrRegister > calErrorSumOfSquares(AP_information, measure_posiANDavg,n_init):
                sqrErrRegister = calErrorSumOfSquares(AP_information, measure_posiANDavg,n_init)
                n_init += step
            else:
                print(round(n_init-step,4) , round(sqrErrRegister,4), '\t_______')
                if n_init-step == 0:
                    return None
                else:
                    return round(n_init-step,4)
                    break
        

def getClassifyList(weight, recordingData, all_AP_name):
    # classify the different BSSID from data that type is DataFrame as a List
    # save model likes [ [BSSID], [N], [[[position0],[weightAverage0],[wifiData0]],
    #                                   [[position1],[weightAverage1],[wifiData1]],..] ]
    # ______________________________________________________________________________
    # weight : the type is "int"
    # totalData : this is a excel that saved every datas from mobile phone
    # AP_name : this is a list which is on firebase
    classify_WifiData = []
    for i in range(len(all_AP_name)):
        classify_WifiData.append([all_AP_name[i],[],[]])
        for j in range(len(recordingData)):
            if list(recordingData.iloc[j])[1] == all_AP_name[i]:
                classify_WifiData[i][2].append([list(recordingData.iloc[j])[2:4],
                             calWeightAverage(list(recordingData.iloc[j])[4:],weight),
                             list(recordingData.iloc[j])[4:]])
    return classify_WifiData


def save_n_to_classifyList(classifyList, APInfo_from_firebase):
    # before use this function, please make sure 'classifyList' have been created 
    #                                                               by "getClassifyList()"
    for i in range(len(classifyList)):
        classifyList[i][1] = calValueOfN(APInfo_from_firebase[classifyList[i][0]], 
                    classifyList[i][2])
    return classifyList


def add_n_to_dictionary(APInfo_from_firebase, classifyList):
    for i in range(len(classifyList)):
        APInfo_from_firebase[classifyList[i][0]]["n"] = classifyList[i][1]
    return APInfo_from_firebase


# ==================================================================================


if __name__ == '__main__':
    config = {
      "apiKey": "apiKey",
      "authDomain": "projectId.firebaseapp.com",
      "databaseURL": "https://wifiinfobycoordinate.firebaseio.com/",
      "storageBucket": "projectId.appspot.com"
    }
    
    firebase = pyrebase.initialize_app(config)
    
    db = firebase.database()
    db.child("position").remove()
    db_possition = db.child("position")
    pushDataTest = {"x":3010,"y":9}
    db_possition.push(pushDataTest)
    
    name = db_possition.child("position").get().val().keys()
    name = list(name)[0]
    name = dict(db_possition.child("position").child(name).get().val())
    
    db_AP = dict(db.child("AP").get().val())
    all_AP_Name = list(db_AP.keys())
    
    
    data = pandas.read_excel(os.getcwd()+"/xls/wifiData3.xls",0)
    #data = data.drop(0,axis = 0)  # del rows of index
    # test dictionary
    # db_AP["00:22:cf:cc:d1:36"]["n"] = 1111
      
    classifyRecordingList = getClassifyList(4,data,all_AP_Name)
    save_n_to_classifyList(classifyRecordingList, db_AP)
    add_n_to_dictionary(db_AP, classifyRecordingList)
    
    
    db.child('forN').remove()
    
    upNewAPInfo = db.child('forN')
    upNewAPInfo.push(db_AP)