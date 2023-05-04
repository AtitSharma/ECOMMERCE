from django.shortcuts import render,redirect,reverse
from productdetails.models import Category,Product,Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages





def home(request):
    categories=Category.objects.all()
    context={
        "categories":categories
    }

    return render(request,"home.html",context)



def product(request,pk):
    products=Product.objects.filter(category__id=pk,status="in_stock",available__gte=1)

    context={
        "products":products
    }
    return render(request,"product.html",context)


def product_details(request,pk):
    products=Product.objects.filter(pk=pk)
    context={
        'products':products
    }

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
        return HttpResponseRedirect(reverse("product:my_cart",args=(request.user.username,)))
    else:
         Cart.objects.create(username=username,product=product,
                            quantity=quantity,total_price=total_price,
                            address=address)
    return HttpResponseRedirect(reverse("product:my_cart",args=(request.user.username,)))


@login_required
def my_cart(request,username):
    carts=Cart.objects.filter(username=username,product__available__gt=0)
    context={
        "carts":carts,
    }
    return render (request,"my_cart.html",context)

@login_required
def buy_product(request,pk):
    quantity=request.POST.get("quantity")
    quantity=int(quantity)
    available_quantity=Cart.objects.get(pk=pk).product.available
    if quantity<1:
        messages.add_message(request,messages.ERROR,"Please choose atleaset 1 quantity")
        return redirect("product:home")
    elif quantity > available_quantity:
        messages.add_message(request,messages.ERROR,"Please choose quantity less and equal to  available")
        return redirect("product:home")
    else:

        # remaining_quantity=int(available_quantity)-int(quantity)
        # print(remaining_quantity)
        demo=Cart.objects.get(pk=pk).product
        # demo.available=remaining_quantity
        price=demo.price
        # demo.save()
        Cart.objects.filter(pk=pk).update(quantity=quantity,total_price=price*quantity)
        carts=Cart.objects.filter(pk=pk)
        print(carts)
        
    return render (request,"buy_product.html",{"carts":carts,"quantity":quantity})


@login_required
def place_a_order(request,pk,quantity):
    available_quantity=Cart.objects.get(pk=pk).product.available
    remaining_quantity=int(available_quantity)-int(quantity)
    demo=Cart.objects.get(pk=pk).product
    demo.available=remaining_quantity
    demo.save()
    messages.add_message(request,messages.INFO,"sucessfully bought we will contact you ")
    Cart.objects.filter(pk=pk).delete()
    return redirect("product:home")



 
    
    






