from django.db import models
from customer.models import Contact, Company
from authentication.models import User, BaseModel

# Create your models here.
class Campaign(BaseModel):
    TYPE_CHOICES = [
        ('Webinar', 'Webinar'),
        ('Conference', 'Conference'),
        ('Public Relations', 'Public Relations'),
        ('Advertisement', 'Advertisement'),
        ('Banners', 'Banners'),
    ]

    campaign_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # Added description field
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    expected_response = models.IntegerField()
    leads = models.ManyToManyField(Contact, related_name='campaigns')
    responses = models.ManyToManyField(Contact, related_name='responses', blank=True)
    campaign_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.campaign_name


class Opportunity(BaseModel):
    STAGE_CHOICES = [
        ('Open Discussion', 'Open Discussion'),
        ('Not Started', 'Not Started'),
        ('Closed - Won', 'Closed - Won'),
        ('Closed - Lost', 'Closed - Lost'),
    ]

    opportunity_name = models.CharField(max_length=255)
    company_name = models.TextField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact_name = models.ForeignKey(Contact, on_delete=models.CASCADE)  # Assuming you have a Contact model
    campaign_name = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    probability = models.DecimalField(max_digits=5, decimal_places=2)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)

    def __str__(self):
        return self.opportunity_name
