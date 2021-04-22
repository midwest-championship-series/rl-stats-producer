import requests
import json

def send_message_via_bot(url, message=None):
    if message is None:
        message = {
            "message": "context: INTERNAL SERVICE ERROR\nError: An unknown error has occured, check logs for "
                       "further assistance."
        }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url=url, data=json.dumps(message), headers=headers)

    if response.status_code != 200:
        raise ValueError(f'Received a non-200 response code from the call to the RL BOT: {response.status_code}')
