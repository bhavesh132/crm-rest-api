from dataclasses import fields
from .models import Contact, Company
from authentication.models import User
from rest_framework import serializers
from authentication.serializer import UserSerializer

class ContactSerializerPut(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Allow updating

    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user  # Auto-assign on POST
        return super().create(validated_data)


class ContactSerializerGet(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = Contact
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    contact = ContactSerializerGet()
    class Meta:
        model = Company
        fields = '__all__'