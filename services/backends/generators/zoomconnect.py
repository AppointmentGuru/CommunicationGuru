'''
A collection of sample data generators for zoomconnect
'''
from faker import Factory
FAKE = Factory.create()

def successful_send_response():
    return {'messageId': '5b37661ae396c8e42e0c9ca2', 'error': None}

def send_error_response():
    return {
        "status": "INTERNAL_SERVER_ERROR",
        "code": 1,
        "message": "An error occurred while processing your request.",
        "developerMessage": "Please contact support.",
        "moreInfoUrl": "None"
    }

def reply():
    return {
        "date": "201806292136",
        "dataField": "cli:1,app:21502,pra:3001,pro:17554,",
        "repliedToMessageId": "123",
        "messageId": "456",
        "campaign": "some-campaign",
        "from": "+27832565643",
        "to": "27987654349",
        "nonce-date": "20180629214112",
        "message": "Testing testing 123",
        "nonce": "5cfb2a28-c660-4b4d-aa6e-aeafc8f04563",
        "checksum": "072a46e882faab427434cb8f2e4e01159cf6f9ab"
    }

def status_update():
    return {
        "dataField": "test",
        "messageId": "5b37661ae396c8e42e0c9ca2",
        "campaign": "test-channel",
        "nonce-date": "20180630131940",
        "nonce": "44bebaf2-5e52-492c-8a74-dd5383d2f29f",
        "status": "DELIVERED",
        "checksum": "6bb6e745804d49c2cc2f7303c08d7ea1332e5ad3"
    }