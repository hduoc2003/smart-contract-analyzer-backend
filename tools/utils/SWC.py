import re

swc_regex: dict[str, str] = {
    "only_number": r"^(1[0-2]\d|13[0-6])$",
    "full": r"^[sS][wW][cC]-(1[0-2]\d|13[0-6])$"
}
map_check_to_issue: dict[str, str] = {
   'abiencoderv2-array': 'storage-abiencoderv2-array',
   'arbitrary-send-erc20': 'arbitrary-from-in-transferfrom',
   'array-by-reference': 'modifying-storage-array-by-value',
   'encode-packed-collision': 'abi-encodepacked-collision',
   'incorrect-shift': 'incorrect-shift-in-assembly.',
   'multiple-constructors': 'multiple-constructor-schemes',
   'name-reused': 'name-reused',
   'protected-vars': 'protected-variables',
   'public-mappings-nested': 'public-mappings-with-nested-variables',
   'rtlo': 'right-to-left-override-character',
   'shadowing-state': 'state-variable-shadowing',
   'suicidal': 'suicidal',
   'uninitialized-state': 'uninitialized-state-variables',
   'uninitialized-storage': 'uninitialized-storage-variables',
   'unprotected-upgrade': 'unprotected-upgradeable-contract',
   'arbitrary-send-erc20-permit': 'arbitrary-from-in-transferfrom-used-with-permit',
   'arbitrary-send-eth': 'functions-that-send-ether-to-arbitrary-destinations',
   'controlled-array-length': 'array-length-assignment',
   'controlled-delegatecall': 'controlled-delegatecall',
   'delegatecall-loop': 'payable-functions-using-delegatecall-inside-a-loop',
   'msg-value-loop': 'msg.value-inside-a-loop',
   'reentrancy-unlimited-gas': 'reentrancy-vulnerabilities',
   'storage-array': 'storage-signed-integer-array',
   'unchecked-transfer': 'unchecked-transfer',
   'weak-prng': 'weak-prng',
   'codex': 'codex',
   'domain-separator-collision': 'domain-separator-collision',
   'enum-conversion': 'dangerous-enum-conversion',
   'erc20-interface': 'incorrect-erc20-interface',
   'erc721-interface': 'incorrect-erc721-interface',
   'incorrect-equality': 'dangerous-strict-equalities',
   'locked-ether': 'contracts-that-lock-ether',
   'mapping-deletion': 'deletion-on-mapping-containing-a-structure',
   'shadowing-abstract': 'state-variable-shadowing-from-abstract-contracts',
   'tautology': 'tautology-or-contradiction',
   'write-after-write': 'write-after-write',
   'boolean-cst': 'misuse-of-a-boolean-constant',
   'constant-function-asm': 'constant-functions-using-assembly-code',
   'constant-function-state': 'constant-functions-changing-the-state',
   'divide-before-multiply': 'divide-before-multiply',
   'reused-constructor': 'reused-base-constructors',
   'tx-origin': 'dangerous-usage-of-tx.origin',
   'unchecked-lowlevel': 'unchecked-low-level-calls',
   'unchecked-send': 'unchecked-send',
   'uninitialized-local': 'uninitialized-local-variables',
   'unused-return': 'unused-return',
   'incorrect-modifier': 'incorrect-modifier',
   'shadowing-builtin': 'builtin-symbol-shadowing',
   'shadowing-local': 'local-variable-shadowing',
   'uninitialized-fptr-cst': 'uninitialized-function-pointers-in-constructors',
   'variable-scope': 'pre-declaration-usage-of-local-variables',
   'void-cst': 'void-constructor',
   'calls-loop': 'calls-inside-a-loop',
   'events-access': 'missing-events-access-control',
   'events-maths': 'missing-events-arithmetic',
   'incorrect-unary': 'dangerous-unary-expressions',
   'missing-zero-check': 'missing-zero-address-validation',
   'timestamp': 'block-timestamp',
   'assembly': 'assembly-usage',
   'assert-state-change': 'assert-state-change',
   'boolean-equal': 'boolean-equality',
   'cyclomatic-complexity': 'cyclomatic-complexity',
   'deprecated-standards': 'deprecated-standards',
   'erc20-indexed': 'unindexed-erc20-event-parameters',
   'function-init-state': 'function-initializing-state',
   'incorrect-using-for': 'incorrect-usage-of-using-for-statement',
   'low-level-calls': 'low-level-calls',
   'missing-inheritance': 'missing-inheritance',
   'naming-convention': 'conformance-to-solidity-naming-conventions',
   'pragma': 'different-pragma-directives-are-used',
   'redundant-statements': 'redundant-statements',
   'solc-version': 'incorrect-versions-of-solidity',
   'unimplemented-functions': 'unimplemented-functions',
   'unused-state': 'unused-state-variable',
   'costly-loop': 'costly-operations-inside-a-loop',
   'dead-code': 'dead-code',
   'similar-names': 'variable-names-too-similar',
   'too-many-digits': 'too-many-digits',
   'cache-array-length': 'cache-array-length',
   'constable-states': 'state-variables-that-could-be-declared-constant',
   'external-function': 'public-function-that-could-be-declared-external',
   'immutable-states': 'state-variables-that-could-be-declared-immutable',
   'var-read-using-this': 'public-variable-read-in-external-context',
}
map_slither_check_to_swc: dict[str, str] = {
  "abiencoderv2-array": "N/A",
  "arbitrary-send-erc20": "N/A",
  "array-by-reference": "N/A",
  "encode-packed-collision": "SWC-133",
  "incorrect-shift": "N/A",
  "multiple-constructors": "SWC-118",
  "name-reused": "N/A",
  "protected-vars": "N/A",
  "public-mappings-nested": "N/A",
  "rtlo": "SWC-130",
  "shadowing-state": "SWC-119",
  "suicidal": "SWC-106",
  "uninitialized-state": "N/A",
  "uninitialized-storage": "SWC-109",
  "unprotected-upgrade": "N/A",
  "codex": "N/A",
  "arbitrary-send-erc20-permit": "N/A",
  "arbitrary-send-eth": "N/A",
  "controlled-array-length": "N/A",
  "controlled-delegatecall": "SWC-112",
  "delegatecall-loop": "N/A",
  "msg-value-loop": "N/A",
  "reentrancy-eth": "SWC-107",
  "storage-array": "N/A",
  "unchecked-transfer": "N/A",
  "weak-prng": "SWC-120",
  "domain-separator-collision": "N/A",
  "enum-conversion": "N/A",
  "erc20-interface": "N/A",
  "erc721-interface": "N/A",
  "incorrect-equality": "SWC-132",
  "locked-ether": "N/A",
  "mapping-deletion": "N/A",
  "shadowing-abstract": "SWC-119",
  "tautology": "N/A",
  "write-after-write": "SWC-135",
  "boolean-cst": "N/A",
  "constant-function-asm": "N/A",
  "constant-function-state": "N/A",
  "divide-before-multiply": "N/A",
  "reentrancy-no-eth": "SWC-107",
  "reused-constructor": "N/A",
  "tx-origin": "SWC-115",
  "unchecked-lowlevel": "N/A",
  "unchecked-send": "N/A",
  "uninitialized-local": "N/A",
  "unused-return": "SWC-135",
  "incorrect-modifier": "N/A",
  "shadowing-builtin": "SWC-119",
  "shadowing-local": "SWC-119",
  "uninitialized-fptr-cst": "N/A",
  "variable-scope": "N/A",
  "void-cst": "N/A",
  "calls-loop": "N/A",
  "events-access": "N/A",
  "events-maths": "N/A",
  "incorrect-unary": "SWC-129",
  "missing-zero-check": "N/A",
  "reentrancy-benign": "SWC-107",
  "reentrancy-events": "SWC-107",
  "timestamp": "SWC-116",
  "assembly": "SWC-127",
  "assert-state-change": "SWC-110",
  "boolean-equal": "N/A",
  "cyclomatic-complexity": "N/A",
  "deprecated-standards": "SWC-111",
  "erc20-indexed": "N/A",
  "function-init-state": "N/A",
  "incorrect-using-for": "SWC-135",
  "low-level-calls": "N/A",
  "missing-inheritance": "N/A",
  "naming-convention": "N/A",
  "pragma": "SWC-103",
  "redundant-statements": "SWC-135",
  "solc-version": "SWC-102",
  "unimplemented-functions": "N/A",
  "unused-state": "SWC-131",
  "costly-loop": "N/A",
  "dead-code": "N/A",
  "reentrancy-unlimited-gas": "SWC-134",
  "similar-names": "N/A",
  "too-many-digits": "N/A",
  "cache-array-length": "N/A",
  "constable-states": "N/A",
  "external-function": "N/A",
  "immutable-states": "N/A",
  "var-read-using-this": "N/A"
}
map_to_swc_title: dict[str, str] = {
  'SWC-100': 'Function Default Visibility',
  'SWC-101': 'Integer Overflow and Underflow',
  'SWC-102': 'Outdated Compiler Version',
  'SWC-103': 'Floating Pragma',
  'SWC-104': 'Unchecked Call Return Value',
  'SWC-105': 'Unprotected Ether Withdrawal',
  'SWC-106': 'Unprotected SELFDESTRUCT Instruction',
  'SWC-107': 'Reentrancy',
  'SWC-108': 'State Variable Default Visibility',
  'SWC-109': 'Uninitialized Storage Pointer',
  'SWC-110': 'Assert Violation',
  'SWC-111': 'Use of Deprecated Solidity Functions',
  'SWC-112': 'Delegatecall to Untrusted Callee',
  'SWC-113': 'DoS with Failed Call',
  'SWC-114': 'Transaction Order Dependence',
  'SWC-115': 'Authorization through tx.origin',
  'SWC-116': 'Block values as a proxy for time',
  'SWC-117': 'Signature Malleability',
  'SWC-118': 'Incorrect Constructor Name',
  'SWC-119': 'Shadowing State Variables',
  'SWC-120': 'Weak Sources of Randomness from Chain Attributes',
  'SWC-121': 'Missing Protection against Signature Replay Attacks',
  'SWC-122': 'Lack of Proper Signature Verification',
  'SWC-123': 'Requirement Violation',
  'SWC-124': 'Write to Arbitrary Storage Location',
  'SWC-125': 'Incorrect Inheritance Order',
  'SWC-126': 'Insufficient Gas Griefing',
  'SWC-127': 'Arbitrary Jump with Function Type Variable',
  'SWC-128': 'DoS With Block Gas Limit',
  'SWC-129': 'Typographical Error',
  'SWC-130': 'Right-To-Left-Override control character (U+202E)',
  'SWC-131': 'Presence of unused variables',
  'SWC-132': 'Unexpected Ether balance',
  'SWC-133': 'Hash Collisions With Multiple Variable Length Arguments',
  'SWC-134': 'Message call with hardcoded gas amount',
  'SWC-135': 'Code With No Effects',
  'SWC-136': 'Unencrypted Private Data On-Chain',
  'N/A' : 'N/A'
}

def get_swc_no(check: str) -> str:
    if map_slither_check_to_swc[check] != 'N/A':
        return map_slither_check_to_swc[check]
    return 'N/A'

def link_hint(check: str) -> str:
    url = "https://github.com/crytic/slither/wiki/Detector-Documentation"
    return map_check_to_issue[check]

def valid_swc(swc: str) -> tuple[bool, str]:
    """kiểm tra và lấy định dạng swc chuẩn

    Args:
        swc (str): _description_

    Returns:
        tuple[bool, str]: _description_
    """
    if (re.match(swc_regex['only_number'], swc)):
        return (True, "SWC-"+swc)
    if (re.match(swc_regex['full'], swc)):
        return (True, swc.upper())
    return (False, f"{swc} is not a valid SWC, see more details https://swcregistry.io/")


def get_swc_link(swc: str, validated: bool = False) -> str:
    if (swc == 'N/A'):
        return "N/A"
    if (validated or valid_swc(swc)[0]):
        return f'https://swcregistry.io/docs/{swc.upper()}/'
    raise Exception(f"{swc} is not a valid SWC, see more details https://swcregistry.io/")

def get_swc_title(swc: str, validated: bool = False) -> str:
    if (swc == 'N/A'):
        return "N/A"
    if (validated or valid_swc(swc)[0]):
        return map_to_swc_title[swc.upper()]
    raise Exception(f"{swc} is not a valid SWC, see more details https://swcregistry.io/")
