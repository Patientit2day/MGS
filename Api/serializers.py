
from rest_framework import serializers
from .models import Client,CustomUser
from django.core.mail import send_mail
from django.conf import settings

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'date_of_birth', 'address', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  # Rendre le mot de passe facultatif
        }

    def create(self, validated_data):
        # Définir le mot de passe par défaut
        default_password = '00000'
        user = CustomUser(**validated_data)
        user.set_password(default_password)  # Hash le mot de passe par défaut
        user.save()
        
        # Envoyer l'e-mail avec le mot de passe par défaut
        subject = 'Votre mot de passe par défaut'
        message = f' Bonjour{CustomUser.username}Votre mot de passe est : {default_password}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return user