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
