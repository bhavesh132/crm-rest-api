from rest_framework.decorators import api_view
from rest_framework.response import Response
from service.models import Ticket, Task
from sales.models import *
from django.db.models import Q
from django.utils import timezone

@api_view(['GET'])
def dashboard_summary(request):
    user = request.user
    tickets_summary = {
        'Critical Tickets': Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]), priority='p1', owner=user).count(),
        'Urgent Tickets': Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]), priority='p2', owner=user).count(),
        'Standard Tickets': Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]), priority='p3', owner=user).count(),
        'Scheduled Tickets': Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]), priority='p4', owner=user).count(),
        # 'Open Tickets': Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]),owner=user).count(),
        'Due Today' : Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]), owner=user, due_date=timezone.now().date()).count()
    }

    tasks_summary = {
        'Critical Tasks': Task.objects.filter(~Q(status__in=["completed", "cancelled"]), priority='p1', owner=user).count(),
        'Urgent Tasks': Task.objects.filter(~Q(status__in=["completed", "cancelled"]), priority='p2', owner=user).count(),
        'Standard Tasks': Task.objects.filter(~Q(status__in=["completed", "cancelled"]), priority='p3', owner=user).count(),
        'Scheduled Tasks': Task.objects.filter(~Q(status__in=["completed", "cancelled"]), priority='p4', owner=user).count(),
        # 'Open Tasks': Task.objects.filter(~Q(status__in=["completed", "cancelled"]),owner=user).count(),   
        'Due Today' : Task.objects.filter(~Q(status__in=["completed", "cancelled"]), owner=user, due_date=timezone.now().date()).count(),
        'Critical Due Today' : Task.objects.filter(~Q(status__in=["completed", "cancelled"]), priority='p1', owner=user, due_date=timezone.now().date()).count()
    }

    opportunities_summary = {
        'Open Opportunities': Opportunity.objects.filter(stage='Open Discussion', owner=user).count(),
        'New Opportunities': Opportunity.objects.filter(stage="Not Started", owner=user).count(),
        'Low Probability': Opportunity.objects.filter(stage__in=['Open Discussion', 'Not Started'],probability__lt=50, owner=user).count(),
        'High Probability': Opportunity.objects.filter(stage__in=['Open Discussion', 'Not Started'], probability__gt=50, owner=user).count()
    }

    campaigns_summary = {
        # 'Active Campaigns': Campaign.objects.filter(active=True, owner=user).count(),
        'Webinar' : Campaign.objects.filter(active=True, type='Webinar', owner=user).count(),
        'Conference' : Campaign.objects.filter(active=True, type='Conference', owner=user).count(),
        'Public Relations' : Campaign.objects.filter(active=True, type='Public Relations', owner=user).count(),
        'Advertisement' : Campaign.objects.filter(active=True, type='Advertisement', owner=user).count(),
        'Banner' : Campaign.objects.filter(active=True, type='Banners', owner=user).count(),
        
    }

    data = {
        'tickets': tickets_summary,
        'opportunities': opportunities_summary,
        'campaigns': campaigns_summary,
        'tasks': tasks_summary
    }

    return Response(data)



@api_view(['GET'])
def total_data(request):
    user = request.user
    total_tickets = Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]), owner=user).count()
    total_opportunities = Opportunity.objects.filter( stage__in=['Open Discussion', 'Not Started'], owner=user).count()
    total_tasks = Task.objects.filter(~Q(status__in=["completed", "cancelled"]), owner=user).count()
    total_campaigns = Campaign.objects.filter(active=True , owner=user).count()

    data = {
        'tickets': total_tickets,
        'opportunities': total_opportunities,
        'campaigns': total_campaigns,
        'tasks': total_tasks
    }

    return Response(data)
