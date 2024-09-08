from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime
from django.utils import timezone



# Create your models here.
class User(AbstractUser):
    id = models.UUIDField( default=uuid.uuid4, editable=False)
    num_id = models.AutoField(unique=True, primary_key=True)
    role = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    modified_by = models.ForeignKey('self', related_name='%(class)s_modifier', on_delete=models.SET_NULL, null=True, blank=True)


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    num_id = models.AutoField(unique=True, primary_key=True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='%(class)s_modifier', on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, null=True,related_name='%(class)s_owner', on_delete=models.SET_NULL)

    class Meta:
        abstract = True

class AuditLog(models.Model):
    model_name = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    app_label = models.CharField(max_length=50, null=True)
    object_id = models.TextField()
    changes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.action} on {self.model_name} by {self.user} at {self.timestamp}'