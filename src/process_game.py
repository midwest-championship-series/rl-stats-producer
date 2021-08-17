import sys

from carball.decompile_replays import analyze_replay_file, decompile_replay
from carball.json_parser.game import Game
import logging
from src.services.rl_bot import send_error_to_channel, send_message_to_channel

import json


def analyzeGame(fname):
    _json = decompile_replay(fname)
    all_players = extract_players(obj=_json)
    game = Game()
    game.initialize(loaded_json=_json)

    # the calculate_intensive_stats is causing the issue!!!! I was able to track it down!
    analysis = analyze_replay_file(replay_path=fname, logging_level=logging.DEBUG, clean=True).get_json_data()

    for player in analysis.get('players', [{}]):
        name = player['name']
        score = player['score']
        goals = player['goals']
        assists = player['assists']
        saves = player['saves']
        shots = player['shots']
        if all_players.get((name, assists, goals, saves, score, shots), None) is not None:
            player['id']['platform'] = all_players[(name, assists, goals, saves, score, shots)]['platform']

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

    except:
        return send_error_to_channel(context="FAILED TO PARSE REPLAY AND EXTRACT PLAYERS", error=sys.exc_info()[0])

    return all_players


if __name__ == '__main__':
    replay_json = analyzeGame("/Users/andrewray/Documents/GitHub/rl-stats-producer/epic_steam_replay.replay")
    # print(replay_json)