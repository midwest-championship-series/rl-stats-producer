import json
from src.process_game import analyzeGame
import boto3
from urllib.parse import unquote_plus
import os
from src.services import error_handling
import sys

# from aws_creds import creds


def handler(event, context):
    # event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2021-03-25T00:39:03.433Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDA2DYXBXAXXAFD2TJH3'}, 'requestParameters': {'sourceIPAddress': '75.73.213.19'}, 'responseElements': {'x-amz-request-id': 'BEKX43TT19XYN1CB', 'x-amz-id-2': 'sXxOIepH8ejqoiKz8Qb5lbMscV57ZBxCUV5uO3Syvj7G0ywnsgdaS0/H0B0fGuWdckAnHmGMWnVoTpduFOl/THRDY5a4GA6k'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'e4bc8b8a-1e86-4ee4-a1d6-28996b60c581', 'bucket': {'name': 'rl-stats-producer-replays-dev-us-east-1', 'ownerIdentity': {'principalId': 'A206CTAY98T2VV'}, 'arn': 'arn:aws:s3:::rl-stats-producer-replays-dev-us-east-1'}, 'object': {'key': '2B3722BD4096D3C365D7F1A6447F93F3.replay', 'size': 1434824, 'eTag': '2be639155cecfc08203cb176cd3f7fb6', 'sequencer': '00605BDBAA9E643E9B'}}}]}
    # aws_access_key_id = creds.get("aws_access_key_id")
    # aws_secret_access_key = creds.get("aws_secret_access_key")
    # region_name = creds.get("region_name")
    replay_bucket = os.environ.get("REPLAY_BUCKET", None)
    event_bucket = os.environ.get("EVENT_STATS_BUCKET", None)

    s3_client = boto3.client('s3')

    key = event['Records'][0]['s3']['object']['key']
    key = unquote_plus(key, encoding='utf-8')
    s3_client.download_file(replay_bucket, key, f"/tmp/curr_replay_{key}")
    try:
        gameData = analyzeGame(fname=f"/tmp/curr_replay_{key}")

    except:
        if os.path.exists(f"/tmp/curr_replay_{key}"):
            os.remove(f"/tmp/curr_replay_{key}")

        if os.path.exists(f'/tmp/output.json'):
            os.remove(f'/tmp/output.json')

        try:
            bot_url = os.environ.get('RL_BOT_URL', None)
            channel_id = os.environ.get('ERROR_CHANNEL_ID', None)
            request_url = f"{bot_url}/api/v1/channels/{channel_id}"
            error_msg = {
                "message": f"context: analyzeGame failure\nerror: {sys.exc_info()[0]}"
            }
            error_handling.send_message_via_bot(url=request_url, message=error_msg)

        except (ValueError) as e:
            raise ValueError(f'Failed to make a successful call to the '
                             f'RL_BOT: {e}')

        except:
            raise ValueError(f'Failed to make a successful call to the '
                             f'RL_BOT: {sys.exc_info()[0]}')

        return

    else:
        if gameData:
            if event_bucket is not None:
                print(gameData.keys())
                s3_client.put_object(
                    Bucket=event_bucket,
                    Key=f'{gameData["gameMetadata"]["matchGuid"]}.json',
                    ACL='private',
                    Body=json.dumps(gameData)
                )

        if os.path.exists(f"/tmp/curr_replay_{key}"):
            os.remove(f"/tmp/curr_replay_{key}")

        return

# to test the output of the json, from the file object in the s3 bucket
# def read_file_contents(fname=None):

    # define `creds` as a dictionary object in the ./aws_creds.py file
    # aws_access_key_id = creds.get("aws_access_key_id")
    # aws_secret_access_key = creds.get("aws_secret_access_key")
    # region_name = creds.get("region_name")
    #
    # s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
    #                          region_name=region_name)
    # bucket_name = "rl-stats-producer-replays-dev-us-east-1"
    # key = "analysis_2B3722BD4096D3C365D7F1A6447F93F3.json"
    # response = s3_client.get_object(Bucket=bucket_name,Key=key)

    # print(json.loads(response["Body"].read()))


if __name__ == "__main__":
    handler(None, None)
    # read_file_contents('example.json')