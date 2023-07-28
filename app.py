import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from tools.Mythril import Mythril

(final, raw) = Mythril.analyze(
    r'D:\SE_LAB\SE_Task\blockchain\tool\test-mythril\bugs',
    'swc-107.sol'
)

Mythril.export_result('swc-107.sol', raw, final)
