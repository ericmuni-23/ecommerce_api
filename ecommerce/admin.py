from django.contrib import admin

from .models import Category, Product, User, Review, Wishlist, Promotion
# Register your models here.

admin.site.register((Category, Product, User, Review, Wishlist, Promotion))
