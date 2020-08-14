import json
from src.process_game import analyzeGame
# import numpy as np

def handler(event, context):
    # a = np.arange(15).reshape(3, 5)

    # print("Your numpy array:")
    # print(a)

    gameData = analyzeGame()

    # print(gameData.keys())

    # response = {
    #     "statusCode": 200,
    #     "body": {
    #         "success": True,
    #         "length": len(json.dumps(gameData))
    #     }
    #     # "body": json.dumps(a)
    # }
    # print(response)
    # return response
    jsonData = json.dumps(gameData)
    # print(jsonData)
    return jsonData

if __name__ == "__main__":
    handler(None, None)