from rest_framework.response import Response
from django.http import HttpResponse
from .models import *
from .serializer import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from django.utils import timezone

# Create your views here.
@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contact_list(request):
    if request.method == "GET":
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        serializer = ContactSerializer(data=data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contact_detail(request, uuid):
    try: 
        contact = Contact.objects.get(id=uuid)
    except Contact.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        contact.first_name = request.data.get('first_name', contact.first_name)
        contact.last_name = request.data.get('last_name', contact.last_name)
        contact.title = request.data.get('title', contact.title)
        contact.contact_type = request.data.get('contact_type', contact.contact_type)
        contact.email = request.data.get('email', contact.email)
        contact.contact_number = request.data.get('contact_number', contact.contact_number)

        contact.save(updated_at=timezone.now())
    
    elif request.method == "DELETE":
        contact.delete()
        return HttpResponse(status=204)


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_list(request):
    if request.method == "GET":
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)
    
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
        company.name = request.data.get('name', company.name)
        company.website = request.data.get('website', company.website)
        company.revenue = request.data.get('revenue', company.revenue)
        company.priority = request.data.get('priority', company.priority)
        company.industry = request.data.get('industry', company.industry)
        company.country = request.data.get('country', company.country)
        company.is_active = request.data.get('is_active', company.is_active)
        company.upsell_opportunity = request.data.get('upsell_opportunity', company.upsell_opportunity)
        company.sla_agreement = request.data.get('sla_agreement', company.sla_agreement)

        company.save(updated_at=timezone.now())
    
    elif request.method == "DELETE":
        company.delete()
        return HttpResponse(status=204)