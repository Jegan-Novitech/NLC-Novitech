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
import pyautogui
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2,message
import os,subprocess
from multiprocessing.pool import ThreadPool
import serial
import face_match as face
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
subprocess.Popen("python3 audio.py --model 'Device Initiating Please wait'",shell=True)
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
from imutils import paths
data=face_train()
import time,subprocess,random
check=0
cnt=1
count=0
flag=1
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
        self.emp_img = Frame(self.bottomFrame, background ='#333579')
        self.emp_img.pack(side = LEFT, expand = NO,fill=BOTH)
        self.emp_detail = Frame(self.bottomFrame, background ='#333579')
        self.emp_detail.pack(side = RIGHT, expand = NO,fill=BOTH)
        self.display_on()
        pyautogui.moveTo(260, 80)
        time.sleep(0.2)
        pyautogui.click()
        #self.mask_test()
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
        if(len(preds)>0):
            for (box, pred) in zip(locs, preds):
                                # unpack the bounding box and predictions
                        (startX, startY, endX, endY) = box
                        (mask, withoutMask) = pred

                        label = "Mask" if mask > withoutMask else "No Mask"
                        if(label == "No Mask" and  max(mask, withoutMask) * 100>50):
                            return "No Mask"
                        elif(label == "Mask" and  max(mask, withoutMask) * 100>90):
                            return "Mask"
                        else:
                            return "No Face"
        else:
            return "No Face"
        # return a 2-tuple of the face locations and their corresponding
        # locations
#         return (locs, preds)
    def barcode_read(self,event):
        global flag
        self.depositLabel["text"] = '        Your ID         '
        self.b_id=self.depositEntry.get()
#         print(self.b_id)
        location=os.getcwd()+"/dataset/"+str(self.b_id)
        imagePaths = list(paths.list_images(location))
#         z=1
#         while z:
#             z=0
        try:
            for (i, imagePath) in enumerate(imagePaths):
                print(imagePath)
            print(imagePath)
            image = Image.open(imagePath)
            image = image.resize((250,250), Image.ANTIALIAS)
            frame_image = ImageTk.PhotoImage(image)
            self.employee_img.config(image=frame_image)    
            self.employee_img.image = frame_image
            z=1
            while z:
                z=0
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
                mask=self.detect_and_predict_mask(blended1, faceNet, maskNet)
                print(mask)
                
                if(mask=="No Mask"):
                    state=1
                    if(flag==1):
                        self.sl3.config(text="Mask Not Wear", fg='#000000', bg='RED')
                    else:
                        flag=1
                    if(temperature123>float(temp)):
                            GPIO.output(R_LED,1)
                            GPIO.output(BUZZER,1)
                            time.sleep(2)
                            GPIO.output(BUZZER,0)
                            self.sl1.config(text=str(temperature123)+" °F", fg='#000000', bg='RED')
                    else:
                        self.sl1.config(text=str(temperature123)+" °F", fg='#FFFFFF', bg='GREEN')
                        for i in range(1):
                            name=None
                            while name==None:
                                img=self.vs.read()
                                img=cv2.resize(img, (int(1000), int(700)))
                                img = cv2.flip(img, 1)
                                blended1 = cv2.addWeighted(src1=img,alpha=1,src2=img1,beta=0.9, gamma = 0)
                                name=face.recognize(data,blended1,self.b_id)
                                print('name=',name)
                        if(name):
                            self.test_data=udplib.Attend_send(self.b_id+"~"+str(temperature123),host_ip=host_ip,port_no=port_no,bufferSize = 1024)
                            GPIO.output(G_LED,1)
                            self.sl2.config(text="Face Matched", fg='#FFFFFF', bg='GREEN')
                        else:
                            GPIO.output(R_LED,1)
                            self.sl2.config(text="Face Not Matched", fg='#000000', bg='RED')
                elif(mask=="No Face"):
                    state=0
                else:
                    state=0
                    flag=0
                    self.sl2.config(text="Show Your Face", fg='#FFFFFF', bg='#333579')
                    self.sl3.config(text="Mask OK", fg='#FFFFFF', bg='GREEN')
        except:
            state=1
            imagePath="100.jpg"
            image = Image.open(imagePath)
            image = image.resize((250,250), Image.ANTIALIAS)
            frame_image = ImageTk.PhotoImage(image)
            self.employee_img.config(image=frame_image)    
            self.employee_img.image = frame_image    
            self.sl2.config(text="Not in Emp list", fg='#000000', bg='RED')
        self.sl2.after(3000, lambda: self.reset(state))
    def reset(self,state):
        
        GPIO.output(BUZZER,0)
        GPIO.output(G_LED,0)
        GPIO.output(R_LED,0)
        imagePath="100.jpg"
        if(state==1):
            self.name_var.set("")
            self.depositLabel["text"] = self.labelText
        
            self.b_id=""
            image = Image.open(imagePath)
            image = image.resize((250,250), Image.ANTIALIAS)
            frame_image = ImageTk.PhotoImage(image)
            self.employee_img.config(image=frame_image)    
            self.employee_img.image = frame_image
            self.sl2.config(text="Match State:", fg='#FFFFFF', bg='#333579')
            self.sl1.config(text="Temperature:", fg='#FFFFFF', bg='#333579')
            self.sl3.config(text="Mask State", fg='#FFFFFF', bg='#333579')
        else:
            self.sl2.config(text="Show Your Face", fg='#FFFFFF', bg='#333579')
            self.sl2.after(2000, lambda: self.barcode_read(self.b_id))
#             self.sl1.config(text="Temperature:", fg='#FFFFFF', bg='#333579')
#             self.sl3.config(text="Mask State", fg='#FFFFFF', bg='#333579')
    def display_on(self):
        self.labelText = '   Scan Your Barcode     '
        self.depositLabel = Label(self.topFrame, text = self.labelText, bg='#333579',font=('Garamond', 18, 'bold'))
        self.name_var=StringVar()
        self.depositEntry = Entry(self.topFrame,textvariable = self.name_var, width = 18, bg='#333579',font=('Garamond', 28, 'bold'))
        self.depositEntry.bind('<Return>', self.barcode_read)
        self.depositLabel.pack(side=TOP,anchor=N)
        self.depositEntry.pack(side=BOTTOM,anchor=N)
        
        self.sl1 = Label(self.emp_detail ,width=26,height=2,font= ('Garamond', 24 , 'bold'), justify=LEFT)
        self.sl1.pack(side=TOP,anchor=W, expand = YES ,fill=BOTH,padx=0,pady=1)
        self.sl1.config(text="Temperature:", fg='#FFFFFF', bg='#333579')
            
        self.sl2 = Label(self.emp_detail ,width=26,height=1,font= ('Garamond', 24 , 'bold'), justify=LEFT)
        self.sl2.pack(side=TOP,anchor=W,padx=0,pady=5)
        self.sl2.config(text="Match State:", fg='#FFFFFF', bg='#333579')
        self.sl3 = Label(self.emp_detail ,width=26,height=1,font= ('Garamond', 24 , 'bold'), justify=LEFT)
        self.sl3.pack(side=TOP,anchor=W,padx=0,pady=5)
        self.sl3.config(text="Mask State", fg='#FFFFFF', bg='#333579')
        
        self.employee_img=Label(self.emp_img, bg='#FFFFFF')
        self.employee_img.pack(side=TOP,anchor=S,padx=15,pady=0)
        image = Image.open("100.jpg")
            #print(name)
        image = image.resize((250,250), Image.ANTIALIAS)
#         image = image.convert('RGB')
        frame_image = ImageTk.PhotoImage(image)
        self.employee_img.config(image=frame_image)
        self.canvas = Canvas(self.middleFrame, width = int(ws), height = int(hs/1.5), bg ='#ffffff')
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
