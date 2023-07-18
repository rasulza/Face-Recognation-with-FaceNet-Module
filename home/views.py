import cv2
import os
import numpy as np 
from PIL import Image
from django import views
from .models import Order, One_Bread_Order
from .forms import Number_Bread
from django.conf import settings
from django.db.models import Sum
from keras_facenet import FaceNet
from numpy import asarray, expand_dims
from django.shortcuts import render, redirect
import time




class Home_view(views.View):
    def get(self, request):
        orders = Order.objects.all()
        One_Bread_Orders = One_Bread_Order.objects.all()
        return render(request, 'home/home.html',{'orders':orders,'one_breads':One_Bread_Orders})


class BreadStatusView(views.View):

    
    def get(self, request):
        form = Number_Bread()
        return render(request,'home/bread_num.html', {'form':form})


    def post(self, request):
                        
            form = Number_Bread(request.POST)
            if form.is_valid():

                HaarCascade = cv2.CascadeClassifier(os.path.join(settings.STATIC_DIR,'models/haarcascade_frontalface_default.xml'))
                eye_cascade = cv2.CascadeClassifier(os.path.join(settings.STATIC_DIR,'models/haarcascade_eye.xml'))
                MyFaceNet = FaceNet()
                cap = cv2.VideoCapture(0)
                while True:
                    

                    if not cap.isOpened():
                        break
                    ret, frame = cap.read()
                    if ret == False:
                        break
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    face = HaarCascade.detectMultiScale(gray,1.1,4)
                    eyes_detected = False
                    cv2.imshow('frame', frame)
                    for (x, y, w, h) in face:
                        face_img = frame[y:y+h, x:x+w]  
                        
                                
                        eyes = eye_cascade.detectMultiScale(face_img, scaleFactor=1.1, minNeighbors=12)
                        if len(eyes) == 2:
                            eyes_detected = True
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (250, 0, 0), 2)
                            for (ex, ey, ew, eh) in eyes:                                           
                                cv2.rectangle(face_img, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                                
                                
                                rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                rgb_img = Image.fromarray(rgb_img)
                                img_array = asarray(rgb_img)

                                detected_face = HaarCascade.detectMultiScale(frame,1.1,4)
                                if len(detected_face) == 0:
                                    break 
                                x1, y1, w, h = detected_face[0]
                                x1, y1 = abs(x1), abs(y1)
                                x2, y2 = x1 + w , y1 + h

                                face_crop = img_array[y1:y2,x1:x2]
                                
                                face_crop = Image.fromarray(face_crop) 
                                face_crop = face_crop.resize((160,160))
                                face_crop = asarray(face_crop)

                                face_crop = expand_dims(face_crop,axis=0)
                                signature = MyFaceNet.embeddings(face_crop)
                                
                                min_dist=0.80
                                identity=''
                                identity_obj_One = ''

                                for obj in Order.objects.all():
                                    embedding = np.frombuffer(obj.embedding, dtype=np.float32)                                    
                                    dist = np.linalg.norm(embedding-signature)
                                    print(dist)                                    
                                    if dist < min_dist:
                                        min_dist = dist
                                        identity = obj.name

                                for obj_One in One_Bread_Order.objects.all():  
                                    embedding_obj_One = np.frombuffer(obj_One.embedding, dtype=np.float32)  
                                    dist_obj_one = np.linalg.norm(embedding_obj_One-signature)
                                    print(dist_obj_one)
                                    if dist_obj_one < min_dist:
                                        min_dist = dist_obj_one
                                        identity_obj_One = obj_One.name
                                    
                                number = form.cleaned_data['num']
                                
                                if identity == '' and identity_obj_One == '':
                                    if number > 1:
                                        name = str(Order.objects.count() + One_Bread_Order.objects.count() + 1)
                                        embedding = signature.tobytes()
                                        identity = name
                                        time_sec = number * 20
                                        times = Order.objects.aggregate(Sum('time'))
                                        wating_time = times['time__sum'] 
                                        if wating_time == None:
                                            wating_time = time_sec
                                        
                                        Order.objects.create(name=name,embedding=embedding,time=time_sec, waitingـtime=wating_time, bread_number=number)
                                    else:   
                                        name_obj_one = str(One_Bread_Order.objects.count() + Order.objects.count() + 1)
                                        embedding_obj_One = signature.tobytes()
                                        identity_obj_One = name_obj_one
                                        time_sec = number * 20
                                        times = One_Bread_Order.objects.aggregate(Sum('time'))
                                        wating_time = times['time__sum'] 
                                        if wating_time == None:
                                            wating_time = time_sec
                                                
                                        One_Bread_Order.objects.create(name=name_obj_one, embedding=embedding_obj_One,time=time_sec, waitingـtime=wating_time, bread_number=number)
                                      
                                else:
                                    print(f"you have already logged the user")
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return redirect('home:home')

                    if cv2.waitKey(1) == ord('q') or eyes_detected:         
                        cap.release()
                        cv2.destroyAllWindows()
                        break
            else:
                return render(request,'home/bread_num.html', {'form':form})   
            cap.release()
            cv2.destroyAllWindows()
            return redirect('home:home')


