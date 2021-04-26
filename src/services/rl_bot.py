import requests
import json
import os

bot_url = os.environ.get('RL_BOT_URL', None)
error_channel_id = os.environ.get('ERROR_CHANNEL_ID', None)

def send_message_to_channel(channel_id, message):
    headers = {
        "Content-Type": "application/json"
    }
    request_url = f"{bot_url}/api/v1/channels/{channel_id}"
    body = {
        'message': message
    }
    response = requests.post(url=request_url, data=json.dumps(body), headers=headers)

    if response.status_code != 200:
        raise ValueError(f'Received a non-200 response code from the call to the RL BOT: {response.status_code}')

def send_error_to_channel(context=None, error=None):
    if context is None:
        context = 'INTERNAL SERVICE ERROR'
    if error is None:
        error = 'An unknown error has occured, check logs for further assistance.'
    message = f'context: {context}\nError: {error}'
    return send_message_to_channel(error_channel_id, message)
