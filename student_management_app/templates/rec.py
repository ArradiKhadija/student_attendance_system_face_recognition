import cv2
import mysql.connector
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('C:/Users/azlgh/Desktop/student_management_system/student_management_app/trainer/trainer.yml')
cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
id=0
def select(id):
  connection = mysql.connector.connect(host="localhost",
                               user="student_management_system",
                               password="student_management_password",
                               database="student_management_system")


  mySql_insert_query = """SELECT student_management_app_etudiants.CodeApogee,student_management_app_utilisateur.first_name,student_management_app_utilisateur.last_name,
  student_management_app_etudiants.profile FROM student_management_app_utilisateur
  INNER JOIN student_management_app_etudiants ON student_management_app_utilisateur.id = student_management_app_etudiants.admin_id_id
   where student_management_app_utilisateur.id="""+str(id)
  cursor = connection.cursor()
  cursor.execute(mySql_insert_query)
  for row in cursor:
     profile=row
     cursor.close()
     return profile

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
    # Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
        ret, img = cam.read()
        img = cv2.flip(img, 1)  # Flip vertically

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(int(minW), int(minH)))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            profile = select(id)

            # Check if confidence is less them 100 ==> "0" is perfect match
            if confidence < 75:
                id = profile[2]
                confidence = " {0}%".format(round(100 - confidence))
                cv2.rectangle ( img, (x, y), (x + w, y + h), (0, 255, 0), 2 )

            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.rectangle ( img, (x, y), (x + w, y + h), (0, 25, 255), 2 )
            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 255), 1)
            try :
                connection = mysql.connector.connect ( host='localhost',
                                                       database='student_management_system',
                                                       user='student_management_system',
                                                       password='student_management_password' )
                mySql_insert_query = """INSERT INTO presence(CodeApogee,Nom,Prenom,Photo) VALUES(%s,%s,%s,%s)"""

                cursor = connection.cursor ()
                cursor.execute ( mySql_insert_query,(str ( profile[0] ), str ( profile[1] ), str ( profile[2] ), str ( profile[3] )) )
                connection.commit ()
                print ( cursor.rowcount, "Record inserted successfully into Guest table" )
                cursor.close ()
            except mysql.connector.Error as error :
                print ( "Failed to insert record into Laptop table {}".format ( error ) )

            finally :
                if (connection.is_connected ()) :
                    connection.close ()
                    print ( "MySQL connection is closed" )

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff
        # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
print ( "\n [INFO] Exiting Program and cleanup stuff" )
cam.release()
cv2.destroyAllWindows()


def marque() :
    connection = mysql.connector.connect ( host='localhost',
                                           database='student_management_system',
                                           user='student_management_system',
                                           password='student_management_password' )
    mySql_insert_query = f"""INSERT INTO liste_presence(CodeApogee,Nom,Prenom,Photo) SELECT CodeApogee,Nom,Prenom,Photo from presence group by CodeApogee;"""
    cursor = connection.cursor ()
    cursor.execute ( mySql_insert_query )
    connection.commit ()
    print ( cursor.rowcount, "Record inserted successfully into Guest table" )
    cursor.close ()


p = marque ()