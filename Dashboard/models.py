from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Food_Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Food_Item(models.Model):
    name = models.CharField(max_length=100)
    food_category = models.ForeignKey(Food_Category, on_delete=models.CASCADE)
    small_description = models.CharField(max_length=100)
    description = models.TextField(max_length=600, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    Price = models.DecimalField(max_digits=6, decimal_places=2)
    food_image = models.FileField(upload_to= 'images/')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    food_item = models.ForeignKey(Food_Item, on_delete=models.CASCADE) 
    food_qty = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    foodcat = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatus= (
        ("cooking", "cooking"), 
        ("Delivered", "Delivered")
    )
    status = models.CharField(max_length=150, choices=orderstatus, default="cooking" )
    message= models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def _str_(self):
        return f"{self.id} - {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(Food_Item, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def _str_(self):
        return f"{self.order.user.username} - {self.order.tracking_no}"
