from rest_framework import serializers
from .models import User, AuditLog
from django.contrib.auth.models import Group, Permission

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ['id','name', 'permissions']

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions)
        return group

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions')
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        instance.permissions.set(permissions)
        return instance
    
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'


