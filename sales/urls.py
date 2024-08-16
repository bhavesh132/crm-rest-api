from django.urls import path
from .views import *

urlpatterns = [
    path('campaign/', campaign_list),
    path('campaign/<uuid:uuid>/', campaign_detail),
    path('opportunity/', opportunity_list),
    path('opportunity/<uuid:uuid>/', opportunity_detail),
]