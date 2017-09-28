from rest_framework import decorators, permissions, routers, serializers, viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from slackclient import SlackClient

from .models import Communication
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

    if (request.data.get('X-Mailgun-Sid') is not None):
        Email(None).status_update(request.data)
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

# Serializers define the API representation.
class CommunicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Communication
        fields = '__all__'

                        # ViewSets define the view behavior.
class CommunicationViewSet(viewsets.ModelViewSet):
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer

router = routers.DefaultRouter()
router.register(r'communications', CommunicationViewSet)
