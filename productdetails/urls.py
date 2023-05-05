
from django.urls import path
from productdetails.views import( home,product,add_item,
                                product_details,add_to_cart,my_cart
                                ,buy_product,place_a_order,admin_pannel)
app_name="product"
urlpatterns = [ 
    path("",home,name="home"),
    path("product/<int:pk>/",product,name="products"),
    path("product-detail/<int:pk>/",product_details,name="product_detail"),
    path("add_to_cart/<int:pk>/",add_to_cart,name="add_to_cart"),
    path("my-cart/<str:username>/",my_cart,name="my_cart"),
    path("buy-product/<int:pk>/",buy_product,name="buy_product"),
    path("place_order/<int:pk>/<int:quantity>/",place_a_order,name="place_order"),
    path("admin-pannel/",admin_pannel,name="admin_pannel"),
    path("add-item/",add_item,name="add_item"),


]
