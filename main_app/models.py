from django.db import models


class Category(models.Model):
    name_category = models.CharField(max_length=127)
    slug = models.SlugField(unique=True, max_length=127)

    def __str__(self):
        return self.name_category

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name_subcategory = models.CharField(max_length=127)
    slug = models.SlugField(unique=True, max_length=127)

    def __str__(self):
        return self.name_subcategory

class Product(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=127)
    name_product = models.CharField(max_length=127)
    description = models.TextField(max_length=1027)
    image = models.ImageField(upload_to = 'images/', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name_product