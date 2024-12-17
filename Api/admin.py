from django.contrib import admin
from .models import Client
# Register your models here.

@admin.register(Client)
class Client(admin.ModelAdmin):
    list_display=('id','nom','email')
