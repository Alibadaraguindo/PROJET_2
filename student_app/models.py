from django.db import models
from admin_app.models import Teacher
from django.contrib.auth.models import AbstractUser, Group,Permission

class Filiere(models.Model):
    id_filiere = models.AutoField(primary_key=True)
    nom_filiere = models.CharField(max_length=100)

class Student(AbstractUser):
    idStudent = models.AutoField(primary_key=True)
    codeMassar = models.CharField(max_length=100, unique=True)
    dateNaissance = models.DateField(null =True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="images/",blank=True,null=True)
    groups = models.ManyToManyField('auth.Group', related_name='students')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='student_users')
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Module(models.Model):
    id_module = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=150)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)    

class ModuleAssociate(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    date_assoc = models.DateField(auto_now_add=True)

class Classroom(models.Model):
    id_salle = models.CharField(primary_key=True,max_length = 100)
    capacited = models.IntegerField(default=35)
    

class ClassSession(models.Model):
    id_class_session = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom,blank=True,null=True,on_delete = models.PROTECT)
    heureDebut = models.TimeField(blank = True,null = True)
    heureFin = models.TimeField(blank = True,null = True)
    jour = models.CharField(max_length = 50)
    #timetable = models.CharField(max_length=150,blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

class Marking(models.Model):
    id_marking = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    date_marked = models.DateField(auto_now_add=True)
    code_massar = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)