# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


def face_encode(location=os.getcwd()+"/dataset",method='hog'):
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(location))
    try:
        with open('/home/pi/share/encodings1.pickle', 'rb') as f:
            knownEncodings = pickle.load(f)
    # initialize the list of known encodings and known names
    except:
        knownEncodings = {}

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
        if(name in knownEncodings.keys()):
            pass
        else:
           knownEncodings[name] =[]
        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model=method)

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            KE=knownEncodings[name]
            KN=KE+encoding
            knownEncodings[name]=KN
    print(knownEncodings)
    f = open("/home/pi/share/encodings1.pickle", "wb")
    f.write(pickle.dumps(knownEncodings))
    f.close()
#     pickle_make(knownEncodings)
def pickle_make(knownEncodings):
    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    i=1
    try:
        i=0
        with open('/home/pi/share/encodings.pickle', 'rb') as f:
            mylist = pickle.load(f)
        encodings=mylist["encodings"]
        names=mylist["names"]
        KE=encodings+knownEncodings
        KN=names+knownNames
        
        data = {"encodings": KE, "names": KN}
        f = open("/home/pi/share/encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()
        print("complete1")
    except:
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open("/home/pi/share/encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()
        print("complete2")
if __name__=="__main__":
    face_encode()
    #pickle_make(knownEncodings,knownNames) 
