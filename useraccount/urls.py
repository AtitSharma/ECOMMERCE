
from django.urls import path
from useraccount.views import register,Login,user_logout
app_name="user"
urlpatterns = [
    path("register/",register,name="register"),
    path("login/",Login.as_view(),name="login"),
    path("logout/",user_logout,name="logout")

    
]