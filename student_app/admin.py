from django.contrib import admin
from student_app.models import Module,Classroom,Marking,ModuleAssociate,ClassSession,Student,Filiere
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(Module)
admin.site.register(Classroom)
admin.site.register(Marking)
admin.site.register(ModuleAssociate)
admin.site.register(ClassSession)
admin.site.register(Filiere)
admin.site.register(Student)
