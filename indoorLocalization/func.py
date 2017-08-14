# -*- coding: utf-8 -*-
import xlrd
import pyrebase



''' JUST FOR TESTING '''

class findValueOfN:
    readBook = None
    database = None
    
    def getReadBook(self, readXlsPath):
        self.readBook = xlrd.open_workbook(readXlsPath)
        return self.getReadBook
    
    
    def connectToDatabase(self, databaseURL):
        config = {
          "apiKey": "apiKey",
          "authDomain": "projectId.firebaseapp.com",
          "databaseURL": databaseURL,
          "storageBucket": "projectId.appspot.com"
        }
        self.database = pyrebase.initialize_app(config).database









'''

wifidata = findValueOfN
wifidata.getReadBook(wifidata,"/home/yuda/workspace/python/indoorLocalization/xls/wifiInfo.xls")
wifidata.connectToDatabase(wifidata, "https://fingerprinteronfirebase.firebaseio.com/")



import pyrebase

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
dataA = {"x":3010,"y":9}
db_possition.push(dataA)

name = db_possition.child("position").get().val().keys()
name = list(name)[0]
name = dict(db_possition.child("position").child(name).get().val())

db_AP = dict(db.child("AP").get().val())
getAPInfo = list(db_AP.keys())




import xlrd
wifiDataBook = xlrd.open_workbook("/home/yuda/workspace/python/indoorLocalization/xls/wifiData.xls")
wifiDataSheet = wifiDataBook.sheets()[0]
print(wifiDataSheet.nrows, wifiDataSheet.ncols)
print(wifiDataSheet.row_values(8))













'''




'''
import pyrebase

config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://fingerprinteronfirebase.firebaseio.com/",
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
db.child("position").remove()
db_place = db.child("place").get()
db_possition = db.child("position")
dataA = {"x":3010,"y":9}
db_possition.push(dataA)

name = db_possition.child("position").get().key()
'''





'''
% 加權平均值
close all; clear all; clc;
x = [ % data放這裡

];
x = int8(x);

times = zeros(1,2);
for m = min(x):max(x)
    n = m-min(x)+1;
    times(n,1) = m;
    times(n,2) = length(find(x==m));
end
s = 0;
t = 0;
n = 4;
for m = 1:length(times)
    s = s +times(m,2)^n;
    t = t + times(m,1)*times(m,2)^n;
end
t = t/s
'''






'''
% 平方差公式
err = sum(abs(data(:,2)-(- (10.*n.*log10(data(:,4))-max))));
er = zeros(2,1);
count = 1;
cnt = zeros(2,3);
for m=3:0.001:4.5
    er(count) = sum(abs(data(:,1)-(- (10.*m.*log10(data(:,4))-max))));
    if(count&gt;1)
        if(er(count) &lt; er(count-1))
        
        %break;
        n2 = n1;
        end
    end
    cnt(count,1) = count;
    cnt(count,2) = m;
    cnt(count,3) = er(count);
    count = count +1;
    n1 = m;
end
'''




















