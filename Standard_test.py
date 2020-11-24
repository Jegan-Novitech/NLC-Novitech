# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import grove_d6t
import pigpio
import time
from tkinter import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
BUZZER=21
G_LED=16
R_LED=20
GPIO.setup(BUZZER,GPIO.OUT)
GPIO.setup(G_LED,GPIO.OUT)
GPIO.setup(R_LED,GPIO.OUT)
GPIO.output(BUZZER,0)
GPIO.output(G_LED,0)
GPIO.output(R_LED,0)

from skimage import *
import time,subprocess,random
import threading
import tkinter.font as font
import udplib
import pymsgbox,random
import imageio,time
from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk
from pathlib import Path

from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2,message
import os,subprocess
from multiprocessing.pool import ThreadPool
import serial
#import recognize_faces_video as face
import json
from pyzbar import pyzbar
ROOT = Tk()
w=300
h=200
# ROOT.attributes('-fullscreen', True)
ws = ROOT.winfo_screenwidth()
hs = ROOT.winfo_screenheight()
print(ws,hs)
BIG_SIZE=int(hs/24)
MIDIUM_SIZE=int(hs/46)
SMALL_SIZE=int(hs/89)
x = (ws/2) - (w/2)    
y = (hs/2) - (h/2)

f=open("/home/pi/share/config",'r')
test_string = f.read()
f.close()
res = json.loads(test_string)

host_ip=res['host_ip']
port_no=res['port_no']
calib_value=res['calib_value']
temp_max=res['temp_thresh']
d6t = grove_d6t.GroveD6t()

def read_temp():
    tpn, tptat = d6t.readData()
    if tpn == None:
        return 0
    tpn1=tpn[8:12]+tpn[12:16]
    calib_temp=round((36.0+(36-38)*(max(tpn))/(33.1-36.1))/float(calib_value),1)
    #print(calib_temp)
    temp=float(round((calib_temp* 9/5 + 32),1))
    if(type(temp)!=type(99.0)):
        temp=0
    return temp

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
#cap = VideoStream(src=0).start()
cap = VideoStream(src=0,usePiCamera=1).start()
time.sleep(2)

class App(threading.Thread):
    def __init__(self, tk_root):
        self.tk = tk_root
        self.b_id=""
        threading.Thread.__init__(self)
#         self.vid = cv2.VideoCapture(video_name)
#         self.vs = VideoStream(src=0,usePiCamera=True,framerate=32).start()
#         self.vs = VideoStream(src=0,usePiCamera=False).start()
#         time.sleep(2.0)
#         self.frame = self.vs.read()
        
        self.start()
    def run(self):
        self.tk.configure(background='#333579')
        self.leftFrame = Frame(self.tk, background ='#f09f10')
        self.rightFrame = Frame(self.tk, background ='#333579')
        
        self.leftFrame.pack(side = LEFT,fill=BOTH, expand = YES,anchor=CENTER)
        self.rightFrame.pack(side = RIGHT, expand = YES,fill=BOTH)
        
        self.idFrame = Frame(self.rightFrame, background ='#333579')
        self.nameFrame = Frame(self.rightFrame, background ='#333579')
        self.popupFrame = Frame(self.rightFrame, background ='#333579')
        
        
        self.idFrame.pack(side = TOP,fill=BOTH, expand = YES)
        self.nameFrame.pack(side = TOP, expand = YES,fill=BOTH)
        self.popupFrame.pack(side = TOP,fill=BOTH, expand = YES)
        self.display_on()
        while 1:
            self.b_id=""
            self.frame = cap.read()
            image=cv2.resize(self.frame , (400,400))
            try:
                barcodes = pyzbar.decode(image)
            except:
                barcodes=[]
#             print (barcodes)
            temperature123=read_temp()
        #self.sl3.config(text="Show Your ID", fg='black', bg='#D5DBDB')
#         self.sl1.config(text="READY TO CHECK MASK.", fg='black', bg='#D5DBDB')
            while not temperature123:
                temperature123=read_temp()
            for barcode in barcodes:
                self.b_id=barcode.data.decode("utf-8")
                
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
#             print (self.b_id)
            if(len(barcodes)>0):
                self.idLabel.config(text=str(self.b_id))
                self.tempLabel.config(text=str(temperature123)+" degF")
                i=1
                try:
                    i=0
                    print("self.b_id",self.b_id)
                    self.test_data=udplib.Attend_send(self.b_id+"~"+str(temperature123),host_ip=host_ip,port_no=port_no,bufferSize = 1024)
                    print(self.test_data)
                    try:
                        self.test_datas=self.test_data.split('~')
                        self.nameLabel.config(text=str(self.test_datas[1]))
                        if(temperature123>float(temp_max)):
                            GPIO.output(BUZZER,1)
                            GPIO.output(G_LED,0)
                            GPIO.output(R_LED,1)
                            self.depositLabel.config(text="NOT ALLOWED", fg='#FFFFFF', bg='GREEN')
                        else:
                            GPIO.output(BUZZER,0)
                            GPIO.output(G_LED,1)
                            GPIO.output(R_LED,0)
                            self.depositLabel.config(text="ALLOWED", fg='#FFFFFF', bg='RED')
                    except:
                        self.nameLabel.config(text="Unknown")
                except:
                    self.nameLabel.config(text="Server Connection Failed")
                time.sleep(2)
                self.idLabel.after(3000, self.reset)
            cv2.imshow("Image", image)
            cv2.waitKey(1)
            
    def reset(self):
        GPIO.output(BUZZER,0)
        GPIO.output(G_LED,0)
        GPIO.output(R_LED,0)
        barcodes=[]
        self.idLabel.config(text=" ")
        self.nameLabel.config(text="    Waiting   ")
        self.tempLabel.config(text="          ")
        self.depositLabel.config(text=" ")
    def display_on(self):
        
        self.labelText = '   Scan Your Barcode     '
        self.depositLabel = Label(self.popupFrame, text = self.labelText, bg='#333579',fg="#FFFFFF",font=('Arial',18, 'bold'))
        self.depositLabel.pack(side=TOP,anchor=CENTER)
        
        self.labelText1 = ' Employee ID  '
        self.idLabel = Label(self.idFrame, text = self.labelText1, bg='#333579',fg="#FFFFFF",font=('Arial', 18, 'bold'))
        self.idLabel.pack(side=TOP,anchor=CENTER)
        
        self.labelText2 = ' Employee Name  '
        self.nameLabel = Label(self.nameFrame, text = self.labelText2, bg='#333579',fg="#FFFFFF",font=('Arial', 18, 'bold'))
        self.nameLabel.pack(side=TOP,anchor=CENTER)
        
        self.labelText3 = ' Temperature  '
        self.tempLabel = Label(self.leftFrame, text = self.labelText3, bg='#f09f10',fg="#000000",font=('Arial', 28, 'bold'))
        self.tempLabel.pack(side=LEFT,anchor=E)

ROOT.geometry('%dx%d+%d+%d' % (w, h, x, y))
ROOT.attributes("-fullscreen", True)
#ROOT.geometry('800X600')
ROOT.resizable(True, True) 
APP = App(ROOT)
ROOT.mainloop()    
