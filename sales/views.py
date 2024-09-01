from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from authentication.ApiFeatures import GlobalPagination, filter_and_order

# Create your views here.
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def campaign_list(request):
    """
    List all Campaigns in the Database
    """
    if request.method == "GET":
        queryset = Campaign.objects.all()
        campaigns = filter_and_order(queryset, request)
        paginator = GlobalPagination()
        paginated_queryset = paginator.paginate_queryset(campaigns, request)
        serializer = CampaignSerializer(paginated_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def campaign_detail(request, uuid):
    try: 
        campaign = Campaign.objects.get(id=uuid)
    except Campaign.DoesNotExist:
        return Response({"message": "No campaign found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        campaign.delete()
        return Response({"message": "campaign removed successfully"}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = CampaignSerializer(campaign, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now(), modified_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def opportunity_list(request):
    """
    List all Opprotunities in the Database
    """
    if request.method == "GET":
        queryset = Opportunity.objects.all()
        opportunities = filter_and_order(queryset, request)
        paginator = GlobalPagination()
        paginated_queryset = paginator.paginate_queryset(opportunities, request)
        serializer = OpportunitySerializer(paginated_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def opportunity_detail(request, uuid):
    try: 
        opportunity = Opportunity.objects.get(id=uuid)
    except Opportunity.DoesNotExist:
        return Response({"message": "No opportunity found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OpportunitySerializer(opportunity)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        opportunity.delete()
        return Response({"message": "opportunity removed successfully"}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = OpportunitySerializer(opportunity, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now(), modified_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)