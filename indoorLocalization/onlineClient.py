# -*- coding: utf-8 -*-

import pyrebase

if __name__ == '__main__':
    
    config = {
      "apiKey": "apiKey",
      "authDomain": "projectId.firebaseapp.com",
      "databaseURL": "https://wifiinfobycoordinate.firebaseio.com/",
      "storageBucket": "projectId.appspot.com"
    }
    firebase = pyrebase.initialize_app(config).database()
    firebase.child("realtime").remove()
    realtime = firebase.child("realtime")
    
    # position is -6 12
    realtimeWifiData = {
            'c8:3a:35:28:56:b0':	-62,
            '1c:b7:2c:ed:b5:f8':	-50,
            'c8:3a:35:11:55:a8':	-62,
            'c8:3a:35:14:ce:a0':	-73,
            '40:4a:03:8d:aa:9e':	-66,
            '9c:5c:8e:b0:b5:88':	-72,
            '6c:72:20:0d:88:28':	-76,
            '04:8d:38:a3:da:13':	-80,
            'b0:c7:45:ac:21:4a':	-69,
            '10:c3:7b:cc:51:50':	-79,
            '70:62:b8:83:94:63':	-82,
            'f8:e9:03:8f:bc:62':	-84,
            '00:13:49:af:ad:2b':	-85,
            'e8:94:f6:97:90:e0':	-85,
            '54:d0:ed:a1:21:e8':	-86,
            'e4:6f:13:62:c7:ea':	-87,
            'c8:3a:35:53:bc:31':	-89,
            '10:be:f5:ab:e0:21':	-81

                        }
    realtime.push(realtimeWifiData)