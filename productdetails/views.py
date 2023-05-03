from django.shortcuts import render,redirect
from productdetails.models import Category,Product,Cart
from django.contrib.auth.decorators import login_required




# Create your views here.



def home(request):
    categories=Category.objects.all()
    context={
        "categories":categories
    }

    return render(request,"home.html",context)



def product(request,pk):
    products=Product.objects.filter(category__id=pk,status="in_stock")
    context={
        "products":products
    }
    return render(request,"product.html",context)


def product_details(request,pk):
    products=Product.objects.filter(pk=pk)
    context={
        'products':products
    }
    print(products)

    return render(request,"product_details.html",context)

@login_required
def add_to_cart(request,pk,quantity=1):
    username=request.user.username
    product=Product.objects.get(pk=pk)
    price=Product.objects.get(pk=pk).price
    total_price=quantity*price
    address=request.user.address
    if Cart.objects.filter(username=username,product__name=product).exists():
        cart_item=Cart.objects.get(username=username,product__name=product)
        cart_item.quantity +=quantity
        cart_item.total_price += total_price
        cart_item.save()
        return redirect('product:home')
    else:
         Cart.objects.create(username=username,product=product,
                            quantity=quantity,total_price=total_price,
                            address=address)
    return redirect('product:home')


@login_required
def my_cart(request,username):
    carts=Cart.objects.filter(username=username)
    context={
        "carts":carts
    }
    return render (request,"my_cart.html",context)


 
    
    






