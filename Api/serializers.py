
from rest_framework import serializers
from .models import Client,CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'date_of_birth', 'address', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  # Rendre le mot de passe facultatif
        }

    def create(self, validated_data):
        # Vérifiez si l'email existe déjà
        if CustomUser.objects.filter(email=validated_data.get('email')).exists():
            raise ValidationError("Cet email est déjà utilisé.")

        # Définir le mot de passe par défaut
        default_password = '00000'
        user = CustomUser(**validated_data)
        user.set_password(default_password)  # Hash le mot de passe par défaut
        user.save()
        
        # Envoyer l'e-mail avec le mot de passe par défaut
        subject = 'Votre mot de passe par défaut'
        message = f'Bonjour {user.username},\nVotre mot de passe est : {default_password}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return user
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        # Vérifiez si l'email existe déjà
        if Client.objects.filter(email=validated_data.get('email')).exists():
            raise ValidationError("Cet email est déjà utilisé.")

        # Créez le client
        client = Client(**validated_data)
        client.save()
        return client

    def update(self, instance, validated_data):
        # Vérifiez si l'email existe déjà pour un autre client
        email = validated_data.get('email', instance.email)  # Utilisez l'email existant par défaut
        if email != instance.email and Client.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")

        # Mettez à jour les champs du client
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance