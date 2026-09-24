from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Bags', 'Bags'),
        ('Plushies', 'Plushies'),
        ('Flowers', 'Flowers'),
        ('Accessories', 'Accessories'),
        ('Baby', 'Baby'),
    ]

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Accessories')
    image_url = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
