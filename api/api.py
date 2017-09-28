from rest_framework import decorators, permissions, routers, serializers, viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from slackclient import SlackClient

from .models import Communication, CommunicationStatus
from .mixins import MultiSerializerMixin
from services.email import Email
from services.sms import SMS

import os, json

@csrf_exempt
@decorators.api_view(['GET'])
def health(request):
    return HttpResponse('ok')

@csrf_exempt
@decorators.api_view(['POST', 'GET'])
@decorators.permission_classes((permissions.AllowAny, ))
def slack_webhook(request):

    token = os.environ.get('SLACK_TOKEN')
    slack_client = SlackClient(token)

    channel = 'bot_factory'
    print(request.data)

    if request.data.get('X-Mailgun-Sid') is not None:
        Email(None).status_update(request.data)
    if request.data.get('message-id') is not None:
        # normalize mailgun message ids .. sigh
        data = request.data.copy()
        data['Message-Id'] = "<{}>".format(data.get('message-id'))
        Email(None).status_update(data)
    if (request.data.get('SmsSid') is not None):
        SMS().status_update(request.data)
    message = """
Data:
```{}```""".format(json.dumps(request.data, indent=2))

    res = slack_client.api_call("chat.postMessage", channel=channel, text=message)
    print(res)

    return HttpResponse('ok')


@csrf_exempt
@decorators.api_view(['POST', 'GET'])
@decorators.permission_classes((permissions.AllowAny, ))
def incoming_email(request):
    pass

class CommunicationStatusSerializer(serializers.ModelSerializer):
    order_by = ('created_date')
    class Meta:
        model = CommunicationStatus
        fields = '__all__'

# Serializers define the API representation.
class CommunicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = '__all__'

class CommunicationDetailSerializer(serializers.ModelSerializer):
    communicationstatus = CommunicationStatusSerializer(read_only=True, many=True)
    class Meta:
        model = Communication
        fields = '__all__'


class CommunicationViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    queryset = Communication.objects.all()

    default_serializer_class = CommunicationListSerializer
    serializer_map = {
        'retrieve': CommunicationDetailSerializer,
        'list': CommunicationListSerializer
    }

router = routers.DefaultRouter()
router.register(r'communications', CommunicationViewSet)
