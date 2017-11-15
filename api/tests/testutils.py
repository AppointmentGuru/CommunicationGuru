# from faker import Factory
# FAKE = Factory.create()

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
