import json
import decimal
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework.authentication import TokenAuthentication
from .models import User, AuditLog
from .serializer import UserSerializer, GroupSerializer, PermissionSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from .permissions import IsInGroup, CanViewOnlyGroups
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .serializer import AuditLogSerializer
from authentication.ApiFeatures import GlobalPagination, filter_and_order
from django.forms.models import model_to_dict
from uuid import UUID
from django.apps import apps
from django.http import JsonResponse, Http404
from django.views import View
from datetime import datetime, date


_old_instances = {}
# Create your views here.
@api_view(['POST'])
def register_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)

            max_age = 60 * 60 * 24  # 1 day in seconds
            expires = (timezone.now() + timedelta(seconds=max_age))
            response = Response({'token': token.key, 'user':serializer.data}, status=200)
            response.set_cookie(key='auth_token', value=token.key, expires=expires, httponly=True)
            return response
        return Response(serializer.errors, status=400)
    

@api_view(['POST'])
def user_login(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try: 
                email_user = User.objects.get(email=username)
                if (email_user):
                    user = authenticate(username=email_user.username, password=password)
            except ObjectDoesNotExist:
                Response({'error': 'Invalid Credentials'}, status=401)
        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            user.last_login = timezone.now()
            user.save()
            serializer = UserSerializer(instance=user)
            max_age = 60 * 60 * 24  # 1 day in seconds
            expires = (timezone.now() + timedelta(seconds=max_age))
            response = Response({'token': token.key, 'user':serializer.data}, status=200)
            response.set_cookie(key='auth_token', value=token.key, expires=expires, httponly=True, path='/', samesite='lax')
            return response
        return Response({'error': 'Invalid Credentials'}, status=401)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            response = Response({'message': 'Successfully logged out.'}, status=200)
            response.delete_cookie('auth_token')
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request, uuid):
    try:
        user = User.objects.get(id=uuid)
    except User.DoesNotExist:
         return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=201)
    
    if request.method == 'PUT':
        data = request.data
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    if request.method == 'DELETE':
        user.delete()
        return Response(status=204)
    
class GroupCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, OR(IsInGroup, CanViewOnlyGroups)]
    group_name = 'Leads'
    authentication_classes = [TokenAuthentication]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInGroup]
    group_name = 'Leads'
    authentication_classes = [TokenAuthentication]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermissionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsInGroup]
    group_name = 'Leads'
    authentication_classes = [TokenAuthentication]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


def convert_to_serializable(data):
    """
    Convert UUIDs and other non-serializable objects to strings for JSON serialization.
    """
    if isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, UUID):
        return str(data)  # Convert UUID to string
    elif isinstance(data, datetime):
        return data.isoformat()  
    elif isinstance(data, date):
        return data.isoformat()  
    elif isinstance(data, decimal.Decimal):
        return float(data)  
    return data


@receiver(pre_save)
def capture_old_instance(sender, instance, **kwargs):
    """
    Capture the old instance before it is updated in the database.
    This signal is triggered before saving the instance.
    """
    if sender in [AuditLog, LogEntry, Token]:
        return

    try:
        # Get the existing instance from the database
        old_instance = sender.objects.get(pk=instance.pk)
        _old_instances[instance.pk] = model_to_dict(old_instance)
    except sender.DoesNotExist:
        # If the instance is new, no old instance exists
        _old_instances[instance.pk] = None

# @receiver([post_save, post_delete])
# def create_audit_log(sender, instance, **kwargs):
#     # Skip logging for the AuditLog, LogEntry, and Token models
#     if sender in [AuditLog, LogEntry, Token, Session]:
#         return

#     # Get the user (if exists)
#     user = None
#     if hasattr(instance, 'modified_by'):
#         user = instance.modified_by

#     if sender == User:
#         request = kwargs.get('request', None)
#         if request and (request.path == 'auth/login/' or request.path == 'auth/logout/'):
#             return

#     # Determine the action (created, updated, deleted)
#     if kwargs.get('signal') == post_delete:
#         action = 'Deleted'
#         changes = model_to_dict(instance)  # No changes captured for deletion
#     elif kwargs.get('created', False):
#         action = 'Created'
#         # Capture all fields on creation
#         changes = model_to_dict(instance)
#     else:
#         action = 'Updated'
#         changes = {}
#         try:
#             # Fetch the old instance from the database
#               # Fetch the old instance from the pre_save signal's dictionary
#             old_instance_dict = _old_instances.get(instance.pk)

#             if old_instance_dict:
#                 new_instance_dict = model_to_dict(instance)

#                 # Compare the old and new instance field values
#                 for field, old_value in old_instance_dict.items():
#                     new_value = new_instance_dict.get(field)
#                     if old_value != new_value:
#                         if field == "last_login":
#                             return
#                         changes[field] = {'old': old_value, 'new': new_value}
        
#         except sender.DoesNotExist:
#                 # Handle the case where the old instance does not exist
#             changes = model_to_dict(instance)

#     # Clean up fields like _state from changes (unnecessary in logs)

#     # Convert changes to JSON serializable format
#     serializable_changes = convert_to_serializable(changes)

#     app_label = sender._meta.app_label
#     # Create a new audit log entry
#     AuditLog.objects.create(
#         model_name=sender.__name__,
#         action=action,
#         object_id=instance.pk,
#         app_label=app_label,
#         changes=json.dumps(serializable_changes, indent=4),  # Store changes as JSON
#         timestamp=timezone.now(),
#         user=user  # Log the user making the change
#     )
# # Disconnect the signal for the AuditLog model
# post_save.disconnect(create_audit_log, sender=AuditLog)
# post_delete.disconnect(create_audit_log, sender=AuditLog)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_audit_logs(request):
    queryset = AuditLog.objects.all().order_by('-id')
    logs = filter_and_order(queryset, request)
    paginator = GlobalPagination()
    paginated_queryset = paginator.paginate_queryset(logs, request)
    serializer = AuditLogSerializer(paginated_queryset, many=True)
    return Response(serializer.data)


class InstanceDetailView(View):
    def get(self, request, app_label, model_name, object_id):
        try:
            # Dynamically get the model class
            model = apps.get_model(app_label=app_label, model_name=model_name)
            # Fetch the instance
            instance = model.objects.get(pk=object_id)
            # Return instance details as a JSON response
            return JsonResponse({
                'data': model_to_dict(instance)
            })
        except model.DoesNotExist:
            raise Http404(f"{model_name} instance with id {object_id} does not exist.")