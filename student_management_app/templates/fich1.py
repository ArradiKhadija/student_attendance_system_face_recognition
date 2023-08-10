import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

mydb = mysql.connector.connect (  host="localhost",
                                               user="student_management_system",
                                               password="student_management_password",
                                               database="student_management_system" )

mycursor = mydb.cursor ()

# Fecthing Data From mysql to my python progame
mycursor.execute ( "select nvl(count(Nom),0),Temps from student_management_app_listepresence where Date='2022-06-21' and Temps between '17:00' and '23:00'and id_ens='Mr.Moussaid Khalid' and Modulen=1 group by Temps" )
result = mycursor.fetchall

Names = []
Marks = []

for i in mycursor :
    Names.append ( i[0] )
    Marks.append ( str(i[1]) )

print ( "Name of Students = ", Names )
print ( "Marks of Students = ", Marks )

# Visulizing Data using Matplotlib
plt.bar ( Names, Marks )

plt.xlabel ( "Name of Students" )
plt.ylabel ( "Marks of Students" )
plt.title ( "Student's Information" )
plt.show ()