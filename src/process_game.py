  
import os
import gzip
import json
from carball.decompile_replays import decompile_replay
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager

def analyzeGame(fname):
  # _json = decompile_replay(f"/tmp/curr_replay_{fname}")
  _json = decompile_replay(fname)
  game = Game()
  game.initialize(loaded_json=_json)
  analysis_manager = AnalysisManager(game)
  analysis_manager.create_analysis(calculate_intensive_events=True)
  with gzip.open(os.path.join('/tmp/output.json'), 'wb') as fo:
    fo.write(analysis_manager.get_json_data())
  # analysis_manager.write_json_out_to_file(open(f'/tmp/analysis_curr_replay_{fname.split(".")[0]}.json', 'w'))
  # with gzip.open(os.path.join('/tmp/output.gzip'), 'wb') as fo:
  #   return analysis_manager.get_json_data(fo)
  #
  # return _json

#
if __name__=='__main__':
  pass