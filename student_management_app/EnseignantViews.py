import io

from django.shortcuts import render
import cv2
from io import BytesIO
import base64
import mysql.connector
from student_management_app.models import Etudiants, Utilisateur, liste_filtrer,ListePresence,Module
import numpy as np
import matplotlib.pyplot as plt
def staff_home(request):
    return render(request, "Modele_enseignant/enseignant_modele.html")
def consulter_liste_etudiant(request):
    Etud = Etudiants.objects.all()
    return render(request, "Modele_enseignant/consulter_liste_etudiant.html", {"Etud": Etud})
def consulter_liste_presence(request):
      module = Module.objects.all ()
      def sup():
        connection = mysql.connector.connect(host='localhost',
                                               database='student_management_system',
                                               user='student_management_system',
                                               password='student_management_password')
        requete = """delete from student_management_app_liste_filtrer"""
        cursor = connection.cursor()
        cursor.execute(requete)
        sp=cursor.fetchall()
        connection.commit()
        return sp
        cursor.close()
      sp=sup()
      def choix(debut, fin, date, staff_id,mod):
        connection = mysql.connector.connect(host='localhost',
                                               database='student_management_system',
                                               user='student_management_system',
                                               password='student_management_password')
        requete = f"""insert into student_management_app_liste_filtrer(CodeE,Nom,Prenom,Photo,Module) SELECT Code_Etudiant,Nom,Prenom,Photo,Modulen from student_management_app_listepresence
                   where Temps between %s and %s and Date=%s and id_ens=%s and Modulen=%s """
        cursor = connection.cursor()
        cursor.execute(requete, (str(debut), str(fin), str(date), str(staff_id),str(mod)))
        presence=cursor.fetchall()

        connection.commit()
        print ( cursor.rowcount, "insertion avec succés" )
        return presence
        cursor.close()

      staff_id = request.POST.get("ens")
      debut = request.POST.get("start")
      fin = request.POST.get ( "end" )
      date = request.POST.get ( "date" )
      md=request.POST.get ( "mod" )
      # sp = sup ()
      presence = choix ( debut, fin, date, staff_id,md)
      pr=liste_filtrer.objects.all()

      return render(request,'Modele_enseignant/conslter_liste_presence.html',{'pr':pr,'module':module})


# noinspection PyUnresolvedReferences,PyUnusedLocal
def marquer_presence(request):
     module = Module.objects.all()
     if request.method == "POST":
        staff_id = request.POST.get("staff")
        Module_id = request.POST.get ( "mod" )
        staff = Utilisateur.objects.get ( id=staff_id )
        staff_id=staff
        recognizer = cv2.face.LBPHFaceRecognizer_create ()
        recognizer.read (
            'C:/Users/azlgh/Desktop/student_management_system/student_management_app/trainer/trainer.yml' )
        cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier ( cascadePath )
        font = cv2.FONT_HERSHEY_SIMPLEX
        id = 0

        def select(id) :
            connection = mysql.connector.connect ( host="localhost",
                                                   user="student_management_system",
                                                   password="student_management_password",
                                                   database="student_management_system" )

            requete = """SELECT student_management_app_etudiants.CodeApogee,student_management_app_utilisateur.first_name,student_management_app_utilisateur.last_name,
                 student_management_app_etudiants.profile FROM student_management_app_utilisateur
                 INNER JOIN student_management_app_etudiants ON student_management_app_utilisateur.id = student_management_app_etudiants.admin_id_id
                 where student_management_app_utilisateur.id=""" + str(id)
            cursor = connection.cursor ()
            cursor.execute ( requete )
            for row in cursor :
                profile = row
                cursor.close ()
                return profile
        def select_ens(staff_id):
            connection = mysql.connector.connect ( host="localhost",
                                                   user="student_management_system",
                                                   password="student_management_password",
                                                   database="student_management_system" )

            req = f"""SELECT username from student_management_app_utilisateur
                 where username='{staff_id}'"""
            cursor = connection.cursor()
            cursor.execute(req)
            for row in cursor:
                ens= row
                cursor.close()
                return ens

        cam = cv2.VideoCapture(0)
        cam.set(3, 640)
        cam.set(4, 480)
        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get ( 3 )
        minH = 0.1 * cam.get ( 4 )

        while True :
            ret, img = cam.read ()
            img = cv2.flip ( img, 1 )  # Flip vertically

            gray = cv2.cvtColor ( img, cv2.COLOR_BGR2GRAY )
            faces = faceCascade.detectMultiScale ( gray, scaleFactor=1.3, minNeighbors=5,
                                                   minSize=(int ( minW ), int ( minH )) )
            for (x, y, w, h) in faces :
                cv2.rectangle ( img, (x, y), (x + w, y + h), (0, 255, 0), 2 )
                id, confidence = recognizer.predict ( gray[y :y + h, x :x + w] )
                profile = select(id)
                ens =select_ens(staff_id)
                # Check if confidence is less them 100 ==> "0" is perfect match
                if confidence < 60:
                    id = profile[2]
                    confidence = " {0}%".format ( round ( 100 - confidence ) )
                    cv2.rectangle ( img, (x, y), (x + w, y + h), (0, 255, 0), 2 )
                    cv2.putText ( img, str ( id ), (x + 5, y - 5), font, 1, (255, 255, 255), 2 )
                    cv2.putText ( img, str ( confidence ), (x + 5, y + h - 5), font, 1, (255, 255, 255), 1 )
                    try:
                        def suprimé():
                            connection = mysql.connector.connect ( host='localhost',
                                                                   database='student_management_system',
                                                                   user='student_management_system',
                                                                   password='student_management_password' )
                            requete = """delete from student_management_app_presence"""
                            cursor = connection.cursor ()
                            cursor.execute ( requete )
                            sp = cursor.fetchall ()
                            connection.commit ()
                            return sp
                            cursor.close ()

                        connection = mysql.connector.connect ( host='localhost',
                                                               database='student_management_system',
                                                               user='student_management_system',
                                                               password='student_management_password' )
                        req=f"""INSERT INTO student_management_app_presence(Etudiant_id,Nom,Prenom,Photo,Enseignant_id,Module_num) 
                        VALUES(%s,%s,%s,%s,%s,%s)"""

                        cursor = connection.cursor ()
                        cursor.execute ( req,(str ( profile[0] ), str ( profile[1] ), str ( profile[2] ), str ( profile[3]),str ( ens[0] ),str(Module_id)) )
                        connection.commit ()
                        print ( cursor.rowcount, "Record inserted successfully into Guest table" )
                        cursor.close ()
                    except mysql.connector.Error as error :
                        print ( "Failed to insert record into Laptop table {}".format ( error ) )

                    finally :
                        if connection.is_connected () :
                            connection.close ()
                            print ( "MySQL connection is closed" )

                else :
                    id = "unknown"
                    confidence = "  {0}%".format ( round ( 100 - confidence ) )
                    cv2.rectangle ( img, (x, y), (x + w, y + h), (0, 25, 255), 2 )
                    cv2.putText ( img, str ( id ), (x + 5, y - 5), font, 1, (255, 255, 255), 2 )
                    cv2.putText ( img, str ( confidence ), (x + 5, y + h - 5), font, 1, (255, 255, 255), 1 )
            cv2.imshow ( 'camera', img )

            k = cv2.waitKey ( 10 ) & 0xff
            # Press 'ESC' for exiting video
            if k == 27 :
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release ()
        cv2.destroyAllWindows()

        def table():
            connection = mysql.connector.connect ( host='localhost',
                                                   database='student_management_system',
                                                   user='student_management_system',
                                                   password='student_management_password')
            requete = """INSERT INTO student_management_app_ListePresence(Code_Etudiant,Nom,Prenom,Photo,id_ens,Modulen)
                SELECT Etudiant_id,Nom,Prenom,Photo,Enseignant_id,Module_num from student_management_app_presence group by Etudiant_id """
            cursor = connection.cursor()
            cursor.execute(requete)
            connection.commit()
            print(cursor.rowcount, "insertion avec succés")
            cursor.close()
        p=table()
        delete = suprimé ()
     return render(request, "Modele_enseignant/marquer_presence.html", {"module": module})
def Consulter_statistique_ens(request):
    module = Module.objects.all ()
    if request.method == "POST" :
        debut = request.POST.get ( "start" )
        fin = request.POST.get ( "end" )
        date = request.POST.get ( "date" )
        modu = request.POST.get ( "mod" )
        Heure = np.array ( ['08:30', '10:00', '10:15', '12:45', '13:00', '14:15', '14:30', '16:00', '17:30', '18:00'] )

        def select_nbr_presence(heure, hr, mod, date) :
            connection = mysql.connector.connect ( host="localhost",
                                                   user="student_management_system",
                                                   password="student_management_password",
                                                   database="student_management_system" )

            requete = f"""select nvl(count(Nom),0) from student_management_app_listepresence where Temps between %s and %s  and Modulen=%s and Date=%s"""

            cursor = connection.cursor ()
            cursor.execute ( requete, (str ( heure ), str ( hr ), str ( mod ), str ( date )) )
            for row in cursor :
                nombre_presence = row
                cursor.close ()
                return nombre_presence

        # Fecthing Data From mysql to my python progame
        Students = []

        def select(debu, fi) :
            H = []
            for i in range ( len ( Heure ) ) :
                if Heure[i] >= debu and Heure[i] <= fi :
                    H.append ( Heure[i] )
            return H

        k = select ( debut, fin )
        for j in range ( len ( k ) ) :
            if j == len ( k ) - 1 :
                Students.append ( (0,) )
            else :
                Students.append ( select_nbr_presence ( k[j], k[j + 1], modu, date ) )

        print ( "Hours = ", k )
        print ( " Students = ", Students )

        def get_graph() :
            buffer = BytesIO ()
            plt.savefig ( buffer, format='png' )
            buffer.seek ( 0 )
            graph = base64.b64encode ( buffer.getvalue () ).decode ( 'utf-8' )
            buffer.close ()
            return graph

        # Visulizing Data using Matplotlib
        def get_plot(Heure, Students) :
            plt.switch_backend ( 'AGG' )
            plt.figure ( figsize=(10, 5) )
            plt.title ( "Graphe sur la présence des Etudiants" )
            plt.plot ( Heure, Students )
            plt.xticks ( rotation=45 )
            plt.xlabel ( "Temps" )
            plt.ylabel ( "Nombre des etudiants" )
            plt.tight_layout ()
            graph = get_graph ()
            return graph

        chart = get_plot ( k, Students )
        return render ( request, 'Modele_enseignant/main.html',{'chart':chart})
    return render ( request, 'Modele_enseignant/consulter_statistique.html' ,{"module": module})
