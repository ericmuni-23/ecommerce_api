from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Category(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    image_url = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="ecommerce_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="ecommerce_user_set",
        related_query_name="user",
    )

    # Add any additional fields here

    def __str__(self):
        return self.username

class Review(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

class Wishlist(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist item for {self.user.username}"

class Promotion(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Promotion for {self.product.name}"
    
    