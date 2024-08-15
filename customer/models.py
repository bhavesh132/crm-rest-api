from django.db import models
from authentication.models import User, BaseModel

# Create your models here.
class Company(BaseModel):
    PRIORITY = {
        'low' : 'Low',
        'medium': 'Medium',
        'high' : 'High'
    }

    SLA_AGREEMENT = {
        'bronze' : 'Bronze',
        'silver' : 'Silver',
        'gold' : 'Gold',
        'platinum' : 'Platinum'
    }

    name = models.TextField()
    website = models.TextField()
    contact_name = models.TextField()
    revenue = models.IntegerField(null=True)
    priority = models.CharField(max_length=50, choices=PRIORITY)
    industry = models.TextField(max_length=150, null=True)
    country = models.TextField(max_length=60, null=True)
    is_active = models.BooleanField(default=True)
    upsell_opportunity = models.BooleanField(default=False)
    sla_agreement = models.CharField(max_length=100, choices=SLA_AGREEMENT)

    def __str__(self):
        return self.name

class Contact(BaseModel):
    CONTACT_TYPE = {
        'lead': 'Lead',
        'customer': 'Customer',
        'partner': 'Partner'
    }
    first_name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    title = models.TextField(max_length=150, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPE)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name