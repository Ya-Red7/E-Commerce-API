from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    image_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.name