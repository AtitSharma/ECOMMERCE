from django.shortcuts import render,redirect,reverse
from productdetails.models import Category,Product,Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from productdetails.forms import ProductAdditionForm
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from ec import settings
from celery import shared_task
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


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


@user_passes_test(lambda u : u.is_superuser)
def admin_pannel(request):
    return render(request,"admin_pannel.html")


@user_passes_test(lambda u : u.is_superuser)
def add_item(request):
    if request.method=="POST":
        form=ProductAdditionForm(request.POST)
        if form.is_valid():
            form.save()
            product_name=request.POST.get("name")
            mail_subject="New product available !!!!"
            message="Please check it out "
            send_mails_to_all(request,mail_subject,message)
            return redirect("product:admin_pannel")
    else:
        form=ProductAdditionForm()
    return render(request,"add_product.html",{"form":form})





@shared_task
def send_mails_to_all(request,mail_subject,message):   
    users=get_user_model().objects.all()
    mes=message
    for user in users:
        to_email=user.email
        message = render_to_string("show_in_all.html", {
        'title':mes,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
        })
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return HttpResponse("SENT")

            


 
    
    






