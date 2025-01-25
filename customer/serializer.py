from dataclasses import fields
from .models import Contact, Company
from rest_framework import serializers
from authentication.serializer import UserSerializer

class ContactSerializerGet(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    owner = UserSerializer()
    class Meta:
        model = Contact
        fields = '__all__'
        # fields = ['id', 'first_name', 'last_name','full_name', 'title', 'company_name', "owner", 'contact_type', 'email', 'contact_number', 'created_at', 'updated_at', 'num_id']

class ContactSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'