#Herramienta de BD, contiene tipos de datos
from django.db import models

#Modelo de Usuarios: contraseña, email, nombre
from django.contrib.auth.models import User

#Creación de una tabla llamada tasks en la base de datos llamada Tasks
class Task(models.Model):
    title= models.CharField(max_length=200) #Título
    description= models.TextField(blank=True) #Descripción(Opcional)

    #Estado, lista
    status_choices= [
    ('to do', 'To Do'),
    ('doing', 'Doing'),
    ('done', 'Done'),
    ]
    status = models.CharField(
         max_length=10,
         choices=status_choices,
         default='to do')

    #Prioridad, Lista
    priority_choices = [
        (1, '1 - Very Low'),
        (2, '2 - Low'),
        (3, '3 - Medium'),
        (4, '4 - High'),
        (5, '5 - Critical'),
    ]
    priority = models.IntegerField(
        choices=priority_choices,
        default=1
        )

    #Relación entre tarea y usuario. Borrar datos si se borra usuario.
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    #Tiempos de creación, actualización y vencimiento (opcional)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    due_date= models.DateTimeField(null=True, blank=True)

    #Vista de títulos de cada tarea
    def __str__(self):
        return self.title
    
    # para que se vea bonito, quitamos la "s" extra que se veía en el administrador de tareas
    class Meta:
            verbose_name = "Task"
            verbose_name_plural = "Tasks"