from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=60)
    number = models.CharField(max_length=14)
    location = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3)
    employees = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-employees',)