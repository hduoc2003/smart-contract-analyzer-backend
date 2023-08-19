(final, raw) = Slither.analyze(
    r'D:\University\Laboratory\Blockchain\Tool Intergrating\ReBuild\BE\tools\data\SWC-117',
    'transaction_malleablity.sol'
)
Slither.export_result('swc-117.sol', raw, final)
