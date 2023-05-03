from django.shortcuts import render,redirect
from useraccount.forms import CustomerCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .models import User
# Create your views here.


def register(request):
    if request.method=="POST":
        form=CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product:home")
            
    else:
        form=CustomerCreationForm()
    return render(request,"register.html",{"form":form})



class Login(LoginView):
    template_name="login.html"



def user_logout(request):
    logout(request)
    return redirect("product:home")




