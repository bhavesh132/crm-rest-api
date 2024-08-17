from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_list(request):
    """
    List all Tasks in the Database
    """
    if request.method == "GET":
       task = Task.objects.all()
       serializer = TaskSerializer(task, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_detail(request, uuid):
    try: 
        task = Task.objects.get(id=uuid)
    except Task.DoesNotExist:
        return Response({"message": "No task found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        task.delete()
        return Response({"message": "task removed successfully"}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticket_list(request):
    """
    List all Tickets in the Database
    """
    if request.method == "GET":
       ticket = Ticket.objects.all()
       serializer = TicketSerializer(ticket, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_tickets(request):
    """All tickets assigned to user logged in"""
    if request.method == "GET":
        ticket = Ticket.objects.filter(owner_id=request.user)
        serializer = TicketSerializer(ticket, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    """All tickets assigned to user logged in"""
    if request.method == "GET":
        task = Task.objects.filter(owner_id=request.user)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticket_detail(request, uuid):
    try: 
        ticket = Ticket.objects.get(id=uuid)
    except Ticket.DoesNotExist:
        return Response({"message": "No ticket found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        ticket.delete()
        return Response({"message": "ticket removed successfully"}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def note_list(request):
    """
    List all Notes in the Database
    """
    if request.method == "GET":
       note = Note.objects.all()
       serializer = NoteSerializer(note, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def note_detail(request, uuid):
    try: 
        note = Note.objects.get(id=uuid)
    except Note.DoesNotExist:
        return Response({"message": "No note found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = NoteSerializer(note)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        note.delete()
        return Response({"message": "note removed successfully"}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def type_list(request):
    """
    List all Types in the Database
    """
    if request.method == "GET":
       case = Type.objects.all()
       serializer = TypeSerializer(case, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def type_detail(request, uuid):
    try: 
        case = Type.objects.get(id=uuid)
    except Type.DoesNotExist:
        return Response({"message": "No type found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TypeSerializer(case)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        case.delete()
        return Response({"message": "type removed successfully"}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = TypeSerializer(case, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subtype_list(request):
    """
    List all Opprotunities in the Database
    """
    if request.method == "GET":
       subtype = SubType.objects.all()
       serializer = SubTypeSerializer(subtype, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = SubTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subtype_detail(request, uuid):
    try: 
        subtype = SubType.objects.get(id=uuid)
    except SubType.DoesNotExist:
        return Response({"message": "No subtype found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SubTypeSerializer(subtype)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        subtype.delete()
        return Response({"message": "subtype removed successfully"}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = SubTypeSerializer(subtype, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)