import face_recognition,time,cv2
import numpy as np
start=time.time()
# Load the jpg files into numpy arrays
biden_image = cv2.imread("1.jpg")
obama_image = cv2.imread("1.jpg")
unknown_image =cv2.imread("2.jpg")

# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
    print(biden_face_encoding,"1")
    rgb = cv2.cvtColor(biden_image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,
            model="hog")
    biden_face_encoding = face_recognition.face_encodings(rgb, boxes)
    print(biden_face_encoding,"2")
    rgb = cv2.cvtColor(obama_image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,
            model="hog")
    obama_face_encoding = face_recognition.face_encodings(rgb, boxes)
    
    rgb = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,
            model="hog")
    unknown_face_encoding = face_recognition.face_encodings(rgb, boxes)
    
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

known_faces = [
    biden_face_encoding[0],
    obama_face_encoding[0]
]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding[0])
end=time.time()
print("Is the unknown face a picture of Biden? {}".format(results[0]))
print("Is the unknown face a picture of Obama? {}".format(results[1]))
print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
print(end-start)