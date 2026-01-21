#Administración
from django.contrib import admin
#Importar models.py
from .models import Task

#Visual del administrador
class TaskAdmin(admin.ModelAdmin):
    list_display= ('title', 'priority', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Task, TaskAdmin)