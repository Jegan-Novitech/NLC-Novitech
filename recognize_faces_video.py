# USAGE
# python recognize_faces_video.py --encodings encodings.pickle
# python recognize_faces_video.py --encodings encodings.pickle --output output/jurassic_park_trailer_output.avi --display 0

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
    data = pickle.loads(open("/home/farent-t2/share/encodings.pickle", "rb").read())
    return(data)

def recognize(data,frame):
    
    writer = None
    #time.sleep(2.0)
    name='None'
    # loop over frames from the video file stream
    i=1
    while i:
        # grab the frame from the threaded video stream
        
        start_time=time.time()
        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        #rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=200)
        r = frame.shape[1] / float(rgb.shape[1])

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        # the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb,
            model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],encoding,tolerance=0.45)
            name = "Unknown"
            
            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
            
        i=0
        return name
          

if __name__=="__main__":
      print("[INFO] starting video stream...")
      data=start()
      vs = VideoStream(src=0).start()
      while 1:
        img1 = cv2.imread('114.jpg' )
        img1=cv2.resize(img1, (int(1000), int(700)))
        img=vs.read()
        img=cv2.resize(img, (int(1000), int(700)))
        img = cv2.flip(img, 1)
        blended1 = cv2.addWeighted(src1=img,alpha=1,src2=img1,beta=0.9, gamma = 0)
        cv2.imshow("frame",blended1)
        cv2.waitKey(1)
        print(recognize(data,blended1))
    
