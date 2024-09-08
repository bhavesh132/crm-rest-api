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
    model_name = serializers.CharField(source='__class__.__name__', read_only=True)
    action = serializers.SerializerMethodField()
    object_id = serializers.CharField(source='__class__.__id__', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'

    def get_action(self, obj):
        if self.context.get('action'):
            return self.context['action']
        return None
