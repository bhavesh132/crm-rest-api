from .views import *
from django.urls import path

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user_detail/<uuid:uuid>', user_view, name='user_detail'),
    path('groups/', GroupCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
    path('get_logs/', get_audit_logs, name='get_logs'),
]