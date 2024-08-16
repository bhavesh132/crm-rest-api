from django.urls import path
from .views import *

urlpatterns = [
    path('campaign/', campaign_list),
    path('campaign/<uuid:uuid>/', campaign_detail),
]