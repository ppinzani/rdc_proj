#Std Lib Import
#Core Django Import
from django.contrib.auth.models import AbstractUser
from django.db import models

#Third-party import
#Import from apps


class Usuario(AbstractUser):

    def __str__(self):
        return self.get_full_name()
