
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

class Utilisateur(AbstractUser):
    user_type_data = ((1, "Admins"), (2, "Staff"), (3, "student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Admin(models.Model):
    CleAdmin = models.AutoField(primary_key=True)
    admin_id = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    DateCreation = models.DateTimeField(auto_now_add=True)
    DateModification = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Etudiants(models.Model):
    id = models.AutoField(primary_key=True)
    CodeApogee=models.TextField(max_length=255)
    Adresse = models.TextField(max_length=255)
    admin_id = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    Genre = models.CharField(max_length=255)
    profile = models.ImageField()
    Date_naissance = models.DateField()
    DateCreation = models.DateTimeField(auto_now_add=True)
    DateModification = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
class Enseignant(models.Model):
    CodeEnseignant = models.AutoField(primary_key=True)
    admin_id = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    Adresse = models.TextField(max_length=255)
    Genre = models.CharField(max_length=255)
    DateCreation = models.DateTimeField(auto_now_add=True)
    DateModification = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
class Module(models.Model):
        Module_id = models.AutoField(primary_key=True)
        staff_id = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
        NomModule = models.CharField(max_length=255)
        DateCreation = models.DateTimeField(auto_now_add=True)
        DateModification = models.DateTimeField(auto_now_add=True)
        objects = models.Manager()


class Presence(models.Model):
    id = models.AutoField ( primary_key=True )
    Etudiant_id=models.TextField(max_length=255)
    Nom = models.CharField ( max_length=255 )
    Enseignant_id=models.TextField(max_length=255)
    Prenom = models.CharField ( max_length=255 )
    Photo = models.ImageField ()
    Temps = models.TimeField ( auto_now_add=True )
    Date = models.DateField ( auto_now_add=True )
    Module_num=models.TextField(max_length=255)
    objects = models.Manager ()

class liste_filtrer(models.Model):
    objects = models.Manager()
    CodeE=models.TextField(max_length=255)
    Nom=models.CharField(max_length=255)
    Prenom=models.CharField(max_length=255)
    Photo=models.ImageField()
    Module = models.TextField ( max_length=255 )
    objects = models.Manager ()


class ListePresence(models.Model):
    id = models.AutoField(primary_key=True)
    Code_Etudiant=models.TextField(max_length=255)
    Nom = models.CharField(max_length=255)
    id_ens = models.TextField(max_length=255)
    Prenom=models.CharField(max_length=255)
    Photo = models.ImageField()
    Temps= models.TimeField(auto_now_add=True)
    Date = models.DateField(auto_now_add=True)
    Modulen= models.TextField ( max_length=255 )
    objects = models.Manager()

class ArchiverListePresence(models.Model):
    id = models.AutoField(primary_key=True)
    Etudiants_id = models.ForeignKey(Etudiants, on_delete=models.CASCADE)
    DateArchive = models.CharField(max_length=255)
    StatusArchive = models.BooleanField(default=False)
    cree_a = models.DateTimeField(auto_now_add=True)
    mise_a_jour_a = models.DateTimeField(auto_now_add=True)
    objects = models.Manager

@receiver(post_save, sender=Utilisateur)
# Ajouter des données a etudiants , admin , Enseignat
    # sender insert data,created :True/false,
def creation_profil_utilisateur(sender, instance, created, **Kwargs):
     if created:
         if instance.user_type == 1:
          Admin.objects.create(admin_id=instance)
         if instance.user_type == 2:
          Enseignant.objects.create(admin_id=instance, Genre=" ", Adresse=" ")
         if instance.user_type == 3:
          Etudiants.objects.create(admin_id=instance, CodeApogee=" ", Genre=" ", Adresse=" ", Date_naissance="2020-01-01")


@receiver(post_save, sender=Utilisateur)
def enregistre_profil_utilisateur(sender, instance, created, **Kwargs):
         if instance.user_type == 1:
          instance.admin.save()
         if instance.user_type == 2:
             instance.enseignant.save()
         if instance.user_type == 3:
             instance.etudiants.save()



