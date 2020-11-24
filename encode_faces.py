# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
global name1
def face_encode(location,name1,method='hog'):
	# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(location))
	print(location)

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,
			len(imagePaths)))
		#name = imagePath.split(os.path.sep)[1]
		name=name1
		#print(name)

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
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)
	print(len(knownEncodings),len(knownNames))
	location2='E:/facerecogcodewithdlib - Copy/pikfile'
	pickle_make(knownEncodings,knownNames,location2,name1)
def pickle_make(knownEncodings,knownNames,location2,name1):
	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	#print(name1)
	#print(location2)

	try:
		with open(location2+'/'+name1+'encodings.pickle', 'rb') as f:
			mylist = pickle.load(f)
		encodings=mylist["encodings"]
		names=mylist["names"]
		KE=encodings+knownEncodings
		KN=names+knownNames
		
		data = {"encodings": KE, "names": KN}
		f = open(location2+"/"+name1+"encodings.pickle", "wb")
		f.write(pickle.dumps(data))
		f.close()
		print("complete1")
	except:
		data = {"encodings": knownEncodings, "names": knownNames}
		f = open(location2+"/"+name1+"encodings.pickle", "wb")
		f.write(pickle.dumps(data))
		f.close()
		print("complete2")
location='E:/facerecogcodewithdlib - Copy/dataset'
import os
files = os.listdir(location)
for name1 in files:
        #print(name1)
        face_encode(location,name1)
if __name__=="__main__":
        location='E:/facerecogcodewithdlib - Copy/dataset'
        	
