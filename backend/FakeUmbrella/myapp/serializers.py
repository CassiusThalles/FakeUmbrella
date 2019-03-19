from rest_framework import serializers
from myapp.models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'prsn_of_contact', 'tel_number', 'location', 'country_code', 'num_of_employees')