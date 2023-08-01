import sys
import os
import pathlib
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from tools.Mythril import Mythril
from tools.Slither import *
dataPath = pathlib.Path(__file__).parent.resolve()

(final, raw) = Mythril.analyze(
    r'D:\SE_LAB\SE_Task\blockchain\tool\test-mythril\bugs',
    'swc-107.sol'
)

try:  
    with open('./tools/results/slither/raw_slither.json') as raw_slither_json:
        raw_json = json.load(raw_slither_json)
        print(type(raw_json))
    (final, raw) = Slither.analyze(
        dataPath, 'raw_slither.json'
    )
except FileNotFoundError:
    print("Error: File not found.")
except json.JSONDecodeError:
    print("Error: Unable to parse JSON.")
except Exception as e:
    print(f"Error: {e}")
Mythril.export_result('swc-107.sol', raw, final)
