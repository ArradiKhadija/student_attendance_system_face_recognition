
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from student_management_app.models import Utilisateur, Etudiants, Enseignant, Module
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import base64
from datetime import timedelta
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
def admin_home(request):
    return render(request, "Modele_admin/home_content.html")


def ajouter_enseignant(request):
    return render(request, "Modele_admin/ajouter_enseignant.html")


# noinspection PyBroadException
def sauvegarder_enseignant(request):
    if request.method != "POST":
        return HttpResponse("Modele n'est pas autorisée")
    else:
        first_name = request.POST.get("Nom")
        last_name = request.POST.get("Prenom")
        password = request.POST.get("password")
        Genre = request.POST.get("Genre")
        email = request.POST.get("email")
        Adresse = request.POST.get("Adresse")
        username = request.POST.get("username")
        try:
            user = Utilisateur.objects.create_user(password=password, username=username, first_name=first_name, last_name=last_name, email=email, user_type=2)
            user.enseignant.Adresse = Adresse
            user.enseignant.Genre = Genre
            user.save()
            messages.success(request, "Ajout avec succés")
            return HttpResponseRedirect("/ajouter_enseignant")
        except:
            messages.error(request, "Ajout Echoué")
            return HttpResponseRedirect("/ajouter_enseignant")
def gerer_enseignant(request):
    enseignant = Enseignant.objects.all()
    return render(request, "Modele_admin/gerer_enseignant.html", {"enseignant": enseignant})
def modifier_enseignant(request, staff_id):
    staff = Enseignant.objects.get(admin_id=staff_id)
    return render(request, "Modele_admin/modifier_enseignant.html", {"staff": staff, "id": staff_id})


# noinspection PyBroadException
def sauvegarder_modifier_enseignant(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        Ens_id = request.POST.get("staff_id")
        first_name = request.POST.get("Nom")
        last_name = request.POST.get("Prenom")
        email = request.POST.get("email")
        username = request.POST.get("username")
        Adresse = request.POST.get("Adresse")
        Genre = request.POST.get("Genre")

        try:
            user = Utilisateur.objects.get(id=Ens_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Enseignant.objects.get(admin_id=Ens_id)
            staff_model.Adresse= Adresse
            staff_model.Genre = Genre
            staff_model.save()
            messages.success(request, "Modification succés")
            return HttpResponseRedirect('/modifier_enseignant/'+Ens_id)
        except:
            messages.error(request, "Modification echoué")
            return HttpResponseRedirect('/modifier_enseignant/'+Ens_id)

def supprimer_enseignant(request, staff_id):
    staff = Enseignant.objects.get(admin_id=staff_id)
    staff.delete()
    return HttpResponseRedirect("/gerer_enseignant")
def ajouter_etudiant(request):
    return render(request, "Modele_admin/ajouter_etudiant.html")


# noinspection PyBroadException
def sauvegarder_etudiant(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("Nom")
        last_name = request.POST.get("Prenom")
        password = request.POST.get("password")
        Genre = request.POST.get("Genre")
        email = request.POST.get("email")
        Adresse = request.POST.get("Adresse")
        username = request.POST.get("username")
        Date_naissance = request.POST.get("Date_naissance")
        CodeApogee=request.POST.get("CodeApogee")
        profile = request.FILES['profile']
        fs = FileSystemStorage()
        filename = fs.save(profile.name, profile)
        profile_url = fs.url(filename)
        # noinspection PyBroadException
        try:
         etud = Utilisateur.objects.create_user(password=password, username=username, first_name=first_name, last_name=last_name, email=email, user_type=3)
         etud.etudiants.Adresse = Adresse
         etud.etudiants.Genre = Genre
         etud.etudiants.CodeApogee=CodeApogee
         etud.etudiants.Date_naissance =Date_naissance
         etud.etudiants.profile=profile_url
         etud.save()
         messages.success(request, "Ajout avec Succés")
         return HttpResponseRedirect("/ajouter_etudiant")
        except:
         messages.error(request, "Ajout Echoué")
         return HttpResponseRedirect("/ajouter_etudiant")


def gerer_etudiant(request):
    etudiant = Etudiants.objects.all()
    return render(request, "Modele_admin/gerer_etudiant.html", {"etudiant": etudiant})
def modifier_etudiant(request, Etd_id):
    Etd=Etudiants.objects.get(admin_id_id=Etd_id)
    return render(request, "Modele_admin/modifier_etudiant.html", {"Etd": Etd})


# noinspection PyBroadException
def sauvegarder_modifier_etudiant(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        std_id = request.POST.get ( "Etd_id" )
        first_name = request.POST.get ( "Nom" )
        last_name = request.POST.get ( "Prenom" )
        password = request.POST.get ( "password" )
        Genre = request.POST.get ( "Genre" )
        email = request.POST.get ( "email" )
        Adresse = request.POST.get ( "Adresse" )
        username = request.POST.get ( "username" )
        Date_naissance = request.POST.get ( "Date_naissance" )
        CodeApogee = request.POST.get ( "CodeApogee" )
        if request.FILES.get ( 'profile', False ) :
            profile = request.FILES['profile']
            fs = FileSystemStorage ()
            filename = fs.save ( profile.name, profile )
            profile_url = fs.url ( filename )
        else :
            profile_url = None

        try:
            staff = Utilisateur.objects.get ( id=std_id )
            staff.first_name = first_name
            staff.password = password
            staff.last_name = last_name
            staff.username = username
            staff.email = email
            staff.save ()

            std = Etudiants.objects.get ( admin_id_id=std_id )
            std.Adresse = Adresse
            std.Date_naissance = Date_naissance
            std.Genre = Genre
            std.CodeApogee = CodeApogee
            std.profile = profile_url
            std.save ()
            messages.success ( request, "Modification avec succés" )
            return HttpResponseRedirect ( "/modifier_etudiant/" + std_id )
        except:
            messages.error(request, "Modification échoué")
            return HttpResponseRedirect("/modifier_etudiant/"+std_id)
def supprimer_etudiant(request, Etd_id):
    Etd=Etudiants.objects.get(admin_id_id=Etd_id)
    Etd.delete()
    return HttpResponseRedirect("/gerer_etudiant")
def ajouter_module(request):
    enseignant = Utilisateur.objects.filter(user_type=2)
    return render(request, "Modele_admin/ajouter_module.html", {"enseignant": enseignant})


# noinspection PyBroadException
def sauvegarder_module(request):
    if request.method != "POST":
        return HttpResponse("Method Non autorisée")
    else:
        NomModule = request.POST.get("NomModule")
        staff_id = request.POST.get("staff")
        staff = Utilisateur.objects.get(id=staff_id)
        try:
            modules = Module(NomModule=NomModule, staff_id=staff)
            modules.save()
            messages.success(request, "Ajout avec succés")
            return HttpResponseRedirect("/ajouter_module")
        except:
            messages.error(request, "Ajout Echoué")
            return HttpResponseRedirect("/ajouter_module")


def gerer_module(request):
    module = Module.objects.all()
    return render(request, "Modele_admin/gerer_module.html", {"module": module})
def modifier_module(request, modules_id):
    modules = Module.objects.get(Module_id=modules_id)
    enseignant = Utilisateur.objects.filter(user_type=2)
    return render(request, "Modele_admin/modifier_module.html", {"modules": modules, "enseignant": enseignant})


# noinspection PyBroadException
def sauvegarder_modifier_module(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        modules_id=request.POST.get("Module_id")
        NomModule=request.POST.get("NomModule")
        staff_id=request.POST.get("staff")
        try:
            modules=Module.objects.get(Module_id=modules_id)
            modules.NomModule=NomModule
            staff = Utilisateur.objects.get(id=staff_id)
            modules.staff_id = staff
            modules.save()
            messages.success(request, "Modification avec succés")
            return HttpResponseRedirect("/modifier_module/"+modules_id)
        except:
            messages.error(request, "Modification échoué")
            return HttpResponseRedirect("/modifier_module/"+modules_id)
def supprimer_module(request, modules_id):
    modules = Module.objects.get(Module_id=modules_id)
    modules.delete()
    return HttpResponseRedirect("/gerer_module")
def Consulter_statistique(request):
    module = Module.objects.all ()
    enseignant = Utilisateur.objects.filter(user_type="2")
    if request.method == "POST" :
        staff_id = request.POST.get ( "ens" )
        staff = Utilisateur.objects.get ( id=staff_id )
        staff_id = staff
        debut = request.POST.get ( "start" )
        fin = request.POST.get ( "end" )
        date = request.POST.get ( "date" )
        modu = request.POST.get ( "mod" )
        Heure = np.array(['08:30', '10:00','10:15', '12:45','13:00','14:15','14:30','16:00','17:30','23:00'])

        def select_nbr_presence(heure, hr, staff_id, mod,date) :
            connection = mysql.connector.connect ( host="localhost",
                                                   user="student_management_system",
                                                   password="student_management_password",
                                                   database="student_management_system" )

            requete = f"""select nvl(count(Nom),0) from student_management_app_listepresence where Temps between %s and %s and id_ens=%s and Modulen=%s and Date=%s"""

            cursor = connection.cursor ()
            cursor.execute ( requete, (str ( heure ), str ( hr ), str ( staff_id ), str ( mod ),str(date)) )
            for row in cursor :
                nombre_presence = row
                cursor.close ()
                return nombre_presence

        # Fecthing Data From mysql to my python progame
        Students =[]

        def select(debu,fi):
            H = []
            for i in range(len ( Heure ))  :
              if Heure[i]>=debu and Heure[i]<=fi:
                H.append(Heure[i])
            return H
        k=select(debut,fin)
        for j in range(len(k)):
             if j==len(k)-1:
               Students.append ( (0,) )
             else :
                Students.append ( select_nbr_presence ( k[j],k[j+1], staff_id, modu,date ) )

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

        chart = get_plot (k, Students )
        return render ( request, 'Modele_admin/main.html', {'chart' : chart} )
    return render ( request, 'Modele_admin/con_stat.html', {"module" : module,"enseignant":enseignant} )
