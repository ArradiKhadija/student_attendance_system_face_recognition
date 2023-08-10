import mysql.connector

def choix(debut, fin, date) :
    connection = mysql.connector.connect ( host='localhost',
                                           database='student_management_system',
                                           user='student_management_system',
                                           password='student_management_password' )
    requete = """insert into student_management_app_liste_filtrer(CodeE,Nom,Prenom,Photo) SELECT Code_Etudiant,Nom,Prenom,Photo from student_management_app_listepresence 
             where Temps between %s and %s and Date=%s"""
    cursor = connection.cursor ()
    cursor.execute ( requete, (str ( debut ), str ( fin ), str ( date )) )
    presence = cursor.fetchall ()
    connection.commit ()
    print ( cursor.rowcount, "insertion avec succés" )
    return presence
    cursor.close ()

debut ='9:07'
fin = '15:15'
date= '2022-05-24'
presence = choix ( debut, fin, date )
pr = liste_filtrer.objects.all ()
