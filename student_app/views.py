from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required
from student_app.models import (
    Student,Classroom,Module,ClassSession,ModuleAssociate,Filiere,Marking)

def listModule(request):
    modules = []
    Etudiantid = request.user.id
    
    # Récupérer l'étudiant en utilisant get_object_or_404 pour gérer les cas où l'étudiant n'existe pas
    student = get_object_or_404(Student, user_ptr_id=Etudiantid)
    
    # Accéder à la filière de l'étudiant
    filiere = student.filiere
    print(filiere)
    
    # Récupérer les modules associés à la filière
    modules = Module.objects.filter(filiere=filiere)
    
    return render(request, 'studentDash/liste_des_modules.html', {'modules': modules})
    
    
   

    
    

def emploi_view(request,idStudent):
    
    if request.method == "POST" : 
        pass


