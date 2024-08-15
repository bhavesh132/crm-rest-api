from .models import Contact, Company
from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name','title', 'company', "owner", 'contact_type', 'email', 'contact_number', 'created_at']
