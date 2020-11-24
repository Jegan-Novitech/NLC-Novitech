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
G_LED=20
R_LED=16
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
import recognize_faces_video as face
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



d6t = grove_d6t.GroveD6t()

def face_train(Name='nothing'):
        #global data
        try:
                data=face.start(Name)
        except:
                data=''
        return data
def read_temp():
    tpn, tptat = d6t.readData()
    if tpn == None:
        return 0
    tpn1=tpn[8:12]+tpn[12:16]
    calib_temp=round((36.0+(36-38)*(max(tpn1))/(33.1-36.1))/1.6,1)
    #print(calib_temp)
    temp=float(round((calib_temp* 9/5 + 32),1))
    if(type(temp)!=type(99.0)):
        temp=0
    return temp
img2 = cv2.imread('/home/pi/Desktop/face_new/113.jpg' )
ret,img2 = cv2.threshold(img2,127,255,cv2.THRESH_BINARY_INV)
print(img2)
img2=cv2.resize(img2, (int(ws), int(hs/1.2)))
img1 = cv2.imread('/home/pi/Desktop/face_new/114.jpg' )
img1=cv2.resize(img1, (int(ws), int(hs/1.2)))
#img_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
def detect_and_predict_mask(frame, faceNet, maskNet):
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

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
    "res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
#cap = VideoStream(src=0).start()
# cap = VideoStream(src=0,usePiCamera=1).start()
# time.sleep(2)

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
        self.middleFrame = Frame(self.tk, background ='#333579')
        self.topFrame.pack(side = TOP,fill=BOTH, expand = NO)
        self.middleFrame.pack(side = TOP, expand = YES,fill=BOTH)
        self.bottomFrame.pack(side = TOP, expand = YES,fill=BOTH)
        self.logo1frame = Frame(self.bottomFrame, background ='#333579')
        self.logo1frame.pack(side = LEFT, expand = YES,fill=BOTH)
        self.logo2frame = Frame(self.bottomFrame, background ='#333579')
        self.logo2frame.pack(side = RIGHT, expand = YES,fill=BOTH)
        self.detail1frame = Frame(self.logo2frame, background ='#333579')
        self.detail1frame.pack(side = LEFT, expand = YES,fill=BOTH)
        self.detail2frame = Frame(self.logo2frame, background ='#333579')
        self.detail2frame.pack(side = RIGHT, expand = YES,fill=BOTH)
        
        self.top1 = Frame(self.topFrame, background ='#f09f10')
        self.top1.pack(side = TOP,fill=BOTH, expand = YES)
        self.top2 = Frame(self.topFrame, background ='#f09f10')
        self.top2.pack(side = BOTTOM,fill=BOTH, expand = YES)
        self.display_on()
        self.mask_test()
    def mask_test(self):
        img=self.vs.read()
        img=cv2.resize(img, (int(ws), int(hs/1.2)))
        img = cv2.flip(img, 1)
        temperature123=read_temp()
        self.sl3.config(text="Show Your ID", fg='black', bg='#D5DBDB')
        while not temperature123:
            temperature123=read_temp()
        if(temperature123>100):
            self.sl2.config(text="Temperature="+str(temperature123)+" °F", fg='black', bg='red')
        else:
            self.sl2.config(text="Temperature="+str(temperature123)+" °F", fg='black', bg='#D5DBDB')
        self.sl1.config(text="READY TO CHECK MASK.", fg='black', bg='#D5DBDB')
        blended1 = cv2.addWeighted(src1=img,alpha=1,src2=img1,beta=0.9, gamma = 0)
        
        (locs, preds) = detect_and_predict_mask(blended1, faceNet, maskNet)      
        print(preds)
        if(len(preds)>0):
            for (box, pred) in zip(locs, preds):
                    # unpack the bounding box and predictions
                (startX, startY, endX, endY) = box
                (mask, withoutMask) = pred

                    # determine the class label and color we'll use to draw
                    # the bounding box and text
                label = "Mask" if mask > withoutMask else "No Mask"
    #                 color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                if(label == "No Mask"):
                    self.sl1.config(text="Please Wear Face Mask", fg='#FFFFFF', bg='RED')
                else:
                    self.sl1.config(text="Mask OK", fg='#FFFFFF', bg='GREEN')
                    barcodes = pyzbar.decode(img)
                    if(len(barcodes)<1):
                        self.sl3.config(text="Show Your ID", fg='black', bg='#D5DBDB')
                    else:
                        for barcode in barcodes:
                                        # extract the bounding box location of the barcode and draw
                                        # the bounding box surrounding the barcode on the image
                            (x, y, w, h) = barcode.rect
                            barcodeData = barcode.data.decode("utf-8")
                            barcodeType = barcode.type
                            # draw the barcode data and barcode type on the image
                            text = "{} ".format(barcodeData)
                            #cv2.putText(frame, text, (100,100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                            if(temperature123>100):
                                self.sl3.config(text="Your ID="+text, fg='#ffffff', bg='red')
                                self.sl2.config(text="Temperature="+str(temperature123)+" °F", fg='black', bg='red')
                            else:
                                self.sl3.config(text="Your ID="+text, fg='#ffffff', bg='green')
                                self.sl2.config(text="Temperature="+str(temperature123)+" °F", fg='#FFFFFF', bg='green')
        self.sl2.after(2000, self.mask_test)    
    def display_on(self):
        self.sl1 = Label(self.top1 ,width=26,height=2,font= ('Arial', 20 , 'bold'), justify=LEFT)
        self.sl1.pack(side=TOP, expand = YES ,fill=BOTH,anchor=CENTER,padx=0,pady=1)
        self.sl1.config(text="READY TO CHECK MASK.", fg='black', bg='#D5DBDB')
        
        self.sl2 = Label(self.top2 ,width=26,height=1,font= ('Arial', 20 , 'bold'), justify=LEFT)
        self.sl2.pack(side=LEFT, expand = YES ,fill=BOTH,anchor=CENTER,padx=0,pady=1)
        self.sl2.config(text="Temperature:", fg='black', bg='#D5DBDB')
        
        self.sl3 = Label(self.top2 ,width=26,height=1,font= ('Arial', 20 , 'bold'), justify=LEFT)
        self.sl3.pack(side=RIGHT, expand = YES ,fill=BOTH,anchor=CENTER,padx=0,pady=1)
        self.sl3.config(text="Show Your ID", fg='black', bg='#D5DBDB')

        im = Image.open("/home/pi/Desktop/logo.png")
        im = im.convert('RGB')
        im = im.resize((205,51), Image.ANTIALIAS)
        self.logo1=Label(self.logo1frame)
        self.logo1.pack(side=TOP, anchor=W,padx=0,pady=5)
        self.photo = PIL.ImageTk.PhotoImage(master = self.logo1,image = im) 
        self.logo1.config(image=self.photo)

        self.canvas = Canvas(self.middleFrame, width = int(ws), height = int(hs/1.2), bg ='#ffffff')
        self.canvas.pack(side=TOP,anchor=CENTER,  padx=0,pady=1)
        self.update()
    def update(self):
            img=self.vs.read()
            
            #print('hi')
            
            img=cv2.resize(img, (int(ws), int(hs/1.2)))
            img = cv2.flip(img, 1)
            frame = cv2.addWeighted(src1=img,alpha=1,src2=img2,beta=0.2, gamma = 0)
            
            frame=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
#                     frame =cv2.rectangle(frame,(384,0),(710,228),(255,0,0),3)
#                     crop_img = frame[0:228, 384:710]
                    
                    
            self.photo = PIL.ImageTk.PhotoImage(master=self.canvas,image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
            self.canvas.after(10, self.update)
ROOT.geometry('%dx%d+%d+%d' % (w, h, x, y))
ROOT.attributes("-fullscreen", True)
#ROOT.geometry('800X600')
ROOT.resizable(True, True) 
APP = App(ROOT)
ROOT.mainloop()    
