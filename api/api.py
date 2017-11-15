from rest_framework import \
    decorators,\
    authentication,\
    permissions,\
    routers,\
    viewsets,\
    filters
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from slackclient import SlackClient

from services.email import Email
from services.sms import SMS

from .tasks import ping
from .models import Communication
from .mixins import MultiSerializerMixin
from .filters import ObjectOverlapFilterBackend, IsOwnerFilterBackend
from .serializers import \
    CommunicationStatusSerializer,\
    CommunicationListSerializer,\
    CommunicationDetailSerializer

from kong_oauth.drf_authbackends import KongDownstreamAuthHeadersAuthentication
import os, json, requests

@csrf_exempt
@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny, ))
def health(request):

    # test connect to db:
    comm = Communication.objects.first()
    # test sending a task:
    task = ping.apply()
    assert task.status == 'SUCCESS',\
        'Error when queuing a task'

    url = 'http://{}:15672/api/healthchecks/node'.format(os.environ.get('RABBITMQ_DEFAULT_HOST'))
    user = os.environ.get('RABBITMQ_DEFAULT_USER')
    passwd = os.environ.get('RABBITMQ_DEFAULT_PASS')

    rabbit_status = requests.get(url, auth=(user, passwd))
    assert rabbit_status.json().get('status') == 'ok',\
        'Issues connecting to rabbit: {}'.format(rabbit_status.content)

    result = {
        'SANDBOX': settings.SANDBOX_MODE,
        'rabbit': rabbit_status.json()
    }

    return JsonResponse(result)

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

class CommunicationViewSet(MultiSerializerMixin, viewsets.ModelViewSet):

    queryset = Communication.objects.all()

    authentication_classes = (
        authentication.SessionAuthentication,
        KongDownstreamAuthHeadersAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    default_serializer_class = CommunicationListSerializer
    serializer_map = {
        'retrieve': CommunicationDetailSerializer,
        'list': CommunicationListSerializer
    }
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        IsOwnerFilterBackend,
        ObjectOverlapFilterBackend)

    ordering = ('-id',)

router = routers.DefaultRouter()
router.register(r'communications', CommunicationViewSet)
