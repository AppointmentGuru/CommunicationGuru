from rest_framework import \
    decorators,\
    authentication,\
    permissions,\
    routers,\
    viewsets,\
    filters
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from slackclient import SlackClient

from services.email import Email
from services.sms import SMS
from weasyprint import HTML

from .models import Communication
from .mixins import MultiSerializerMixin
from .filters import ObjectOverlapFilterBackend, IsOwnerFilterBackend
from .diagnostics import (
    db_connected,
    celery_working,
    rabbit_is_up,
    failed_tasks_count
)
from .serializers import (
    CommunicationListSerializer,
    CommunicationDetailSerializer
)
from .helpers import (
    get_backend_class
)

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

    # rabbit_status = rabbit_is_up()

    tasks = failed_tasks_count(minutes_back=5, failure_threshold=0)
    result = {
        'SANDBOX': settings.SANDBOX_MODE,
        # 'rabbit': rabbit_status.json(),
        'failed_tasks': tasks.count()
    }

    return JsonResponse(result)


@csrf_exempt
@decorators.api_view(['GET', 'POST'])
@decorators.permission_classes((permissions.AllowAny, ))
def download_pdf(request):
    '''
    turn a url into a pdf and pass through to browser as download
    '''
    url = request.GET.get('url') or request.POST.get('url')
    if url:
        pdf = HTML(url).write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponse("No url received")

@csrf_exempt
@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.AllowAny, ))
def incoming_message(request, backend):
    module, klass = get_backend_class(backend)
    be_class = getattr(module, klass)
    data = request.POST
    be = be_class.from_payload(backend, data)
    be.handle_reply(data)
    return HttpResponse('ok')


@csrf_exempt
@decorators.api_view(['POST', 'GET'])
@decorators.permission_classes((permissions.AllowAny, ))
def status_update(request):
    module, klass = get_backend_class(backend)
    be_class = getattr(module, klass)
    data = request.POST
    be = be_class.from_payload(backend, data)
    be.handle_reply(data)
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
`POST`:
```{}```""".format(json.dumps(request.data, indent=2))
    res = slack_client.api_call("chat.postMessage", channel=channel, text=message)
    print(res)

    if len(request.GET.dict().items()) > 0:
        message = """
    `GET`:
    ```{}```""".format(json.dumps(request.GET.dict(), indent=2))
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
        params['campaign'] = 'practitioner-{}'.format(request.user.id)

        data = SMS().search(params).json()
    except AssertionError:
        data = {
            'message': 'Sorry, the current backend does not support searching for SMSes'
        }
        status_code = 403
    return JsonResponse(data, status=status_code)


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
