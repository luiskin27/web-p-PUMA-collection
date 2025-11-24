# shop/models.py
from django.db import models
from django.urls import reverse


# === РАЗМЕРЫ ОБУВИ (ДОЛЖНЫ БЫТЬ ПЕРВЫМИ!) ===
class ShoeSize(models.Model):
    SIZE_CHOICES = [
        ('5', '5'), ('5.5', '5.5'), ('6', '6'), ('6.5', '6.5'),
        ('7', '7'), ('7.5', '7.5'), ('8', '8'), ('8.5', '8.5'),
        ('9', '9'), ('9.5', '9.5'), ('10', '10'), ('10.5', '10.5'),
        ('11', '11'), ('11.5', '11.5'), ('12', '12'), ('13', '13'),
    ]
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, unique=True)

    def __str__(self):
        return self.size

    class Meta:
        ordering = ['size']
        verbose_name = 'Размер обуви'
        verbose_name_plural = 'Размеры обуви'


# === РАЗМЕРЫ ОДЕЖДЫ (ВТОРЫМИ!) ===
class ClothingSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'),
        ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL'),
    ]
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, unique=True)

    def __str__(self):
        return self.size

    class Meta:
        ordering = ['size']
        verbose_name = 'Размер одежды'
        verbose_name_plural = 'Размеры одежды'


# === КАТЕГОРИИ ===
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


# === ТОВАРЫ (ПОСЛЕДНИМ!) ===
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_hover = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    colors_count = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # НОВЫЕ ПОЛЯ
    PRODUCT_TYPE_CHOICES = [
        ('shoes', 'Обувь'),
        ('clothing', 'Одежда'),
        ('accessories', 'Аксессуары'),
    ]
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='accessories')

    shoe_sizes = models.ManyToManyField(ShoeSize, blank=True, related_name='products')
    clothing_sizes = models.ManyToManyField(ClothingSize, blank=True, related_name='products')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])