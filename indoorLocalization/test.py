#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:43:47 2017

@author: yuda
"""

from sklearn import neighbors
from offline import getClassifyList
import pyrebase
import pandas as pd
import os

config = {
      "apiKey": "apiKey",
      "authDomain": "projectId.firebaseapp.com",
      "databaseURL": "https://wifiinfobycoordinate.firebaseio.com/",
      "storageBucket": "projectId.appspot.com"
    }
    
firebase = pyrebase.initialize_app(config)
db = firebase.database()
db_AP = dict(db.child("AP").get().val())
all_AP_Name = list(db_AP.keys())

data = pd.read_excel(os.getcwd()+"/xls/wifiData5.xls",0)

# the sixth data for test
thisAPname = all_AP_Name[5]
classifyRecordingList = getClassifyList(4,data,all_AP_Name)[6][2]

# creeate a excel for training input, rssi (dbm)

for i in range(len(classifyRecordingList)):
    dx = classifyRecordingList[i][0][0] - db_AP[thisAPname]['x']
    dy = classifyRecordingList[i][0][1] - db_AP[thisAPname]['y']
    classifyRecordingList[i][0] = (dx**2+dy**2)**0.5
    del classifyRecordingList[i][2]

classifyRecordingList = pd.DataFrame(classifyRecordingList)

traningData = classifyRecordingList.drop(classifyRecordingList.index[40::],axis=0)
predictData = classifyRecordingList.drop(classifyRecordingList.index[0:40],axis=0)

tr_rssi = traningData.drop(traningData.columns[0],axis=1)
tr_leng = traningData.drop(traningData.columns[1],axis=1)
pr_rssi = (predictData.drop(predictData.columns[0],axis=1)).reset_index(drop=True)
pr_leng = (predictData.drop(predictData.columns[1],axis=1)).reset_index(drop=True)

knn = neighbors.KNeighborsRegressor(20, weights='distance').fit(tr_rssi,tr_leng)

result_check = pd.DataFrame(knn.predict(tr_rssi).tolist())
print("    tr_leng \tresult_check\n",pd.concat([tr_leng,result_check],axis=1),"\n\n")

result_predict = pd.DataFrame(knn.predict(pr_rssi).tolist())
print("    pr_leng \tresult_predict\n",pd.concat([pr_leng,result_predict],axis=1))


