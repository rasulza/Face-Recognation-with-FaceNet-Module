import os
from os import listdir
from PIL import Image
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
from keras.models import load_model
import numpy as np
from django.conf import settings
import pickle
import cv2
from keras_facenet import FaceNet
from django.core.files import File
from home.models import FaceEmbedding
import cv2
import os
from os import listdir
from numpy import asarray, expand_dims
from PIL import Image
import pickle

def detect_save():
    HaarCascade = cv2.CascadeClassifier(os.path.join(settings.STATIC_DIR ,'models/haarcascade_frontalface_default.xml'))
    MyFaceNet = FaceNet()
    folder = os.path.join(settings.MEDIA_ROOT,'images/') 
    database = {}
    
    for filename in listdir(folder):
        path = folder + filename
        gbr1 = cv2.imread(folder + filename)
        
        wajah = HaarCascade.detectMultiScale(gbr1,1.1,4)
        
        if len(wajah)>0:
            x1, y1, width, height = wajah[0]         
        else:
            x1, y1, width, height = 1, 1, 10, 10
            
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        
        gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)                  # konversi dari OpenCV ke PIL
        gbr_array = asarray(gbr)
        
        face = gbr_array[y1:y2, x1:x2]                        
        
        face = Image.fromarray(face)                       
        face = face.resize((160,160))
        face = asarray(face)
        
        face = face.astype('float32')
        mean, std = face.mean(), face.std()
        face = (face - mean) / std
        
        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)
        
        # Create a new record in the database
        face_data = FaceEmbedding(name=os.path.splitext(filename)[0], embedding= signature)
        face_data.save()

        database[os.path.splitext(filename)[0]]=signature

    return database