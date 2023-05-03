
from django.urls import path
from productdetails.views import home,product,product_details,add_to_cart,my_cart
app_name="product"
urlpatterns = [ 
    path("",home,name="home"),
    path("product/<int:pk>/",product,name="products"),
    path("product-detail/<int:pk>/",product_details,name="product_detail"),
    path("add_to_cart/<int:pk>/",add_to_cart,name="add_to_cart"),
    path("my-cart/<str:username>/",my_cart,name="my_cart")

]
