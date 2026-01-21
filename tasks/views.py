#HTML (?)
from django.shortcuts import render

#Punto de acceso, API
from rest_framework.decorators import api_view

#Formato JSON
from rest_framework.response import Response

#Reglas de validación
from .serializers import UserSerializer  
from rest_framework import status   #Diccionario de códigos (creación, error, etc.)
from rest_framework.authtoken.models import Token   #Código secreto, llaves

#Tablita de usuarios
from django.contrib.auth.models import User

#Buscador que devuelve error si no encuentra lo que busca
from django.shortcuts import get_object_or_404

from rest_framework.decorators import permission_classes # Para proteger las rutas
from rest_framework.permissions import IsAuthenticated # Solo gente con Token
from .models import Task # modelo de tareas
from .serializers import TaskSerializer # serializer

from rest_framework.permissions import AllowAny # Para que cualquiera pueda entrar

from rest_framework.permissions import AllowAny


#SIGNUP
#Filtro, solo acepta envíos
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    
    #Validación de datos, correo
    if serializer.is_valid():
        serializer.save()
        
        #Token a usuario
        user = User.objects.get(username=request.data['username'])
        token = Token.objects.create(user=user)
        
        # Creación :D
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    
    #Error D:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Pedir token al perderla o cerrar sesión, login

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    #Buscar al usuario por su nombre
    user = get_object_or_404(User, username=request.data['username'])
    
    #ver si contraseña coincide
    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    #Obtenemos su llave (Token) o la creamos si no tiene
    token, created = Token.objects.get_or_create(user=user)
    
    # exitoOoOo, yay
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

#LOGOUT
@api_view(['POST'])
def logout(request):
    # Borramos el token del usuario que hace la petición
    request.user.auth_token.delete()
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

#TASK
# VISTA PARA LISTAR Y CREAR TAREAS
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) #¡Seguridad! Sin token no entras
def task_list_create(request):
    if request.method == 'GET':
        # Buscamos solo las tareas del usuario que está logueado
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# VISTA PARA VER, EDITAR O BORRAR UNA TAREA ESPECÍFICA
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    # Buscamos la tarea por su ID (pk) y que pertenezca al usuario
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({"message": "Tarea eliminada"}, status=status.HTTP_204_NO_CONTENT)
