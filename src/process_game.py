  
import os
import gzip
import json
from carball.decompile_replays import decompile_replay
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager

# def analyzeGame():
  # return carball.decompile_replay('example.replay')
def analyzeGame(fname):
  _json = decompile_replay(f"/tmp/curr_replay")
  game = Game()
  game.initialize(loaded_json=_json)
  analysis_manager = AnalysisManager(game)
  analysis_manager.create_analysis(calculate_intensive_events=True)
  analysis_manager.write_json_out_to_file(open(f'/tmp/analysis_curr_replay.json', 'w'))
  with gzip.open(os.path.join('/tmp/output.gzip'), 'wb') as fo:
    analysis_manager.write_pandas_out_to_file(fo)
  return _json

#
# if __name__=='__main__':
  # analyzeGame()