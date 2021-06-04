def hello_world(request):
    import json
    import os 
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request_json and 'passcode' in request_json:
        if request_json['passcode'] == os.environ.get('PASSCODE'):
            status = "OK"
            if request_json and 'message' in request_json:
                message = request_json['message']
            else:
                message = "Empty Message"
        else: 
            status = "FAIL"
            message = "Wrong Passcode"

    out = {'status': status, 'message': message}
    headers= {
        'Access-Control-Allow-Origin': '*',
        'Content-Type':'application/json'
        }
    return (json.dumps(out), 200, headers)