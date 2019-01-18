# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:43:31 2019

@author: Diego
"""
#importation of libraries
import numpy as np
import time
import cv2
pygame.init() #Initialize the pygame library to make it sound
### CREATE THE ASSISTANT FUNCTION ###
# Setup the camera
camara = cv2.VideoCapture(0)
count = 0
countf = 0
#instance to save the data
f = open('datos.csv','w')
# Load the classifiers Haar-Cascade for detecting faces
rostro_deteccion = cv2.CascadeClassifier('/var/projects/opencv-3.0.0/data/haarcascades/lbpcascade_frontalface.xml')
# Load the libraries Haar-Cascade for detecting Eyes and profile face
ojos_deteccion = cv2.CascadeClassifier('/var/projects/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')
perfil_deteccion = cv2.CascadeClassifier('/var/projects/opencv-3.0.0/data/haarcascades/lbpcascade_profileface.xml')
### Main ####
# Capture frames from the camera
while 1:
    ret1, image = camara.read()
    # we use the OpenCv libraries to convert the image to grayscale
    gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    kernel = np.ones((3,3),np.uint8)
    # we use the OpenCV libraries to equalize the histogram of the grayscale image
    img = cv2.equalizeHist( gray )
    # We use the Erode library to eliminate noise from the image
    transformacion = cv2.erode(img,kernel,iterations = 1)
    #load the transformation into a variable
    faces = rostro_deteccion.detectMultiScale(transformacion, 1.3, 5)
    rostro_perfil = perfil_deteccion.detectMultiScale(transformacion, 1.3, 5)
    print "Found " + str( len( faces ) ) + " face(s)" # Print on console the number of faces detected
    # Draw a rectangle around every face and move the motor towards the face
    if (int(str( len( faces ))) == 0):
        countf = countf + 1
        print "no cara"
    for ( x, y, w, h ) in faces:
        ojos_gris = transformacion[y:y+h, x:x+w]
        ojos = ojos_deteccion.detectMultiScale(ojos_gris)        
        cv2.rectangle(transformacion,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText( transformacion, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )#
        print "Found " + str( len( ojos ) ) + " eyes(s)"
        
         # Draw a rectangle around every eye and move the motor towards the eye
        for (ex,ey,ew,eh) in ojos:
            count = count + 1                  
            cv2.rectangle(ojos_gris,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            cv2.putText( ojos_gris, "Eyes No." + str( len( ojos ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )                
            print "entro a ojos"
            if (int(str( len( ojos ))) == 0):
                count = 0
            #wax the counter    
                print count
    if(count >= 5):
	#save the data obtained in the csv file
        e = "HORA DE ALERTA OJOS: ",time.strftime("%d/%m/%y"),time.strftime("%I:%M:%S")                        
        f.write(str(e)+'\n')
        count=0
		#send a sound alert
        pygame.mixer.music.load("/home/pi/Desktop/Paper/alerta1.wav")
        pygame.mixer.music.play()
        print "Detecta ojos"   
    if(countf >= 5):
	    #save the data obtained in the csv file
        e = "HORA DE ALERTA CARA: ",time.strftime("%d/%m/%y"),time.strftime("%I:%M:%S")                        
        f.write(str(e)+'\n')
		#send a sound alert
        pygame.mixer.music.load("/home/pi/Desktop/Paper/alerta1.wav")
        pygame.mixer.music.play()
        countf=0
        print "Detecta no cara 1"                     
     # Show the frame
    cv2.imshow('Erosion', transformacion)    
    k = cv2.waitKey(30) & 0xff #define key for program output
    if k == 27:
        break
	#end of the program, close the file and the camera
f.close()
camara.realease()
cv2.destroyAllWindows()

