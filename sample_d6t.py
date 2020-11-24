# coding: utf-8
# Sample that outputs the value acquired by D6T.
# Please execute the following command before use "pigpio"
#  $ sudo pigpio

import grove_d6t
import pigpio
import time

d6t = grove_d6t.GroveD6t()

while 1:
        try:
                tpn, tptat = d6t.readData()
                if tpn == None:
                        continue
                print(round(((max(tpn)+3)* 9/5 + 32),1))
                print(max(tpn))
                print(tpn,"PTAT : %.1f" %tptat)
                time.sleep(1.0)
        except IOError:
                print("IOError")
read_temp()