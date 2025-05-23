from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import *
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from django.utils import timezone
from authentication.ApiFeatures import GlobalPagination, filter_and_order



# Create your views here.
@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contact_list(request):
    if request.method == "GET":
        queryset = Contact.objects.all()
        contacts = filter_and_order(queryset, request)
        total_count = contacts.count()
        paginator = GlobalPagination()
        paginated_queryset = paginator.paginate_queryset(contacts, request)
        serializer = ContactSerializerGet(paginated_queryset, many=True)
        return Response({
            'data': serializer.data,
            'total_count': total_count
            })
    
    elif request.method == "POST":
        data = request.data
        serializer = ContactSerializerPut(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(modified_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contact_detail(request, uuid):
    try: 
        contact = Contact.objects.select_related('owner').get(id=uuid)
    except Contact.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = ContactSerializerGet(contact)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ContactSerializerPut(contact, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now(), modified_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        contact.delete()
        return HttpResponse(status=204)


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_list(request):
    if request.method == "GET":
        queryset = Company.objects.select_related('modified_by', 'owner', 'contact').all()
        companies = filter_and_order(queryset, request)
        paginator = GlobalPagination()
        paginated_queryset = paginator.paginate_queryset(companies, request)
        serializer = CompanySerializer(paginated_queryset, many=True)
        total_count = companies.count()
        return Response({
            'data': serializer.data,
            'total_count': total_count
            })
    
    elif request.method == "POST":
        data = request.data
        serializer = CompanySerializer(data=data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_detail(request, uuid):
    try: 
        company = company.objects.get(id=uuid)
    except company.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now(), modified_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        company.delete()
        return HttpResponse(status=204)