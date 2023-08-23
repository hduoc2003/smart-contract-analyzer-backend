import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import pathlib
import json
import time
from tools.Mythril import Mythril
from tools.Slither import Slither
from typing import List
# from tools.Slither import Slither
from tools.Tool import Tool

from tools.type import FinalResult, ToolAnalyzeArgs, ToolName
from tools.utils.parsers import obj_to_jsonstr
from tools.docker.Docker import Docker
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

g: List[FinalResult] = Tool.analyze_files_async(
    files=[
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-106.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-107-modifier-reentrancy.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-107-reentrancy-eth.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-107-simple-dao.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-110-contructor-create-argument.sol",
            # solc="0.4.13"
        ),
        
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-110-out-of-bounds-exception.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-110-return-memory.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-110-two-mapppings.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-110-sha-of-sha-collision.sol",
            # sol,c="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-112-proxy.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-112-proxy-pattern-false-positive.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-120-guess-the-number.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-120-old-blockhash.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-120-random-number-generator.sol",
            # solc="0.4.13"
        ),
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-127.sol",
            # solc="0.4.13"
        )
        
    ],
    tools=[ToolName.Slither, ToolName.Mythril]
)

print(g)