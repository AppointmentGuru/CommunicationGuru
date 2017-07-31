from rest_framework import decorators
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from slackclient import SlackClient
import os, json

@csrf_exempt
@decorators.api_view(['POST', 'GET'])
def slack_webhook(request):

    token = os.environ.get('SLACK_TOKEN')
    slack_client = SlackClient(token)

    channel = 'bot_factory'
    print (request.data)
    message = """
Data:
```{}```""".format(json.dumps(request.data, indent=2))

    res = slack_client.api_call("chat.postMessage", channel=channel, text=message)
    print(res)

    return HttpResponse('ok')
