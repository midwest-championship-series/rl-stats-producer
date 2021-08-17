import sys

from carball.decompile_replays import analyze_replay_file, decompile_replay
from carball.json_parser.game import Game
import logging


def analyze_game(fname):
    _json = decompile_replay(fname)
    try:
        all_players = extract_players(obj=_json)

    except (KeyError, AttributeError, ValueError, TypeError) as e:
        print('failed to extract the player properties from within the _json variable.')
        raise e

    game = Game()
    game.initialize(loaded_json=_json)

    # the calculate_intensive_stats is causing the issue!!!! I was able to track it down!
    analysis = analyze_replay_file(replay_path=fname, logging_level=logging.DEBUG, clean=True).get_json_data()

    try:
        for player in analysis.get('players', [{}]):
            name = player['name']
            score = player['score']
            goals = player['goals']
            assists = player['assists']
            saves = player['saves']
            shots = player['shots']
            if all_players.get((name, assists, goals, saves, score, shots), None) is not None:
                player['id']['platform'] = all_players[(name, assists, goals, saves, score, shots)]['platform']

    except (KeyError, AttributeError, ValueError, TypeError) as e:
        print('failed to extract the players objects from within the analysis variable.')
        raise e

    return analysis


def extract_players(obj):
    all_players = {}
    try:
        properties = obj['properties']
        for player in properties['PlayerStats']:
            assists = player['Assists']
            goals = player['Goals']
            saves = player['Saves']
            score = player['Score']
            shots = player['Shots']

            name = player['Name']
            platform = player['Platform']['value'].split('_')[1]
            online_id = player['OnlineID']
            all_players[(name, assists, goals, saves, score, shots)] = {'online_id': online_id, 'platform': platform}

    except (KeyError, AttributeError, ValueError, TypeError) as e:
        raise e

    return all_players


if __name__ == '__main__':
    replay_json = analyze_game("/Users/andrewray/Documents/GitHub/rl-stats-producer/epic_steam_replay.replay")
    # print(replay_json)