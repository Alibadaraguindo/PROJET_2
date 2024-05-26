from django.db import models
from django.contrib.auth.models import AbstractUser, Group,Permission

# Create your models .here.
from django.contrib.auth.models import AbstractUser
from django.db import models

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


