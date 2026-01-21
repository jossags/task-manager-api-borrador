#Importando Serializers
from rest_framework import serializers
#Importando tablita de usuarios :)
from django.contrib.auth.models import User

#Configuración
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        # La contraseña solo se puede escribir, nunca leer por seguridad 
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        # Requisito: Validar que el email sea único 
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # Crea el usuario usando create_user para que la contraseña se guarde encriptada 
        user = User.objects.create_user(**validated_data)
        return user