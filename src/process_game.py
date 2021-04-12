  
import os
import gzip
import json
from carball.decompile_replays import decompile_replay
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager

def analyzeGame(fname):
  _json = decompile_replay(fname)
  game = Game()
  game.initialize(loaded_json=_json)
  analysis_manager = AnalysisManager(game)
  analysis_manager.create_analysis(calculate_intensive_events=True)
  return analysis_manager.get_json_data()

#
if __name__=='__main__':
  pass