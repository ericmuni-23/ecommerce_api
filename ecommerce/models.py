from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Max
import re

def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError(
            _('Username must contain only letters, numbers, and underscores'),
            params={'value': value},
        )

# ID generators for each model
def generate_category_id():
    max_id = Category.objects.aggregate(Max('id'))['id__max']
    return 55499885 if max_id is None else max_id + 2

def generate_product_id():
    max_id = Product.objects.aggregate(Max('id'))['id__max']
    return 65499885 if max_id is None else max_id + 2

def generate_review_id():
    max_id = Review.objects.aggregate(Max('id'))['id__max']
    return 75499885 if max_id is None else max_id + 2

def generate_wishlist_id():
    max_id = Wishlist.objects.aggregate(Max('id'))['id__max']
    return 85499885 if max_id is None else max_id + 2

def generate_promotion_id():
    max_id = Promotion.objects.aggregate(Max('id'))['id__max']
    return 95499885 if max_id is None else max_id + 2

class Category(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_category_id)
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_category_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'categories'

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            MinLengthValidator(3),
            validate_username,
        ],
        help_text=_('Required. 3-150 characters. Letters, numbers, and underscores only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.'),
    )
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    
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

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

class Product(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_product_id)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='created_products',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_product_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

class Review(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_review_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_review_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username if self.user else 'Anonymous'}"

    class Meta:
        ordering = ['id']

class Wishlist(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_wishlist_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    created_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_wishlist_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Wishlist item for {self.user.username}"

    class Meta:
        ordering = ['id']
        unique_together = ('user', 'product')

class Promotion(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_promotion_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_promotion_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Promotion for {self.product.name}"

    class Meta:
        ordering = ['id']
