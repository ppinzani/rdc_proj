#Core Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#My Apps Imports
from .models import Usuario


# Register your models here.
admin.site.register(Usuario, UserAdmin)
