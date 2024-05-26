from django.db import models
from django.contrib.auth.models import AbstractUser, Group,Permission

# Create your models .here.
class Teacher(AbstractUser):
    idTeacher = models.AutoField(primary_key=True)
    role = models.CharField(default="teacher", max_length=150)
    groups = models.ManyToManyField('auth.Group', related_name='teachers')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='teacher_users')
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

