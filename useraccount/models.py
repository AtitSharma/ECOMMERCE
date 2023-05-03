from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    contact=models.CharField(max_length=100)
    address=models.CharField(max_length=100)

    class Meta:
        verbose_name="User"
        verbose_name_plural="Users"


    
    

    
