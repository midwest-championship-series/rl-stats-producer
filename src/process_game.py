from carball.decompile_replays import analyze_replay_file


def analyzeGame(fname):
    analysis = analyze_replay_file(replay_path=fname, calculate_intensive_events=True, clean=True)
    return analysis.get_json_data()


#
if __name__ == '__main__':
    pass