"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the_include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from student_management_app import views, EnseignantViews, EtudiantViews

from student_management_app import AdminViews

urlpatterns = [
                  path ( 'demo', views.showDemoPage ),
                  path ( 'admin/', admin.site.urls ),
                  path ( '', views.ShowLoginPage, name="show_login" ),
                  path ( 'get_user_details', views.GetUserDetails ),
                  path ( 'logout_user', views.logout_user, name="logout" ),
                  path ( 'doLogin', views.doLogin, name="do_login" ),
                  path ( 'admin_home', AdminViews.admin_home ),
                  path ( 'gerer_enseignant', AdminViews.gerer_enseignant ),
                  path ( 'ajouter_enseignant', AdminViews.ajouter_enseignant ),
                  path ( 'sauvegarder_enseignant', AdminViews.sauvegarder_enseignant ),
                  path ( 'modifier_enseignant/<str:staff_id>', AdminViews.modifier_enseignant ),
                  path ( 'sauvegarder_modifier_enseignant', AdminViews.sauvegarder_modifier_enseignant ),
                  path ( 'supprimer_enseignant/<str:staff_id>', AdminViews.supprimer_enseignant ),
                  path ( 'gerer_module', AdminViews.gerer_module ),
                  path ( 'ajouter_module', AdminViews.ajouter_module ),
                  path ( 'sauvegarder_module', AdminViews.sauvegarder_module ),
                  path ( 'modifier_module/<str:modules_id>', AdminViews.modifier_module ),
                  path ( 'sauvegarder_modifier_module', AdminViews.sauvegarder_modifier_module ),
                  path ( 'supprimer_module/<str:modules_id>', AdminViews.supprimer_module ),
                  path ( 'gerer_etudiant', AdminViews.gerer_etudiant ),
                  path ( 'ajouter_etudiant', AdminViews.ajouter_etudiant ),
                  path ( 'sauvegarder_etudiant', AdminViews.sauvegarder_etudiant ),
                  path ( 'gerer_etudiant', AdminViews.gerer_etudiant ),
                  path ( 'modifier_etudiant/<str:Etd_id>', AdminViews.modifier_etudiant ),
                  path ( 'sauvegarder_modifier_etudiant', AdminViews.sauvegarder_modifier_etudiant ),
                  path ( 'supprimer_etudiant/<str:Etd_id>', AdminViews.supprimer_etudiant ),
                  path ( 'Consulter_statistique', AdminViews.Consulter_statistique ),
                  path ( 'staff_home', EnseignantViews.staff_home ),
                  path ( 'consulter_liste_etudiant', EnseignantViews.consulter_liste_etudiant ),
                  path ( 'consulter_liste_presence', EnseignantViews.consulter_liste_presence),
                  path ( 'Consulter_statistique_ens', EnseignantViews.Consulter_statistique_ens),
                  path ('marquer_presence', EnseignantViews.marquer_presence),
                  path ( 'student_home', EtudiantViews.student_home ),
                  path ('prendre_photos', EtudiantViews.prendre_photos),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
