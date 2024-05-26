from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# from student_app.activated_camera import camera_maked,preprocess_student_images
from admin_app.models import Teacher
from datetime import date
from student_app.models import (
    Student,Classroom,Module,ClassSession,ModuleAssociate,Filiere,Marking)
from django.contrib.auth import (
    get_user_model,login,logout,authenticate
    )

# Create your views here.
def home(request):
    
    return render(request,'admin_app/accueil.html')
def administration(request):
    return render(request,'admin_app/administration/Gérer_Enseignant.html')
def Gérer_Etudiant(request):
    etudiants = Student.objects.all()
    return render(request,'admin_app/administration/Gérer_Etudiant.html' ,  {"etudiants" : etudiants})
def Gérer_Modele(request):
    return render(request,'admin_app/administration/Gérer_Modele.html')
def AjouterEnseignant(request):

    return render(request,'admin_app/administration/AjouterEnseignant.html')
def AjouterEtudiant(request):
    filieres = Filiere.objects.all()
    if request.method == 'POST':
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        massar = request.POST.get("massar")
        dateNaissance = request.POST.get("dateNaissance")
        filiere = request.POST.get("filiere")
        niveau = request.POST.get("niveau")
        email = request.POST.get("email")
        photo = request.FILES.get("photo")

        #trouvé la filiere :
        filiere = Filiere.objects.get(id_filiere = filiere)

        # Créer l'instance Student
        new_student = Student.objects.create(
            first_name=nom,
            last_name=prenom,
            codeMassar=massar,
            dateNaissance=dateNaissance,
            filiere=filiere,
            niveau=niveau,
            email=email,
            photo=photo,
            username=email,
            password=massar ,
        )
        return redirect("Gérer_Etudiant") 
    
    filieres = Filiere.objects.all() 
    return render(request,'admin_app/administration/ajouterEtudiant.html',{"filieres" : filieres})
def login_view(request):
    error=""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            
            return render(request,'enseignantDash/EnseignantDash.html')
        else:
            # Gérer le cas où l'authentification échoue
            error ='Invalid username or password'
            return render(request, 'admin_app/login.html', {'error': error })

    return render(request, 'admin_app/login.html')

@login_required
def logout_user(request):#champs à definir
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            # Gérer l'erreur de mots de passe non correspondants
            return render(request, 'admin_app/register.html', {'error': 'Les mots de passe ne correspondent pas'})

        # Créer un nouvel utilisateur
        user = Teacher.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Authentifier et connecter l'utilisateur
        user = authenticate(username=username, password=password)
        login(request, user)

        # Rediriger vers la page d'accueil
        return render(request,"enseignantDash/EnseignantDash.html")
        #return redirect('home')
        return redirect('login')

    # Si la méthode de la requête n'est pas POST, afficher le formulaire vide
    return render(request, 'admin_app/register.html')



# ************* view Enseignant ************
def enseignant(request) :
    return render(request , 'enseignantDash/EnseignantDash.html')

@login_required
def listeCours(request) :
    
    cours = Module.objects.all()
    return render(request , 'enseignantDash/ListeCours.html',{'cours' : cours})




@login_required
def ajouterCours(request):
    salles = Classroom.objects.all()
    filieres = Filiere.objects.all()
    if request.method == 'POST':
        module_name = request.POST.get('module')
        salle_id = request.POST.get('salle')
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        
        # prof connecté
        teacher = request.user 
         
        #Filiere
        id_filiere = request.POST.get('filiere')
        filiere = Filiere.objects.get(id_filiere=id_filiere)

        # Création du module
        module = Module.objects.create(module_name=module_name,filiere=filiere)
        
        # Récupération de la salle
        salle = Classroom.objects.get(id_salle=salle_id)
        
        # Création de la session de cours
        class_session = ClassSession.objects.create(classroom=salle, heureDebut=debut, heureFin=fin, module=module)
        
        # Enregistrement des objets créés
        module.save()
        class_session.save()
        
        # Attribution du module à l'enseignant
        module_associate = ModuleAssociate.objects.create(teacher=teacher, module=module)
        module_associate.save()
        
        return redirect('listeCours')
    
    return render(request, 'enseignantDash/AjouterCours.html', {'salles': salles,'filieres' : filieres})

def modifierCours(request) : 
    cours = Module.objects.all()
    if request.method == "POST":
        filiere_nom = request.POST.get('filiere_nom')
        module_name = request.POST.get('module_name')
        id_salle = request.POST.get('id_salle')
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        salles = Classroom.objects.all()
        filieres = Filiere.objects.all()
        return render(request , 'enseignantDash/modifierCours.html',{'filiere_nom' : filiere_nom, 'module_name' : module_name, 'id_salle' : id_salle, 'debut' : debut,'fin' : fin,'salles' : salles})

    return render(request , 'enseignantDash/ListeCours.html',{'cours' : cours})

def remarque(request) : 
    return render(request , 'enseignantDash/Remarque.html')

def ListeEtudiants(request) :
    return render(request , 'enseignantDash/ListeEtudiant.html')
# **********************************************

def seanceDeCours(request):
    cours = Module.objects.all()
    student_encodings = preprocess_student_images()
    teacher = request.user
    camera_maked(student_encodings,teacher)
    if request.method == 'POST':
        # Obtenez la filière sélectionnée dans le formulaire
        id_filiere = request.POST.get('filiere')
        current_date = date.today()
        
        # Assurez-vous que l'identifiant de la filière est un entier
        if id_filiere is not None:
            id_filiere = int(id_filiere)

        # Filtrer les marqueurs par la date actuelle et l'identifiant de la filière
        if id_filiere is not None:
            listeAbsences = Marking.objects.filter(date_marked=current_date, code_massar__filiere_id=id_filiere)
        else:
            listeAbsences = Marking.objects.none()  # Si aucun paramètre n'est fourni, renvoyer une liste vide
        
        # Ensuite, vous pouvez effectuer d'autres opérations ou afficher la liste des absences
        return render(request, 'enseignantDash/ListeEtudiant.html', {'listeAbsences': listeAbsences})
    
    return render(request, 'enseignantDash/ListeCours.html', {'cours': cours})

