# -*- coding: utf-8 -*-


import pyrebase



# ==================================================================================

def takeOffNo_N_term(forN):
    for i in range(len(forN)):
        if 'n' not in list(forN[list(forN.keys())[len(forN)-i-1]].keys()):
            del forN[list(forN.keys())[len(forN)-i-1]]
            i+=1
    return forN




# ==================================================================================
config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://wifiinfobycoordinate.firebaseio.com/",
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config).database()
forN = list(firebase.child("forN").get().val().keys())[0]
forN = dict(firebase.child("forN").child(forN).get().val())
forN = takeOffNo_N_term(forN)
realtime = list(firebase.child("realtime").get().val().keys())[0]
realtime = dict(firebase.child("realtime").child(realtime).get().val())


'''
import threading
import time

def main():
    while True:
        print(1)
        time.sleep(0.5)

def thr():
    T2 = threading.Thread(target=main)
    T2.start()
    
if __name__ == '__main__':
    main()
'''











