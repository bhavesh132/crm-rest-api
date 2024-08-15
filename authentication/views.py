from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework.authentication import TokenAuthentication
from .models import User
from .serializer import UserSerializer, GroupSerializer, PermissionSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from .permissions import IsInGroup, CanViewOnlyGroups


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
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass
        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(instance=user)
            max_age = 60 * 60 * 24  # 1 day in seconds
            expires = (timezone.now() + timedelta(seconds=max_age))
            response = Response({'token': token.key, 'user':serializer.data}, status=200)
            response.set_cookie(key='auth_token', value=token.key, expires=expires, httponly=True)
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