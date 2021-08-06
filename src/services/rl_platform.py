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
	if response.status_code != 200:
		raise ValueError(f'Received a non-200 response code from the call to the RL platform: {response.status_code}')

	return response
