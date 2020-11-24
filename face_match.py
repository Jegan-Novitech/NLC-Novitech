
# import the necessary packages
from imutils.video import VideoStream
import face_recognition

import imutils
import pickle
import time
import cv2,message


def start(name='nothing'):
    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    data = pickle.loads(open("/home/pi/share/encodings1.pickle", "rb").read())
    return(data)

def recognize(data,frame,id_no):
    
    writer = None
    #time.sleep(2.0)
    name='None'
    # loop over frames from the video file stream
    i=1
    while i:       
        start=time.time()
        rgb = imutils.resize(frame, width=200)
        r = frame.shape[1] / float(rgb.shape[1])
        boxes = face_recognition.face_locations(rgb,
            model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        print(encodings)
        names = []
        known_encodings=data[id_no]
        if(len(encodings)>0):
            for encoding in encodings:
                face= face_recognition.compare_faces(known_encodings,encodings,tolerance=0.40)
        else:
            face= [None]

        end=time.time()
        print(end-start)
        return face[0]

if __name__=="__main__":
      id_no='nvt003'
      print("[INFO] starting video stream...")
      data=start()
      vs = VideoStream(src=0).start()
      while 1:
        img1 = cv2.imread('/home/pi/Desktop/face_new/114.jpg' )
        img1=cv2.resize(img1, (int(1000), int(700)))
        img=vs.read()
        img=cv2.resize(img, (int(1000), int(700)))
        img = cv2.flip(img, 1)
        blended1 = cv2.addWeighted(src1=img,alpha=1,src2=img1,beta=0.9, gamma = 0)
        cv2.imshow("frame",blended1)
        cv2.waitKey(1)
        if(recognize(data,blended1,id_no)==True):
            print('match')
        elif(recognize(data,blended1,id_no)==False):
            print('not match')
    
