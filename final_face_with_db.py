from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
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
from gtts import gTTS 
# This module is imported so that we can  
# play the converted audio 
import os 
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
import recognize_faces_video as face
import json
import sqlite3,time
import socket
conn = sqlite3.connect('attendance.db')
c = conn.cursor()
reader_name= str(socket.gethostname())
# print("'"+reader_name+"'")
# reader_name=reader_name

try:
    c.execute('''CREATE TABLE temp_attendance
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,Detail text, temperature text, Mask text)''')
except:
    pass
conn.commit()
conn.close()

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

mask_value='0'
# construct the argument parser and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
    default="face_detector",
    help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
    default="mask_detector.model",
    help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
# subprocess.Popen("python3 audio.py --model 'Device Initiating Please wait'",shell=True)
subprocess.Popen("echo 'Device Initiating Please wait' | festival --tts",shell=True)
# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
    "res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
f=open("/home/pi/share/config",'r')
test_string = f.read()
f.close()
res = json.loads(test_string)
# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])
host_ip=res['host_ip']
port_no=res['port_no']
calib_value=res['calib_value']
temp=res['temp_thresh']
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")

d6t = grove_d6t.GroveD6t()
def audio_out(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("welcome.mp3") 
      
    # Playing the converted file 
    os.system("mpg321 welcome.mp3") 
def face_train(Name='nothing'):
        #global data
        try:
                data=face.start(Name)
        except:
                data=''
        return data

def read_temp():
#     return 97.6
    tpn, tptat = d6t.readData()
    if tpn == None:
        return 0
    tpn1=tpn[0:4]+tpn[4:8]
    calib_temp=round((36.0+(36-38)*(max(tpn1))/(33.1-36.1))/calib_value,1)
#     calib_temp=round((36.0+(36.3-33.5)*(max(tpn1)-43.3)/(51-43.3))/1.04,1)
#     calib_temp=round((36.0+(36.3-33.5)*(max(tpn1)-41.3)/(50-41.3))/calib_value,1)
    #print(calib_temp)
    temp=float(round((calib_temp* 9/5 + 32),1))
    if(type(temp)!=type(99.0)):
        temp=0
    return temp
img2 = cv2.imread('/home/pi/Desktop/face_new/113.jpg' )
ret,img2 = cv2.threshold(img2,127,255,cv2.THRESH_BINARY_INV)
print(img2)
img2=cv2.resize(img2, (int(ws), int(hs/1.5)))
img1 = cv2.imread('/home/pi/Desktop/face_new/114.jpg' )
img1=cv2.resize(img1, (int(ws), int(hs/1.5)))
#img_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)


#cap = VideoStream(src=0).start()
# cap = VideoStream(src=0,usePiCamera=1).start()
# time.sleep(2)
data=face_train()
import time,subprocess,random
check=0
cnt=1
count=0
flag=0
class App(threading.Thread):
    def __init__(self, tk_root):
        self.tk = tk_root
        threading.Thread.__init__(self)
#         self.vid = cv2.VideoCapture(video_name)
        self.vs = VideoStream(src=0,usePiCamera=True,framerate=32).start()
#         self.vs = VideoStream(src=0,usePiCamera=False).start()
        time.sleep(2.0)
        self.frame = self.vs.read()
        
        self.start()
    def run(self):
        self.tk.configure(background='#333579')
        self.topFrame = Frame(self.tk, background ='#333579')
        self.bottomFrame = Frame(self.tk, background ='#333579')
        self.middleFrame = Frame(self.tk, background ='#f09f10')
        self.topFrame.pack(side = TOP,fill=BOTH, expand = NO)
        self.middleFrame.pack(side = TOP, expand = NO,fill=BOTH)
        self.bottomFrame.pack(side = TOP, expand = YES,fill=BOTH)
#         self.logo1frame = Frame(self.bottomFrame, background ='#ffffff')
#         self.logo1frame.pack(side = LEFT, expand = YES,fill=BOTH)
#         self.logo2frame = Frame(self.bottomFrame, background ='#ffffff')
#         self.logo2frame.pack(side = RIGHT, expand = YES,fill=BOTH)
        self.detail1frame = Frame(self.bottomFrame, background ='#333579')
        self.detail1frame.pack(side =TOP , expand = YES,fill=BOTH)
        self.detail2frame = Frame(self.bottomFrame, background ='#333579')
        self.detail2frame.pack(side = TOP, expand = YES,fill=BOTH)
        
#         self.top1 = Frame(self.topFrame, background ='#f09f10')
#         self.top1.pack(side = TOP,fill=BOTH, expand = YES)
#         self.top2 = Frame(self.topFrame, background ='#f09f10')
#         self.top2.pack(side = BOTTOM,fill=BOTH, expand = YES)
        self.display_on()
        self.mask_test()
    def detect_and_predict_mask(self,frame, faceNet, maskNet):
        # grab the dimensions of the frame and then construct a blob
        # from it
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
            (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        faceNet.setInput(blob)
        detections = faceNet.forward()

        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        locs = []
        preds = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the detection
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # compute the (x, y)-coordinates of the bounding box for
                # the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # ensure the bounding boxes fall within the dimensions of
                # the frame
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                # extract the face ROI, convert it from BGR to RGB channel
                # ordering, resize it to 224x224, and preprocess it
                #print(startY,endY, startX,endX)
                face = frame[startY:endY, startX:endX]
               # print(face)
                try:
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                    face = cv2.resize(face, (224, 224))
                    face = img_to_array(face)
                    face = preprocess_input(face)
                    face = np.expand_dims(face, axis=0)

                    # add the face and bounding boxes to their respective
                    # lists
                    faces.append(face)
                    locs.append((startX, startY, endX, endY))
                except:
                    pass

        # only make a predictions if at least one face was detected
        if len(faces) > 0:
            # for faster inference we'll make batch predictions on *all*
            # faces at the same time rather than one-by-one predictions
            # in the above `for` loop
            preds = maskNet.predict(faces)

        # return a 2-tuple of the face locations and their corresponding
        # locations
        return (locs, preds)
    def mask_test(self):
        #print('entered')
        global check,cnt,count,flag
        img=self.vs.read()
        img=cv2.resize(img, (int(1000), int(700)))
        img = cv2.flip(img, 1)
        temperature123=read_temp()
        #self.sl3.config(text="Show Your ID", fg='black', bg='#D5DBDB')
#         self.sl1.config(text="READY TO CHECK MASK.", fg='black', bg='#D5DBDB')
        while not temperature123:
            temperature123=read_temp()
        img1 = cv2.imread('/home/pi/Desktop/face_new/114.jpg' )
        img1=cv2.resize(img1, (int(1000), int(700)))         
        blended1 = cv2.addWeighted(src1=img,alpha=1,src2=img1,beta=0.9, gamma = 0)
#         cv2.imshow('1',blended1)
#         cv2.waitKey(1)
                
        if(check==0 or check==1):
            if(temperature123>float(temp)):
                self.sl2.config(text=str(temperature123)+" °F", fg='red', bg='#f09f10')
            else:
                self.sl2.config(text=str(temperature123)+" °F", fg='black', bg='#f09f10')
# abs
            try:
                (locs, preds) = self.detect_and_predict_mask(blended1, faceNet, maskNet)      
                print(preds)
                if(len(preds)>0):
                    for (box, pred) in zip(locs, preds):
                                # unpack the bounding box and predictions
                        (startX, startY, endX, endY) = box
                        (mask, withoutMask) = pred

                                # determine the class label and color we'll use to draw
                                # the bounding box and text
                        label = "Mask" if mask > withoutMask else "No Mask"
                        print(label,check)
                #                 color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                        
                        if(label == "No Mask" and  max(mask, withoutMask) * 100>50):
                            if(check==0):
                                subprocess.Popen("echo 'Please wear face mask' | festival --tts",shell=True)
                                
    #                             subprocess.Popen("python3 audio.py --model 'Please wear face mask'",shell=True)
                                time.sleep(1)
                                self.sl1.config(text="Please Wear Face Mask", fg='Yellow', bg='#333579')
                                count=0
                            elif(check==1):
                                self.sl2.config(text="Temperature Scanning", fg='black', bg='#f09f10')
                                self.sl3.config(text="Face Scanning...", fg='#FFFFFF', bg='#333579')
                                check=2
    #                             audio_out('Please wear face mask')
                        elif(label == "Mask" and  max(mask, withoutMask) * 100>90 and check== 0):
                            
                            count+=1
                            print('entered',count)
                            if(count>2):
                                    
#                                 subprocess.Popen("python3 audio.py --model 'show your face for attendance'",shell=True)
                                time.sleep(0.1)
                                subprocess.Popen("echo 'show your face for attendance' | festival --tts",shell=True)
                                self.sl1.config(text="Mask OK", fg='#FFFFFF', bg='#333579')
                                self.sl3.config(text="Show Your face", fg='#FFFFFF', bg='#333579')
    #                             audio_out('show your face for attendance')
                                
                                check=1
                        elif(check==1):
                            pass
                        else:
                            count=0
                            self.sl3.config(text="", fg='BLACK', bg='#333579')
                            self.sl1.config(text="SCANNING MASK...", fg='#FFFFFF', bg='#333579')
                elif(not(len(preds)>0 or check==1)):
                    self.sl3.config(text="", fg='BLACK', bg='#333579')
                    self.sl1.config(text="SCANNING MASK...", fg='#FFFFFF', bg='#333579')
            except:
                  self.sl3.config(text="", fg='BLACK', bg='#333579')
                  self.sl1.config(text="SCANNING MASK...", fg='#FFFFFF', bg='#333579')
        elif(check==2):
            print('entered face')
            self.sl2.config(text="Temperature Scanning", fg='black', bg='#f09f10')
            self.sl3.config(text="Face Scanning...", fg='#FFFFFF', bg='#333579')
            name=face.recognize(data,blended1)
#             cv2.imwrite(str(time.localtime()[5])+".jpg",blended1)
            print(name)
            if(name=='None'):
                    flag+=1
                    if(flag==35):
                        check=3
            else:
#                     print('excibit')
                    now=time.localtime()
                    temp_list=[now[0],now[1],now[2],now[3],now[4],now[5],str(temperature123)]
                    print(now)
                    if(len(str(now[1]))<2):
                            temp_list[1]='0'+str(now[1])
                    if(len(str(now[2]))<2):
                            temp_list[2]='0'+str(now[2])
                    if(len(str(now[3]))<2):
                            temp_list[3]='0'+str(now[3])
                    if(len(str(now[4]))<2):
                            temp_list[4]='0'+str(now[4])
                    if(len(str(now[5]))<2):
                            temp_list[5]='0'+str(now[5])
                    print(len(str(temperature123)))
                    if(len(str(temperature123))<5):
                        temp_list[6]='0'+str(temperature123)
                        print(str(temp_list[6]))
                    else:
                        temp_list[6]=str(temperature123)
                    k=1
                    try:
                        k=0
                        r_name=name
                        if(len(name)<8):
                            pri='0'*(8-len(name))
                            r_name=pri+name
                        time_stamp=str(temp_list[3])+str(temp_list[4])+str(temp_list[5])
                        date_stamp=str(temp_list[2])+str(temp_list[1])+str(temp_list[0])
                        detail="'"+reader_name+time_stamp+date_stamp+str(r_name)+"'"
                        conn1 = sqlite3.connect('attendance.db')
                        c1 = conn1.cursor()
                        print(temp_list)
                        data12="'"+str(temp_list[6])+"'"
                        print(detail)
                        c1.execute("INSERT INTO temp_attendance (Detail, temperature) VALUES (%s,%s)"% (detail,data12))
                        print('inserted')
                            # Save (commit) the changes
                        conn1.commit()
                        conn1.close()
                        
                        if(temperature123>float(temp)):
                            GPIO.output(R_LED,1)
                            GPIO.output(BUZZER,1)
                            time.sleep(2)
                            GPIO.output(BUZZER,0)
                            self.sl2.config(text=str(temperature123)+" °F", fg='RED', bg='#f09f10')
                            subprocess.Popen("echo 'Temperature Abnormal' | festival --tts",shell=True)
#                             audio_out('High Temperature Detected')
#                             subprocess.Popen("python3 audio.py --model 'High Temperature Detected Not Allowed'",shell=True)
                            self.sl3.config(text="EMP ID      : "+name, fg='#ffffff', bg='#333579')
                            self.test_data=udplib.Attend_send(name+"~"+str(temperature123),host_ip=host_ip,port_no=port_no,bufferSize = 1024)
                            
                            time.sleep(0.1)
                            try:
                                self.test_datas=self.test_data.split('~')
                                self.sl4.config(text="EMP Name : "+self.test_datas[1], fg='#ffffff', bg='#333579')
                            except:
                                self.sl4.config(text=" ", fg='#ffffff', bg='#333579')
                            self.sl1.config(text="Not Allowed", fg='RED', bg='#333579')
                            #audio_out('Not Allowed')

                        else:
                            GPIO.output(G_LED,1)
                            self.sl2.config(text=str(temperature123)+" °F", fg='BLACK', bg='#f09f10')
                        
                            self.sl3.config(text="EMP ID      : "+name, fg='#ffffff', bg='#333579')
                            self.test_data=udplib.Attend_send(name+"~"+str(temperature123),host_ip=host_ip,port_no=port_no,bufferSize = 1024)
                            try:
                                self.test_datas=self.test_data.split('~')
                                self.sl4.config(text="EMP Name : "+self.test_datas[1], fg='#ffffff', bg='#333579')
                                self.sl1.config(text="Attendance Marked", fg='GREEN', bg='#333579')
                                subprocess.Popen("python3 audio.py --model 'Attendance Marked Successfully'",shell=True)
                            except:
                                self.sl1.config(text="Empty data detected", fg='RED', bg='#333579')
                                self.sl4.config(text=" ", fg='#ffffff', bg='#333579')
                            
                            time.sleep(0.1)
#                             audio_out('Attendance Marked Successfully')
                    except:
                        self.sl1.config(text="Server Connection Error", fg='RED', bg='#333579')
#                         self.sl1.config(text="Server Connection Error", fg='RED', bg='#333579')
                        #self.depositLabel["text"] = "Server Connection Error"
#                         self.test_data="~~~~~"                
                    #self.sl1.config(text="READY TO CHECK MASK.", fg='black', bg='#D5DBDB')
                    check=3
        elif(check==3):
            cnt+=1
            if(cnt==5):
                flag=0
                GPIO.output(BUZZER,0)
                GPIO.output(G_LED,0)
                GPIO.output(R_LED,0)
                check=0
                cnt=1
                count=0
                self.sl4.config(text="", fg='#FFFFFF', bg='#333579')
                self.sl3.config(text="", fg='#FFFFFF', bg='#333579')
                self.sl1.config(text="SCANNING MASK...", fg='#FFFFFF', bg='#333579')
                self.sl2.config(text="", fg='#FFFFFF', bg='#333579')
        self.sl2.after(1000, self.mask_test)    
    def display_on(self):
        self.sl1 = Label(self.bottomFrame ,width=26,height=2,font= ('Garamond', 34 , 'bold'), justify=LEFT)
        self.sl1.pack(side=TOP, expand = YES ,fill=BOTH,anchor=CENTER,padx=0,pady=1)
        self.sl1.config(text="SCANNING MASK...", fg='#FFFFFF', bg='#333579')
        
        self.sl2 = Label(self.middleFrame ,width=26,height=1,font= ('Garamond', 34 , 'bold'), justify=LEFT)
        self.sl2.pack(side=LEFT,anchor=CENTER,padx=0,pady=5)
        self.sl2.config(text="Temperature Scanning...", fg='black', bg='#f09f10')
        
        self.sl3 = Label(self.detail1frame ,width=26,height=1,font= ('Garamond', 34 , 'bold'), justify=LEFT)
        self.sl3.pack(side=TOP, expand = YES ,fill=BOTH,anchor=W,padx=0,pady=1)
        self.sl3.config(text="", fg='#FFFFFF', bg='#333579')

        self.sl4 = Label(self.detail2frame ,width=26,height=1,font= ('Garamond', 34 , 'bold'), justify=LEFT)
        self.sl4.pack(side=TOP, expand = YES ,fill=BOTH,anchor=W,padx=0,pady=1)
        self.sl4.config(text="", fg='#FFFFFF', bg='#333579')
#         im = Image.open("/home/pi/Desktop/logo.png")
#         im = im.convert('RGB')
#         im = im.resize((205,51), Image.ANTIALIAS)
#         self.logo1=Label(self.logo1frame,bg='#ffffff')
#         self.logo1.pack(side=TOP, anchor=W,padx=0,pady=5)
#         self.photo = PIL.ImageTk.PhotoImage(master = self.logo1,image = im) 
#         self.logo1.config(image=self.photo)

        self.canvas = Canvas(self.topFrame, width = int(ws), height = int(hs/1.5), bg ='#ffffff')
        self.canvas.pack(side=TOP,anchor=CENTER,  padx=0,pady=1)
        self.update()
    def update(self):
            global check
            img=self.vs.read()
            #print(check)
            #print('hi')
            
            img=cv2.resize(img, (int(ws), int(hs/1.5)))
            img = cv2.flip(img, 1)
            frame = cv2.addWeighted(src1=img,alpha=1,src2=img2,beta=0.2, gamma = 0)
            
            frame=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            blended1 = cv2.addWeighted(src1=img,alpha=1,src2=img1,beta=0.9, gamma = 0)
            #if(check == 1):
                
            self.photo = PIL.ImageTk.PhotoImage(master=self.canvas,image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
            self.canvas.after(10, self.update)
ROOT.geometry('%dx%d+%d+%d' % (w, h, x, y))
ROOT.attributes("-fullscreen", True)
#ROOT.geometry('800X600')
ROOT.resizable(True, True) 
APP = App(ROOT)
ROOT.mainloop()    
