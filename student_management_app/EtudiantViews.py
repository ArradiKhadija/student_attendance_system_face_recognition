from django.shortcuts import render
import cv2
import numpy as np
from PIL import Image
import os
import mysql.connector
from student_management_app.models import Utilisateur
def student_home(request):
    return render(request, "Modele_etudiant/etudiant_modele.html")
def prendre_photos(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff")
        id=staff_id
        face_id =id
        cam = cv2.VideoCapture (0)
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height
        face_detector = cv2.CascadeClassifier ( cv2.data.haarcascades + 'haarcascade_frontalface_default.xml' )
        print ( "\n [INFO] Initializing face capture. Look the camera and wait ..." )
        # Initialize individual sampling face count

        count = 0
        while (True) :

            ret, img = cam.read ()
            img = cv2.flip ( img, 1 )  # flip video image vertically
            gray = cv2.cvtColor ( img, cv2.COLOR_BGR2GRAY )
            faces = face_detector.detectMultiScale ( gray, 1.3, 5 )

            for (x, y, w, h) in faces :
                cv2.rectangle ( img, (x, y), (x + w, y + h), (255, 0, 0), 2 )
                count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite("C:/Users/azlgh/Desktop/student_management_system/student_management_app/image/user." + str (face_id ) + '.' + str ( count ) + ".jpg", gray[y :y + h, x :x + w] )
                cv2.imshow ( 'image', img )

            k = cv2.waitKey ( 10 ) & 0xff  # Press 'ESC' for exiting video

            if k == 27 :
                break
            elif count >= 30 :

                # Take 30 face sample and stop video
                break

        # Do a bit of cleanup
        print ( "\n [INFO] Exiting Program and cleanup stuff" )
        cam.release()
        cv2.destroyAllWindows()
        path = 'C:/Users/azlgh/Desktop/student_management_system/student_management_app/image'
        # noinspection PyUnresolvedReferences
        recognizer = cv2.face.LBPHFaceRecognizer_create ()
        detector = cv2.CascadeClassifier ( cv2.data.haarcascades + "haarcascade_frontalface_default.xml" )

        # function to get the images and label data
        # noinspection PyShadowingNames
        def getImagesAndLabels(path) :

            imagePaths = [os.path.join ( path, f ) for f in os.listdir ( path )]
            faceSamples = []
            ids = []

            for imagePath in imagePaths :
                PIL_img = Image.open ( imagePath ).convert ( 'L' )
                # convert it to grayscale
                img_numpy = np.array ( PIL_img, 'uint8' )

                id = int ( os.path.split ( imagePath )[1].split ( "." )[1] )
                faces = detector.detectMultiScale ( img_numpy )

                for (x, y, w, h) in faces :
                    faceSamples.append ( img_numpy[y :y + h, x :x + w] )
                    ids.append ( id )
            return faceSamples, ids

        print ( "\n [INFO] Training faces. It will take a few seconds. Wait ..." )
        faces, ids = getImagesAndLabels ( path )
        recognizer.train ( faces, np.array ( ids ) )
        # Save the model into trainer/trainer.yml
        recognizer.write (
            'C:/Users/azlgh/Desktop/student_management_system/student_management_app/trainer/trainer.yml' )
        # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print ( "\n [INFO] {0} faces trained. Exiting Program".format ( len ( np.unique ( ids ) ) ) )
    return render(request,"Modele_etudiant/prendre_photos.html")