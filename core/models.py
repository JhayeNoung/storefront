from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser): # extending base User Class
    email = models.EmailField(unique=True)