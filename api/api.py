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

from .models import Communication
from .mixins import MultiSerializerMixin
from .filters import ObjectOverlapFilterBackend, IsOwnerFilterBackend
from .diagnostics import \
    db_connected,\
    celery_working,\
    rabbit_is_up,\
    failed_tasks_count
from .serializers import \
    CommunicationListSerializer,\
    CommunicationDetailSerializer

from kong_oauth.drf_authbackends import KongDownstreamAuthHeadersAuthentication
import os, json, requests

@csrf_exempt
@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny, ))
def health(request):

    # test connect to db:
    db_connected(Communication)
    # test sending a task:
    celery_working()

    rabbit_status = rabbit_is_up()

    tasks = failed_tasks_count(minutes_back=5, failure_threshold=0)
    result = {
        'SANDBOX': settings.SANDBOX_MODE,
        'rabbit': rabbit_status.json(),
        'failed_tasks': tasks.count()
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
@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAuthenticated,))
@decorators.authentication_classes((
    authentication.SessionAuthentication,
    KongDownstreamAuthHeadersAuthentication,
))
def backends_messages(request, transport):
    '''
    Hits the configured backends list endpoint
    '''
    status_code = 200

    try:
        params = request.GET.copy()
        data = SMS().search(params).json()
    except AssertionError:
        data = {
            'message': 'Sorry, the current backend does not support searching for SMSes'
        }
        status_code = 403
    return JsonResponse(data, status=status_code)

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
