'''Backend module for sending messages with PubNub'''
from django.conf import settings
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration

def publish_callback(result, status):
    pass

class PubNubBackend(object):
    '''Send messages with PubNub'''

    def __init__(self):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY
        pnconfig.publish_key = settings.PUBNUB_PUBLISH_KEY
        self.pubnub = PubNub(pnconfig)

    def publish(self, channel, data):
        '''Publish data on channel via PubNub'''
        # return self.pubnub.publish(channel=channel, message=data)
        self.pubnub.publish().channel(channel).message(data).async(publish_callback)

    def subscribe(self, channel):
        '''Subscribe to messages from PubNub (not yet implemented)'''
        pass
