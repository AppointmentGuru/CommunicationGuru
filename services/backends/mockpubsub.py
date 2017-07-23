'''
A mock backend for pub sub
'''

class MockPubSubBackend(object):
    '''Mock class for pubsub'''

    def __init__(self):
        pass

    def publish(self, channel, data):
        '''Fake publish data to channel (does nothing)'''
        return True

    def subscribe(self, channel):
        '''fake subscribe channel (does nothing)'''
        pass