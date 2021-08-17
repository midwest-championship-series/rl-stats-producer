import json
from src.process_game import analyze_game
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
            gameData = analyze_game(fname=f"/tmp/curr_replay_{key}")

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

            except ValueError as e:
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
                    'bucket': {
                        'key': output_key,
                        'source': event_bucket
                    }
                })

            if os.path.exists(f"/tmp/curr_replay_{key}"):
                os.remove(f"/tmp/curr_replay_{key}")
    detail = {
        'parsed_replays': parsed_replays
    }
    for property, value in event.get('detail').items():
        if property in ['league_id', 'match_id', 'reply_to_channel']:
            detail[property] = value
    process_end_event = {
        'type': 'MATCH_PROCESS_REPLAYS_PARSED',
        'detail': detail
    }
    rl_platform.send_event(process_end_event)

    return


if __name__ == "__main__":
    handler(None, None)
    # read_file_contents('example.json')