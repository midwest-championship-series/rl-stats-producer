import json
from src.process_game import analyzeGame
import boto3
import os
from src.services import error_handling
import sys

# from aws_creds import creds


def handler(event, context):
    event_bucket = os.environ.get("EVENT_STATS_BUCKET", None)
    s3_client = boto3.client('s3')

    for replay in event['detail']['replays']:
        key = replay['bucket']['key']
        replay_bucket = replay['bucket']['source']
        print(key)
        print(replay_bucket)
        print('beginning download')

        s3_client.download_file(replay_bucket, key, f"/tmp/curr_replay_{key}")

        try:
            print('beginning analysis')
            gameData = analyzeGame(fname=f"/tmp/curr_replay_{key}")

        except:
            if os.path.exists(f"/tmp/curr_replay_{key}"):
                os.remove(f"/tmp/curr_replay_{key}")

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
                    print(f"uploading {key}")
                    s3_client.put_object(
                        Bucket=event_bucket,
                        Key=f"{key.split('.replay')[0]}.json",
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