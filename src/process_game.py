  
import os
import gzip
import json
from carball.decompile_replays import decompile_replay
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager

from datetime import datetime

# def analyzeGame():
  # return carball.decompile_replay('example.replay')
def analyzeGame(fname):
  _json = decompile_replay(f"{os.getcwd()}/{fname}")
  game = Game()
  game.initialize(loaded_json=_json)
  analysis_manager = AnalysisManager(game)
  analysis_manager.create_analysis(calculate_intensive_events=True)
  analysis_manager.write_json_out_to_file(open(f'{os.getcwd()}/analysis_{fname.split(".replay")[0]}.json', 'w'))
  with gzip.open(os.path.join('output.gzip'), 'wb') as fo:
    analysis_manager.write_pandas_out_to_file(fo)
  return _json


if __name__=='__main__':
  analyzeGame()