from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.utils import timezone

# Create your views here.
@api_view(["GET", "POST"])
def campaign_list(request):
    """
    List all Campaigns in the Database
    """
    if request.method == "GET":
       campaign = Campaign.objects.all()
       serializer = CampaignSerializer(campaign, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(campaign_owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
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
            serializer.save(updated_at=timezone.now)