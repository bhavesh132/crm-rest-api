from authentication.serializer import UserSerializer
from customer.serializer import *
from .models import *
from rest_framework import serializers


# Type, Subtype, Ticket, Note, Task

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class SubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubType
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = Note
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    ticket_type = TypeSerializer()
    ticket_subtype = SubTypeSerializer()
    created_by = UserSerializer()
    modified_by = UserSerializer()
    owner = UserSerializer()
    customer_id= ContactSerializerGet()
    class Meta:
        model = Ticket
        fields = '__all__'



class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    recipient_list = serializers.ListField(child=serializers.EmailField())

