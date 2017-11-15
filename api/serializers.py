from rest_framework import serializers
from .models import Communication, CommunicationStatus
from .fields import CurrentUserDefaultUserId


class CommunicationStatusSerializer(serializers.ModelSerializer):
    order_by = ('created_date')
    class Meta:
        model = CommunicationStatus
        fields = '__all__'

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
