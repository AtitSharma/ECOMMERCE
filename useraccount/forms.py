from useraccount.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm



class CustomerCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","address","contact","password1","password2"]
