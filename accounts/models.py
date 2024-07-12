from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True, default="profile1.png")
    def __str__(self):
        if self.name:
            return self.name
        else:
            return f'customer with id: {self.id}'
    
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'), ('Outdoor', 'Outdoor')
    )
    tag = models.ManyToManyField(Tag)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

    
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),('Out for delivery','Out for delivery'),('Delivered','Delivered')
    )
    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return f'order of {self.product.name} by {self.customer.name}'
    