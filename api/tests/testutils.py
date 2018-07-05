# from faker import Factory
# FAKE = Factory.create()
from api.models import (
    CommunicationTemplate,
    Communication
)
MOCK_SCHEMA = {
  "$id": "http://example.com/example.json",
  "type": "object",
  "definitions": {},
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "foo": {
      "$id": "/properties/foo",
      "type": "string",
      "title": "The Foo Schema ",
      "default": "",
      "examples": [
        "bar"
      ]
    }
  }
}

def assert_response(response, expected_status=200):
    assert response.status_code == expected_status, \
        'Expected status: {}. Got: {}. {}'.format(expected_status, response.status_code, response.content)

def get_proxy_headers(user_id, consumer='joesoap', headers = {}):
    is_anon = user_id is None
    headers.update({
        'HTTP_X_ANONYMOUS_CONSUMER': is_anon,
        'HTTP_X_AUTHENTICATED_USERID': user_id,
        'HTTP_X_CONSUMER_USERNAME': consumer
    })
    headers['HTTP_X_CONSUMER_USERNAME'] = consumer

    if user_id is None:
        headers['HTTP_X_ANONYMOUS_CONSUMER'] = 'true'
    else:
        headers['HTTP_X_AUTHENTICATED_USERID'] = str(user_id)
    return headers

def create_mock_communication_template(owner_id=1, slug='TEST_TEST'):

    tmplt = CommunicationTemplate()
    tmplt.owner = owner_id
    tmplt.slug = slug
    tmplt.subject = 'Subject: {{foo}}'
    tmplt.short_message = 'Short message: {{foo}}'
    tmplt.message = 'Message: {{foo}}'
    tmplt.schema = MOCK_SCHEMA
    tmplt.save()
    return tmplt

def create_templated_communication(template_slug, owner_id, context = None):
    if context is None:
        context = { "foo": "bar" }
    comm = Communication()
    comm.owner = owner_id
    comm.template_slug = template_slug
    comm.context = context
    comm.save()
    return comm
