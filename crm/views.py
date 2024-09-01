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
        'critical_tickets': Ticket.objects.filter(priority='p1', owner=user).count(),
        'open_tickets': Ticket.objects.filter(~Q(status__in=["closed", "completed", "cancelled"]),owner=user).count(),
        'total_tickets': Ticket.objects.filter(owner=user).count(),
        'due_today' : Ticket.objects.filter(owner=user, due_date=timezone.now().date())
    }

    tasks_summary = {
        'critical_tasks': Task.objects.filter(~Q(status__in=["completed", "cancelled"]), priority='p1', owner=user).count(),
        'open_tasks': Task.objects.filter(~Q(status__in=["completed", "cancelled"]),owner=user).count(),
        'total_tasks': Task.objects.filter(owner=user).count(),
        'due_today' : Task.objects.filter(~Q(status__in=["completed", "cancelled"]), owner=user, due_date=timezone.now().date())
    }

    opportunities_summary = {
        'total_opportunities': Opportunity.objects.filter(owner=user).count(),
        'open_opportunities': Opportunity.objects.filter(stage='Open Discussion', owner=user).count(),
        'new_opportunities': Opportunity.objects.filter(stage="Not Started", owner=user).count()
    }

    campaigns_summary = {
        'active_campaigns': Campaign.objects.filter(active=True, owner=user).count(),
        'total_campaigns': Campaign.objects.filter(owner=user).count(),
    }

    data = {
        'tickets': tickets_summary,
        'opportunities': opportunities_summary,
        'campaigns': campaigns_summary,
        'tasks': tasks_summary
    }

    return Response(data)