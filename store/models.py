from django.db import models
from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from uuid import uuid4

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # don't need to add products = models.ManyToManyField(Product).
    # Django will automatically create reverse relationship as 
    # product_set
    def __str__(self):
        return f'{self.discount} discount'

class Collection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField() # slug makes search engine more see to the title
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) # set date every time the object is saved
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT) # if we delete our collection, product shouldn't be deleted
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'BRONZE'),
        (MEMBERSHIP_SILVER, 'SILVER'),
        (MEMBERSHIP_GOLD, 'GOLD'),
    ]

    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True) # we use DateField because we don't care the time of birth
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    #address_set
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    # this method is written because of CustomerAdmin request
    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name # user model's frist_name

    # this method is written because of CustomerAdmin request
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name']
        permissions = [
            ("can_cancel_order", "Cancel Order"),
            ("view_history", "Can read history"),
        ]
    '''
    This is a list or tuple of 2-tuples in the format (permission_code, human_readable_permission_name).

    permissions = [
        (permission_code, human_readable_permission_name),
    ]

    (https://docs.djangoproject.com/en/5.1/ref/models/options/#permissions)
    '''


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'PENDING'),
        (PAYMENT_STATUS_COMPLETE, 'COMPLETE'),
        (PAYMENT_STATUS_FAILED, 'FALIED'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True) # set date at the time of object is created
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT) # if the customer is deleted, we shouldn't delete the order because order represents our sales
    # orderitem_set

    class Meta:
        ordering = ['id']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField() # positive small interger field prevents giving negative value
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, null=True) # product already has price, but price can change, so it should have the price at the time of order

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)# GUID format
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem') # if  the cart is deleted, all the cartitem is deleted
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # many(CartItem) -> one(Product)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']] # a cart with no duplicate product


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)