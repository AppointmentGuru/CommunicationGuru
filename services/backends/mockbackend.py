'''
A mock backend that can be used for testing
'''
import uuid

def get_id():
    return str(uuid.uuid4())

class MockShortMessageBackend:
    backend_id = 'services.backends.mockbackend.MockShortMessageBackend'

    def __init__(self, communication):
        self.communication = communication

    def send(self):
        self.communication.backend_used = self.backend_id
        self.communication.backend_message_id = get_id()
        self.communication.backend_result = {
            "id": self.communication.backend_message_id,
            "message": "Your mock message was mock sent"
        }
        self.communication.save()
        return (self.communication)