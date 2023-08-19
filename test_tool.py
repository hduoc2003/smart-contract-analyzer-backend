import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import pathlib
import json
import time
from tools.Tool import Tool

from tools.docker.Docker import Docker
from tools.utils.Async import Async
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# s: str = 10000000 * 'i'

# def w1():
#     start = time()
#     with open('file1.txt', 'w') as f1:
#         f1.write(s)
#     end = time()
#     return end - start

# def w2():
#     start = time()
#     with open('file2.txt', 'w') as f2:
#         f2.write(s)
#     end = time()
#     return end - start

# async def main():
#     results = await asyncio.gather(asyncio.to_thread(w1), asyncio.to_thread(w2))
#     print(results)

# start = time()
# asyncio.run(main())
# end = time()
# print(end - start)

start = time.time()
result = [t.duration for t in asyncio.run(Tool.analyze_files_async(
    file_dir_path=r'D:\SE_LAB\SE_Task\blockchain\tool\test-mythril\bugs',
    files_names=['swc-107.sol']*10
))]
# result = [t.duration for t in asyncio.run(Tool.analyze_files_async(
#     file_dir_path=r'D:\University\Laboratory\Blockchain\Tool Intergrating\ReBuild\BE\tools\data\SWC-117',
#     files_names=['transaction_malleablity.sol']*10
# ))]
# result = Async.run_single_func(Tool.ru)
end = time.time()

print(end - start)
print(result)



