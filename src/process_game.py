import sys

from carball.decompile_replays import analyze_replay_file, decompile_replay
from carball.json_parser.game import Game
import logging
from src.services.rl_bot import send_error_to_channel, send_message_to_channel


def analyzeGame(fname):
    _json = decompile_replay(fname)
    all_players = extract_players(obj=_json)
    game = Game()
    game.initialize(loaded_json=_json)

    # the calculate_intensive_stats is causing the issue!!!! I was able to track it down!
    analysis = analyze_replay_file(replay_path=fname, logging_level=logging.DEBUG, clean=True).get_json_data()

    keepers = []
    for player in analysis.get('players', []):
        name = player.get('name')
        score = player.get('score')
        if score > 0:
            keepers.append(name)

    for player in all_players:
        if player['name'] not in keepers:
            all_players.remove(player)

    return all_players, analysis


def extract_players(obj):
    all_players = []
    try:
        network_frames = obj['network_frames']
        all_frames = network_frames['frames']
        frame = all_frames[0]
        updated_actors = frame['updated_actors']
        for actor in updated_actors:
            if actor.get('attribute', None) is not None and \
                actor.get('attribute', {}).get('Reservation', None) is not None:
                player_info = actor['attribute']['Reservation']
                name = player_info['name']
                unique_id = player_info['unique_id']
                remote_id = unique_id['remote_id']
                platform, pid = list(remote_id.items())[0]
                all_players.append({'name': name, 'platform': platform, 'platform_id': pid})
                continue

    except:
        return send_error_to_channel(context="FAILED TO PARSE REPLAY AND EXTRACT PLAYERS", error=sys.exc_info()[0])

    return all_players



# if __name__ == '__main__':
    # players, replay_json = analyzeGame("/Users/andrewray/Documents/Programming/Python/rl-stats-producer/example.replay")
