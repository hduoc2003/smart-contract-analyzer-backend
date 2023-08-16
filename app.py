import sys
import os
import pathlib
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from tools.Mythril import Mythril
from tools.Slither import *
dataPath = pathlib.Path(__file__).parent.resolve()

# (final, raw) = Mythril.analyze(
#     r'D:\University\Laboratory\Blockchain\Tool Intergrating\ReBuild\BE\tools\data\SWC-107',
#     'transaction_malleablity.sol'
# )

(final, raw) = Slither.analyze(
    r'D:\University\Laboratory\Blockchain\Tool Intergrating\ReBuild\BE\tools\data\SWC-117',
    'transaction_malleablity.sol'
)
Slither.export_result('swc-117.sol', raw, final)
