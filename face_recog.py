import os
from tqdm import tqdm
import numpy as np
import pandas as pd
import cv2
import time
import re,pickle
from imutils.video import VideoStream
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace, DeepID
from deepface.extendedmodels import Age, Gender, Race, Emotion
from deepface.commons import functions, realtime, distance as dst

def embedded(db_path,model_name,model,input_shape = (224, 224)):
    file_name = "representations_%s.pkl" % (model_name)
##    input_shape = (224, 224)
    input_shape_x = input_shape[0]; input_shape_y = input_shape[1]
    
    text_color = (255,255,255)
    
    employees = []
    #check passed db folder exists
    if os.path.isdir(db_path) == True:
            for r, d, f in os.walk(db_path): # r=root, d=directories, f = files
                    for file in f:
                            if ('.jpg' in file):
                                    #exact_path = os.path.join(r, file)
                                    exact_path = r + "/" + file
                                    #print(exact_path)
                                    employees.append(exact_path)
                                    
    if len(employees) == 0:
            print("WARNING: There is no image in this path ( ", db_path,") . Face recognition will not be performed.")
    
    tic = time.time()
    
    pbar = tqdm(range(0, len(employees)), desc='Finding embeddings')
    
    embeddings = []
    #for employee in employees:
    for index in pbar:
            employee = employees[index]
            pbar.set_description("Finding embedding for %s" % (employee.split("/")[-1]))
            embedding = []
            img = functions.preprocess_face(img = employee, target_size = (input_shape_y, input_shape_x), enforce_detection = False)
            img_representation = model.predict(img)[0,:]
            
            embedding.append(employee)
            embedding.append(img_representation)
            embeddings.append(embedding)
    
    f = open(db_path+'/'+file_name, "wb")
    pickle.dump(embeddings, f)
    f.close()
    toc = time.time()
    
    print("Embeddings found for given data set in ", toc-tic," seconds")
def create_model(db_path, model_name):
    if model_name == 'VGG-Face':
            print("Using VGG-Face model backend and")
            model = VGGFace.loadModel()
            input_shape = (224, 224)    
    
    elif model_name == 'OpenFace':
            print("Using OpenFace model backend")
            model = OpenFace.loadModel()
            input_shape = (96, 96)
    
    elif model_name == 'Facenet':
            print("Using Facenet model backend")
            model = Facenet.loadModel()
            input_shape = (160, 160)
    
    elif model_name == 'DeepFace':
            print("Using FB DeepFace model backend")
            model = FbDeepFace.loadModel()
            input_shape = (152, 152)
    
    elif model_name == 'DeepID':
            print("Using DeepID model backend")
            model = DeepID.loadModel()
            input_shape = (55, 47)
    
    elif model_name == 'Dlib':
            print("Using Dlib model backend")
            from deepface.basemodels.DlibResNet import DlibResNet
            model = DlibResNet()
            input_shape = (150, 150)
    
    else:
            raise ValueError("Invalid model_name passed - ", model_name)
    return model,input_shape

def analysis(img,db_path,input_shape, model_name,distance_metric,  model=None,enable_face_analysis = True):
    if(model==None):
        model,input_shape=create_model(db_path, model_name)
    file_name = "representations_%s.pkl" % (model_name)
    f = open(db_path+'/'+file_name, 'rb')
    embeddings = pickle.load(f)
#     print(embeddings)
    input_shape_x = input_shape[0]; input_shape_y = input_shape[1]
    time_threshold = 5; frame_threshold = 5
    pivot_img_size = 112 #face recognition result image

    #-----------------------
    
    opencv_path = functions.get_opencv_path()
    face_detector_path = opencv_path+"haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(face_detector_path)
    
    #-----------------------

    freeze = False
    face_detected = False
    face_included_frames = 0 #freeze screen if face detected sequantially 5 frames
    freezed_frame = 0
    tic = time.time()
    text_color = (255,255,255)
    
    employees = []
    #check passed db folder exists
    if os.path.isdir(db_path) == True:
        for r, d, f in os.walk(db_path): # r=root, d=directories, f = files
            for file in f:
                if ('.jpg' in file):
                        #exact_path = os.path.join(r, file)
                        exact_path = r + "/" + file
                        #print(exact_path)
                        employees.append(exact_path)
                            
    df = pd.DataFrame(embeddings, columns = ['employee', 'embedding'])
    df['distance_metric'] = distance_metric
#     cap = VideoStream(src=0,usePiCamera=True,framerate=32).start()
    threshold = functions.findThreshold(model_name, distance_metric)
#     time.sleep(2)
    i=1
    while i:
        label='None'
        i=0
        start=time.time()
#         img = cap.read()
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        for (x,y,w,h) in faces:       
            custom_face = functions.preprocess_face(img = img, target_size = (input_shape_y, input_shape_x), enforce_detection = False)                 
            #check preprocess_face function handled
            if custom_face.shape[1:3] == input_shape:
                    if df.shape[0] > 0: #if there are images to verify, apply face recognition
                            img1_representation = model.predict(custom_face)[0,:]
    ##                        print(img1_representation)
                            #print(freezed_frame," - ",img1_representation[0:5])
                            
                            def findDistance(row):
                                    distance_metric = row['distance_metric']
                                    img2_representation = row['embedding']
                                    
                                    distance = 1000 #initialize very large value
                                    if distance_metric == 'cosine':
                                            distance = dst.findCosineDistance(img1_representation, img2_representation)
                                    elif distance_metric == 'euclidean':
                                            distance = dst.findEuclideanDistance(img1_representation, img2_representation)
                                    elif distance_metric == 'euclidean_l2':
                                            distance = dst.findEuclideanDistance(dst.l2_normalize(img1_representation), dst.l2_normalize(img2_representation))
                                            
                                    return distance
                            
                            df['distance'] = df.apply(findDistance, axis = 1)
                            df = df.sort_values(by = ["distance"])
                            
                            candidate = df.iloc[0]
                            employee_name = candidate['employee']
                            best_distance = candidate['distance']
                            
    ##                        print(candidate[['employee', 'distance']].values)
    ##                        print(threshold)
                            #if True:
                            if best_distance <= threshold:
                                    #print(employee_name)
                                    end=time.time()
                                    display_img = cv2.imread(employee_name)
                                    
                                    display_img = cv2.resize(display_img, (pivot_img_size, pivot_img_size))
                                                                                                            
                                    label = employee_name.split("/")[-2].replace(".jpg", "")
    ##                                print(label)
#                                     hex_string = "0x5C"[2:]
#                                     bytes_object = bytes.fromhex(hex_string)
#                                     ascii_string = bytes_object.decode("ASCII")
#                                     label =  label.split(ascii_string)[-1]
                                    print(best_distance,"--->",label,"----->",str(end-start))
#                                     cv2.putText(img, str(label), (100,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
                            else:
                                label =  "Unkown"
#                                 cv2.putText(img, str(label), (100,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
#                             cv2.rectangle(img, (x,y), (x+w,y+h), (67,167,67), 1)
        return label
#         cv2.imshow("image",img)
#         cv2.waitKey(1)

# model1,input_shape1=create_model(db_path="/home/pi/Desktop/deepface_check/dataset", model_name="Facenet")
# embedded(db_path="/home/pi/Desktop/deepface_check/dataset",model_name="Facenet",model=model1,input_shape=input_shape1)
# analysis(db_path="/home/pi/Desktop/deepface_check/dataset", model_name="Facenet", distance_metric = 'cosine', enable_face_analysis = False)
