
from django.contrib import admin
from django.urls import path
from admin_app.views import *
from student_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"), 
    path('logout_user/',logout_user,name='logout_user'),
    path('login/',login_view,name='login'),
    path('administration/Gérer_Enseignant',administration,name="Gérer_Enseignant"),
    path('administration/Gérer_Etudiant',Gérer_Etudiant,name="Gérer_Etudiant"),
    path('administration/Gérer_Modele',Gérer_Modele,name="Gérer_Modele"),
    path('administration/AjouterEnseignant',AjouterEnseignant,name="AjouterEnseignant"),
    path('administration/AjouterEtudiant',AjouterEtudiant,name="ajouterEtudiant"),
    path('seanceDeCours/',seanceDeCours,name='seanceDeCours'),
    path('enseignant/' , enseignant , name='enseignant'),
    path('ListeCours/' , listeCours , name='listeCours'),
    path('AjouterCours/' , ajouterCours , name='ajouterCours'),
    path('ModifierCours/' , modifierCours , name='modifierCours'),
    path('supprimerCour/' , supprimerCour , name='supprimerCour'),
    path('ListeEtudiants/' , ListeEtudiants , name='ListeEtudiants'),
     path('imprimer/' , imprimer , name='imprimer'),
]
