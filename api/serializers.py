from rest_framework import serializers
from .models import (
    Communication,
    CommunicationStatus,
    CommunicationTemplate
)
from .fields import CurrentUserDefaultUserId

class CommunicationTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunicationTemplate
        fields = '__all__'

class CommunicationStatusSerializer(serializers.ModelSerializer):
    order_by = ('created_date')
    class Meta:
        model = CommunicationStatus
        fields = '__all__'

class MinimalCommunicationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=CurrentUserDefaultUserId())
    class Meta:
        model = Communication
        fields = [
            'owner', 'sender_email', 'channel', 'recipient_id', 'recipient_emails', 'recipient_phone_number',
            'subject', 'short_message', 'message', 'attached_urls', 'created_date', 'last_sent_date'
        ]

# Serializers define the API representation.
class CommunicationListSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=CurrentUserDefaultUserId())
    class Meta:
        model = Communication
        fields = '__all__'

class CommunicationDetailSerializer(serializers.ModelSerializer):
    communicationstatus = CommunicationStatusSerializer(read_only=True, many=True)

    class Meta:
        model = Communication
        fields = '__all__'
