# Api/views.py

from rest_framework import viewsets
from .models import Client
from .serializers import ClientSerializer
# Api/views.py

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Client,CustomUser
from rest_framework.permissions import AllowAny
from .serializers import ClientSerializer,CustomUserSerializer
from  django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification

    def update_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Mot de passe mis à jour avec succès.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Nouveau mot de passe requis.'}, status=status.HTTP_400_BAD_REQUEST)
class ClientFilter(filters.FilterSet):
    nom = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['nom']

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClientFilter
   
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()

        # Envoyer un e-mail après la création
        send_mail(
            'Bienvenue chez nous !',
            f'Bonjour {client.nom},\n\nMerci de vous être inscrit en tant que client !',
            settings.EMAIL_HOST_USER,
            [client.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)