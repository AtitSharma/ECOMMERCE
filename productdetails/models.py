from django.db import models


class Category(models.Model):
    name=models.CharField(max_length=100)
    details=models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.name)


class Status(models.TextChoices):
    IN_STOCK="in_stock","IN_STOCK"
    NOT_IN_STOCK="not_in_stock"",NOT_IN_STOCK"


class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to="product_image",blank=True,null=True)
    available=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    status=models.CharField(max_length=100,choices=Status.choices,default=Status.IN_STOCK)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    username=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_price=models.IntegerField()
    address=models.CharField(max_length=100)

    def __str__(self):
        return str(self.username)

















 




