from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    prsn_of_contact = models.CharField('Person of Contact', max_length=60)
    tel_number = models.CharField('Telephone Number', max_length=14)
    location = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3)
    num_of_employees = models.IntegerField('Number of Employees', default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-num_of_employees',)