from django.db import models
from django.contrib.auth.models import AbstractUser, Group,Permission

# Create your models .here.
from django.contrib.auth.models import AbstractUser
from django.db import models
""" 
teacher = Teacher.objects.create(
    username='teacher1',
    first_name='John',
    last_name='Doe',
    email='teacher1@example.com',
    password='password123',  # Assurez-vous de hacher le mot de passe correctement avant de l'insérer
    role='teacher',  # Assurez-vous que le rôle correspond à l'un des choix définis dans votre modèle
    idTeacher=3,  # Remplacez par la valeur souhaitée pour l'identifiant du professeur
    # Ajoutez d'autres champs et leurs valeurs ici
)
"""


class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
        ('student', 'Student'),
        # Ajoutez d'autres rôles au besoin
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Teacher(User):
    idTeacher = models.AutoField(primary_key=True)
    teacher_groups = models.ManyToManyField('auth.Group', related_name='teachers')
    teacher_permissions = models.ManyToManyField('auth.Permission', related_name='teacher_users')
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


