from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from student_management_app.EmailBackEnd import EmailBackEnd

def showDemoPage(request):
    return render(request, "demo.html")

def ShowLoginPage(request):
    return render(request, "login_page.html")

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Méthode Non Autorisée</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
    if user is not None:
        login(request, user)
        if user.user_type == "1":
            return HttpResponseRedirect('/admin_home')
        elif user.user_type== "2":
            return HttpResponseRedirect('/staff_home')
        else:
            return HttpResponseRedirect('/student_home')
    else:
        messages.error(request, "Login ou Mot de passe incorrect")
        return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user is not None:
        return HttpResponse("User : " + request.user.email + " usertype : " + str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")