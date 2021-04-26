import os
import requests
import json

api_key = os.environ.get('RL_PLATFORM_API_KEY', None)
platform_url = os.environ.get('RL_PLATFORM_URL', None)

def send_event(event):
	headers = {
        "Content-Type": "application/json",
		"x-api-key": api_key
    }
	request_url = f'{platform_url}/v2/events'
	response = requests.post(url=request_url, data=json.dumps(event), headers=headers)
	return response