import re

swc_regex: dict[str, str] = {
    "only_number": r"^(1[0-2]\d|13[0-6])$",
    "full": r"^[sS][wW][cC]-(1[0-2]\d|13[0-6])$"
}

map_slither_detectors_to_swc: dict[str, dict[str, str]] = {
  "abiencoderv2-array": {
    "description": "solc versions 0.4.7-0.5.9 contain a compiler bug leading to incorrect ABI encoder usage.",
    "swc": "SWC"
  },
  "arbitrary-send-erc20": {
    "description": "Detect when msg.sender is not used as from in transferFrom.",
    "swc": "SWC"
  },
  "array-by-reference": {
    "description": "Detect arrays passed to a function that expects reference to a storage array",
    "swc": "SWC"
  },
  "encode-packed-collision": {
    "description": "Detect collision due to dynamic type usages in abi.encodePacked",
    "swc": "SWC"
  },
  "incorrect-shift": {
    "description": "Detect if the values in a shift operation are reversed",
    "swc": "SWC"
  },
  "multiple-constructors": {
    "description": "Detect multiple constructor definitions in the same contract (using new and old schemes).",
    "swc": "SWC"
  },
  "name-reused": {
    "description": "If a codebase has two contracts the similar names, the compilation artifactswill not contain one of the contracts with the duplicate name.",
    "swc": "SWC"
  },
  "protected-vars": {
    "description": "Detect unprotected variable that are marked protected",
    "swc": "SWC"
  },
  "public-mappings-nested": {
    "description": "Prior to Solidity 0.5, a public mapping with nested structures returned incorrect values.",
    "swc": "SWC"
  },
  "rtlo": {
    "description": "An attacker can manipulate the logic of the contract by using a right-to-left-override character (U+202E).",
    "swc": "SWC"
  },
  "shadowing-state": {
    "description": "Detection of state variables shadowed.",
    "swc": "SWC"
  },
  "suicidal": {
    "description": "Unprotected call to a function executing selfdestruct/suicide.",
    "swc": "SWC"
  },
  "uninitialized-state": {
    "description": "Uninitialized state variables.",
    "swc": "SWC"
  },
  "uninitialized-storage": {
    "description": "An uninitialized storage variable will act as a reference to the first state variable, and can override a critical variable.",
    "swc": "SWC"
  },
  "unprotected-upgrade": {
    "description": "Detects logic contract that can be destructed.",
    "swc": "SWC"
  },
  "codex": {
    "description": "Detect when msg.sender is not used as from in transferFrom and permit is used.",
    "swc": "SWC"
  },
  "arbitrary-send-erc20-permit": {
    "description": "Unprotected call to a function sending Ether to an arbitrary address.",
    "swc": "SWC"
  },
  "arbitrary-send-eth": {
    "description": "Detects the direct assignment of an array's length.",
    "swc": "SWC"
  },
  "controlled-array-length": {
    "description": "Delegatecall or callcode to an address controlled by the user.",
    "swc": "SWC"
  },
  "controlled-delegatecall": {
    "description": "Detect the use of delegatecall inside a loop in a payable function.",
    "swc": "SWC"
  },
  "delegatecall-loop": {
    "description": "Detect the use of msg.value inside a loop.",
    "swc": "SWC"
  },
  "msg-value-loop": {
    "description": "Detection of the reentrancy bug.Do not report reentrancies that don't involve Ether (see reentrancy-no-eth)",
    "swc": "SWC"
  },
  "reentrancy-eth": {
    "description": "solc versions 0.4.7-0.5.9 contain a compiler bugleading to incorrect values in signed integer arrays.",
    "swc": "SWC"
  },
  "storage-array": {
    "description": "The return value of an external transfer/transferFrom call is not checked",
    "swc": "SWC"
  },
  "unchecked-transfer": {
    "description": "Weak PRNG due to a modulo on block.timestamp, now or blockhash. These can be influenced by miners to some extent so they should be avoided.",
    "swc": "SWC"
  },
  "weak-prng": {
    "description": "Use codex to find vulnerabilities",
    "swc": "SWC"
  },
  "domain-separator-collision": {
    "description": "An ERC20 token has a function whose signature collides with EIP-2612's DOMAIN_SEPARATOR(), causing unanticipated behavior for contracts using permit functionality.",
    "swc": "SWC"
  },
  "enum-conversion": {
    "description": "Detect out-of-range enum conversion (solc < 0.4.5).",
    "swc": "SWC"
  },
  "erc20-interface": {
    "description": "Incorrect return values for ERC20 functions. A contract compiled with Solidity > 0.4.22 interacting with these functions will fail to execute them, as the return value is missing.",
    "swc": "SWC"
  },
  "erc721-interface": {
    "description": "Incorrect return values for ERC721 functions. A contract compiled with solidity > 0.4.22 interacting with these functions will fail to execute them, as the return value is missing.",
    "swc": "SWC"
  },
  "incorrect-equality": {
    "description": "Use of strict equalities that can be easily manipulated by an attacker.",
    "swc": "SWC"
  },
  "locked-ether": {
    "description": "Contract with a payable function, but without a withdrawal capacity.",
    "swc": "SWC"
  },
  "mapping-deletion": {
    "description": "A deletion in a structure containing a mapping will not delete the mapping (see the Solidity documentation). The remaining data may be used to compromise the contract.",
    "swc": "SWC"
  },
  "shadowing-abstract": {
    "description": "Detection of state variables shadowed from abstract contracts.",
    "swc": "SWC"
  },
  "tautology": {
    "description": "Detects expressions that are tautologies or contradictions.",
    "swc": "SWC"
  },
  "write-after-write": {
    "description": "Detects variables that are written but never read and written again.",
    "swc": "SWC"
  },
  "boolean-cst": {
    "description": "Detects the misuse of a Boolean constant.",
    "swc": "SWC"
  },
  "constant-function-asm": {
    "description": "Functions declared as constant/pure/view using assembly code.",
    "swc": "SWC"
  },
  "constant-function-state": {
    "description": "Functions declared as constant/pure/view change the state.",
    "swc": "SWC"
  },
  "divide-before-multiply": {
    "description": "Solidity's integer division truncates. Thus, performing division before multiplication can lead to precision loss.",
    "swc": "SWC"
  },
  "reentrancy-no-eth": {
    "description": "Detection of the reentrancy bug.Do not report reentrancies that involve Ether (see reentrancy-eth).",
    "swc": "SWC"
  },
  "reused-constructor": {
    "description": "Detects if the same base constructor is called with arguments from two different locations in the same inheritance hierarchy.",
    "swc": "SWC"
  },
  "tx-origin": {
    "description": "tx.origin-based protection can be abused by a malicious contract if a legitimate user interacts with the malicious contract.",
    "swc": "SWC"
  },
  "unchecked-lowlevel": {
    "description": "The return value of a low-level call is not checked.",
    "swc": "SWC"
  },
  "unchecked-send": {
    "description": "The return value of a send is not checked.",
    "swc": "SWC"
  },
  "uninitialized-local": {
    "description": "Uninitialized local variables.",
    "swc": "SWC"
  },
  "unused-return": {
    "description": "The return value of an external call is not stored in a local or state variable.",
    "swc": "SWC"
  },
  "incorrect-modifier": {
    "description": "If a modifier does not execute _ or revert, the execution of the function will return the default value, which can be misleading for the caller.",
    "swc": "SWC"
  },
  "shadowing-builtin": {
    "description": "Detection of shadowing built-in symbols using local variables, state variables, functions, modifiers, or events.",
    "swc": "SWC"
  },
  "shadowing-local": {
    "description": "Detection of shadowing using local variables.",
    "swc": "SWC"
  },
  "uninitialized-fptr-cst": {
    "description": "solc versions 0.4.5-0.4.26 and 0.5.0-0.5.8 contain a compiler bug leading to unexpected behavior when calling uninitialized function pointers in constructors.",
    "swc": "SWC"
  },
  "variable-scope": {
    "description": "Detects the possible usage of a variable before the declaration is stepped over (either because it is later declared, or declared in another scope).",
    "swc": "SWC"
  },
  "void-cst": {
    "description": "Detect the call to a constructor that is not implemented",
    "swc": "SWC"
  },
  "calls-loop": {
    "description": "Calls inside a loop might lead to a denial-of-service attack.",
    "swc": "SWC"
  },
  "events-access": {
    "description": "Detect missing events for critical access control parameters",
    "swc": "SWC"
  },
  "events-maths": {
    "description": "Detect missing events for critical arithmetic parameters.",
    "swc": "SWC"
  },
  "incorrect-unary": {
    "description": "Unary expressions such as x=+1 probably typos.",
    "swc": "SWC"
  },
  "missing-zero-check": {
    "description": "Detect missing zero address validation.",
    "swc": "SWC"
  },
  "reentrancy-benign": {
    "description": "Detection of the reentrancy bug.Only report reentrancy that acts as a double call (see reentrancy-eth, reentrancy-no-eth).",
    "swc": "SWC"
  },
  "reentrancy-events": {
    "description": "Detects reentrancies that allow manipulation of the order or value of events.",
    "swc": "SWC"
  },
  "timestamp": {
    "description": "Dangerous usage of block.timestamp. block.timestamp can be manipulated by miners.",
    "swc": "SWC"
  },
  "assembly": {
    "description": "The use of assembly is error-prone and should be avoided.",
    "swc": "SWC"
  },
  "assert-state-change": {
    "description": "Incorrect use of assert(). See Solidity best practices.",
    "swc": "SWC"
  },
  "boolean-equal": {
    "description": "Detects the comparison to boolean constants.",
    "swc": "SWC"
  },
  "cyclomatic-complexity": {
    "description": "Detects functions with high (> 11) cyclomatic complexity.",
    "swc": "SWC"
  },
  "deprecated-standards": {
    "description": "Detect the usage of deprecated standards.",
    "swc": "SWC"
  },
  "erc20-indexed": {
    "description": "Detects whether events defined by the ERC20 specification that should have some parameters as indexed are missing the indexed keyword.",
    "swc": "SWC"
  },
  "function-init-state": {
    "description": "Detects the immediate initialization of state variables through function calls that are not pure/constant, or that use non-constant state variable.",
    "swc": "SWC"
  },
  "incorrect-using-for": {
    "description": "In Solidity, it is possible to use libraries for certain types, by the using-for statement (using <library> for <type>). However, the Solidity compiler doesn't check whether a given library has at least one function matching a given type. If it doesn't, such a statement has no effect and may be confusing.",
    "swc": "SWC"
  },
  "low-level-calls": {
    "description": "The use of low-level calls is error-prone. Low-level calls do not check for code existence or call success.",
    "swc": "SWC"
  },
  "missing-inheritance": {
    "description": "Detect missing inheritance.",
    "swc": "SWC"
  },
  "naming-convention": {
    "description": "Solidity defines a naming convention that should be followed.",
    "swc": "SWC"
  },
  "pragma": {
    "description": "Detect whether different Solidity versions are used.",
    "swc": "SWC"
  },
  "redundant-statements": {
    "description": "Detect the usage of redundant statements that have no effect.",
    "swc": "SWC"
  },
  "solc-version": {
    "description": "solc frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.We also recommend avoiding complex pragma statement.",
    "swc": "SWC"
  },
  "unimplemented-functions": {
    "description": "Detect functions that are not implemented on derived-most contracts.",
    "swc": "SWC"
  },
  "unused-state": {
    "description": "Unused state variable.",
    "swc": "SWC"
  },
  "costly-loop": {
    "description": "Costly operations inside a loop might waste gas, so optimizations are justified.",
    "swc": "SWC"
  },
  "dead-code": {
    "description": "Functions that are not sued.",
    "swc": "SWC"
  },
  "reentrancy-unlimited-gas": {
    "description": "Detection of the reentrancy bug.Only report reentrancy that is based on transfer or send.",
    "swc": "SWC"
  },
  "similar-names": {
    "description": "Detect variables with names that are too similar.",
    "swc": "SWC"
  },
  "too-many-digits": {
    "description": "Literals with many digits are difficult to read and review.",
    "swc": "SWC"
  },
  "cache-array-length": {
    "description": "Detects for loops that use length member of some storage array in their loop condition and don't modify it.",
    "swc": "SWC"
  },
  "constable-states": {
    "description": "State variables that are not updated following deployment should be declared constant to save gas.",
    "swc": "SWC"
  },
  "external-function": {
    "description": "public functions that are never called by the contract should be declared external, and its immutable parameters should be located in calldata to save gas.",
    "swc": "SWC"
  },
  "immutable-states": {
    "description": "State variables that are not updated following deployment should be declared immutable to save gas.",
    "swc": "SWC"
  },
  "var-read-using-this": {
    "description": "The contract reads its own variable using this, adding overhead of an unnecessary STATICCALL.",
    "swc": "SWC"
  }
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
