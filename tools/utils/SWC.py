import re

swc_regex: dict[str, str] = {
    "only_number": r"^(1[0-2]\d|13[0-6])$",
    "full": r"^[sS][wW][cC]-(1[0-2]\d|13[0-6])$"
}

map_slither_detectors_to_swc: dict[str, str] = {
    'abiencoderv2-array': 'SWC',
    'arbitrary-send-erc20': 'SWC',
    'shadowing-state': 'SWC-119'
    ''
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
  'SWC-136': 'Unencrypted Private Data On-Chain'
}



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
    if (validated or valid_swc(swc)[0]):
        return f'https://swcregistry.io/docs/{swc.upper()}/'
    raise Exception(f"{swc} is not a valid SWC, see more details https://swcregistry.io/")

def get_swc_title(swc: str, validated: bool = False) -> str:
    if (validated or valid_swc(swc)[0]):
        return map_to_swc_title[swc.upper()]
    raise Exception(f"{swc} is not a valid SWC, see more details https://swcregistry.io/")
