from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone



# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    num_id = models.AutoField(unique=True, primary_key=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)