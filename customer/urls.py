from django.urls import path
from .views import *

urlpatterns = [
    path('contact/', contact_list),
    path('contact/<uuid:uuid>/', contact_detail),
    path('company/', company_list),
    path('company/<uuid:uuid>/', company_detail),
]