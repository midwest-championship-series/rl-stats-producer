import json
from src.process_game import analyzeGame
import boto3
import os
from src.services import rl_bot, rl_platform
import sys

event_bucket = os.environ.get("EVENT_STATS_BUCKET", None)
s3_client = boto3.client('s3')


def handler(event, context):
    parsed_replays = []
    for replay in event.get('detail', {}).get('replays', []):
        try:
            key = replay.get('bucket').get('key')
            replay_bucket = replay.get('bucket').get('source')

            s3_client.download_file(replay_bucket, key, f"/tmp/curr_replay_{key}")

            print('beginning analysis')
            gameData = analyzeGame(fname=f"/tmp/curr_replay_{key}")

        except:
            if os.path.exists(f"/tmp/curr_replay_{key}"):
                os.remove(f"/tmp/curr_replay_{key}")

            try:
                e_key, e_value, e_traceback = sys.exc_info()
                rl_bot.send_error_to_channel(
                    context=f'parsing replay: {key} from location: {replay_bucket}',
                    error={
                        "key": e_key,
                        "value": e_value,
                        "traceback": {
                            "frame": e_traceback.tb_frame,
                            "tb_lineno": e_traceback.tb_lineno
                        }
                    }
                )

            except (ValueError) as e:
                raise ValueError(f'Failed to make a successful call to the '
                                 f'RL_BOT: {e}')

            except:
                raise ValueError(f'Failed to make a successful call to the '
                                 f'RL_BOT: {sys.exc_info()[0]}')

            return

        else:
            if event_bucket is not None:
                print(f"uploading {key}")
                output_key=f"{key.split('.replay')[0]}.json"
                s3_client.put_object(
                    Bucket=event_bucket,
                    Key=output_key,
                    ACL='private',
                    Body=json.dumps(gameData)
                )
                parsed_replays.append({
                    'id': replay.get('id'),
                    'upload_source': replay.get('upload_source'),
                    'bucket': {
                        'key': output_key,
                        'source': event_bucket
                    }
                })

            if os.path.exists(f"/tmp/curr_replay_{key}"):
                os.remove(f"/tmp/curr_replay_{key}")
    process_end_event = {
        'type': 'MATCH_PROCESS_REPLAYS_PARSED',
        'detail': {
            'league_id': event.get('detail').get('league_id'),
            'reply_to_channel': event.get('detail').get('reply_to_channel'),
            'parsed_replays': parsed_replays
        }
    }
    rl_platform.send_event(process_end_event)

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