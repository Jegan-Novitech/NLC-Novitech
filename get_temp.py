# coding: utf-8
# Sample that outputs the value acquired by D6T.
# Please execute the following command before use "pigpio"
#  $ sudo pigpio

import grove_d6t
##import pigpio
import time

d6t = grove_d6t.GroveD6t()

def read_temp():
    try:
        print('hi')
        tpn, tptat = d6t.readData()
        tpn=tpn[:8]
        print(max(tpn[:8]))
        print(tpn,"PTAT : %.1f" %tptat)
        if tpn == None:
            read_temp()
        else:
            return(float(max(tpn)))
        
        return 0
                #time.sleep(1.0)
    except:
        return 0
while 1:
    temp=read_temp()
    print(temp,type(temp))
    time.sleep(1.0)
# def read_temp():
#     return 97.5
