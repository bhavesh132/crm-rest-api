from .models import Contact, Company
from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name','full_name', 'title', 'company_name', "owner", 'contact_type', 'email', 'contact_number', 'created_at', 'updated_at', 'num_id']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'