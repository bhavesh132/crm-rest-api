from django.db import models
from authentication.models import User, BaseModel
from customer.models import Contact
from django.utils import timezone

# Create your models here.
class Type(BaseModel):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name

class SubType(BaseModel):
    name = models.TextField(max_length=100)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ticket(BaseModel):
    TICKET_STATUS = {
        "new": "New",
        "assigned": "Assigned",
        "in-progress": "In-Progress",
        "completed": "Completed",
        "closed": "Closed",
        "needs-review": "Needs Review",
        "cancelled": "Cancelled"
    }

    PRIORITY = {
        "p1": "P1",
        "p2": "P2",
        "p3": "P3",
        "p4": "P4",
    }

    title = models.CharField(max_length=150)
    ticket_type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)
    ticket_subtype = models.ForeignKey(SubType, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=TICKET_STATUS)
    priority = models.TextField(max_length=20, default="p2", choices=PRIORITY)
    customer_id = models.ForeignKey(Contact, null=True, on_delete=models.SET_NULL)
    owner_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Note(BaseModel):
    body = models.TextField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)


    def __str__(self):
        return self.body
    

class Task(BaseModel):
    SUBJECT = {
        'email' : 'Email',
        'call' : 'Call',
        'other' : 'Other'
    }

    STATUS = {
        'completed': 'Completed',
        'in-progress': 'In Progress',
        'new' : 'New',
        'cancelled': 'Cancelled'
    }
    title = models.CharField(max_length=255)
    subject = models.TextField(max_length=100, choices=SUBJECT)
    status = models.TextField(max_length=50, choices=STATUS)
    due_date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    contact_name = models.ForeignKey(Contact, null=True, on_delete=models.SET_NULL)
    comments = models.TextField(null=True)

    def __str__(self):
        return self.title