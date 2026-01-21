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

#Filtro, solo acepta envíos
@api_view(['POST'])
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
    
    # Error D:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)