from django.urls import path
from .views import *

urlpatterns = [
    path('ticket/', ticket_list),
    path('ticket/<uuid:uuid>/', ticket_detail),
    path('note/', note_list),
    path('note/<uuid:uuid>/', note_detail),
    path('type/', type_list),
    path('type/<uuid:uuid>/', type_detail),
    path('subtype/', subtype_list),
    path('subtype/<uuid:uuid>/', subtype_detail),
    path('task/', task_list),
    path('task/<uuid:uuid>/', task_detail),
    path('my_task/<uuid:uuid>/', my_tasks),
    path('my_tickets/', my_tickets),
]