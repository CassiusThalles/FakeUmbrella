from rest_framework import serializers
from mysite.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'contact', 'number', 'location', 'country_code', 'employees')