import json
from os import path
import os
from random import sample
from typing import Any, Generator
from server.v1.api.utils.path import get_all_files

from tools.Tool import Tool
from tools.tool_types import ToolAnalyzeArgs, ToolName
from tools.utils.parsers import obj_to_jsonstr

log_path = path.join(path.dirname(__file__), f"./tools/storage/survey-logs")

m = {
    "DC": "SWC-112",
    "TD": "SWC-116",
    "RE": "SWC-107",
    "IOU": "SWC-101",
    "UpS": "SWC-106",
    "UcC": "SWC-104",
}

y: dict[str, Any] = {}

with open("f.json", "r") as f:
    data = json.loads(f.read())
    files_name: dict[str, str] = data["contract_name"]
    for idx in files_name:
        y[idx] = json.loads(data['overlapping'][idx])

# print(json.dumps(y['0'], indent=4))

def get_file_name(i: int | str):
    return f"{files_name[str(i)]}-{i}.sol"

def survey():

        # t = 0
        # for idx in files_name:
        #     if (files_name[idx]):
        #         if (path.exists(f'./tools/storage/survey/{get_file_name(idx)}.sol')):
        #             print(get_file_name(idx))
        #         else:
        #             with open(f'./tools/storage/survey/{get_file_name(idx)}', "w", encoding='utf-8') as g:
        #                 g.write(data['source_code'][idx])
        #             t += 1
        #         # print(idx)
        # print(t)

    p = path.join(path.dirname(__file__), "./tools/storage/survey")
    config = []
    done = get_all_files(
        path.join(path.dirname(__file__), f"./tools/storage/survey-logs"), [".json"]
    )
    done = [x.split(".json")[0] for x in done]
    # print(done)
    # for i in ['32', '52', '12', '25', '7', '23', '1', '51', '5', '27', '4']:
    # for i in ['120']:
    for i in range(0, 50):
        if get_file_name(i) in done:
            continue
        # config.append(ToolAnalyzeArgs("survey", get_file_name(i)))
        # y[str(i)] = json.loads(data["overlapping"][str(i)])
        for type in y[str(i)]:
            if  (type in m):
                # print(i)
                config.append(ToolAnalyzeArgs("survey", get_file_name(i)))
                break

    res = Tool.analyze_files_async(config, tools=[ToolName.Mythril], stream=True)
    for x in res:
        logs = {"suspect": [], "source_code": "", "mythril_analysis": ""}
        i = x.file_name.split("-")[1].split(".sol")[0]
        if len(x.analysis.errors) > 0:
            print("error:", get_file_name(i))
        else:
            print("done: ", get_file_name(i))
        for type in y[i]:
            if type in m:
                ok = False
                for g in x.analysis.issues:
                    if m[type] == g.swcID:
                        ok = True
                        break
                if not ok:
                    print(type, m[type], get_file_name(i))
                    logs["suspect"].append({"sample_type": type, "swc": m[type]})
        logs["source_code"] = data["source_code"][str(i)]
        logs["mythril_analysis"] = x
        with open(
            path.join(
                path.dirname(__file__),
                f"./tools/storage/survey-logs/{get_file_name(i)}.json",
            ),
            "w",
        ) as l:
            l.write(obj_to_jsonstr(logs))

def filter():
    logs = get_all_files(log_path, ['.json'])
    print(len(logs))
    err_cnt = 0
    for log_file in logs:
        p = path.join(log_path, log_file)
        with open(p, 'r') as f:
            log = json.loads(f.read())
            err: list = log['mythril_analysis']['analysis']['errors']
            if ((len(err)) > 0) :
                err_cnt += 1

                # print(json.dumps(err, indent=4))
                # print(log_file)
                # print('\n')
                if err[0]['msg'] == '' or (err[0]['error'] == 'runtime out') or (err[0]['msg'].find('Please report this issue to the Mythril GitHub page') != -1) or (err[0]['msg'].find('mythril.ethereum.util') != -1):
                    if (err[0]['msg'] == ''):
                        os.remove(p)
                    print(log_file)
                    # print(err[0]['msg'])
                    # err_cnt += 1
                    print('\n')
                    # os.remove(p)
    print(err_cnt)
    return

def stat():
    sample_type_cnt = {}
    suspect_cnt = {}
    total_time = 0
    err_cnt = 0
    err_stat: dict[str, int] = {
        'empty': 0,
        'runtime out': 0,
        'other': 0,
        'compile error': 0,
        'unsupported solc': 0
    }
    logs = get_all_files(log_path, ['.json'])
    for log_file in logs:
        p = path.join(log_path, log_file)
        with open(p, 'r') as f:
            log = json.loads(f.read())
            i = log_file.split("-")[1].split(".sol.json")[0]
            total_time += log['mythril_analysis']['duration']
            for g in y[i]:
                if not (g in m):
                    continue
                # print(i, ',', g)
                if (g in sample_type_cnt):
                    sample_type_cnt[g] += 1
                else:
                    sample_type_cnt[g] = 1

            if (len(log['mythril_analysis']['analysis']['errors']) == 0):
                for x in log['suspect']:
                    type = x['sample_type']
                    # print(log['mythril_analysis']['file_name'])
                    if (type in suspect_cnt):
                        suspect_cnt[type] += 1
                    else:
                        suspect_cnt[type] = 1
            else:
                err_cnt += 1
                err: list = log['mythril_analysis']['analysis']['errors']
                if err[0]['msg'] == '':
                    err_stat['empty'] += 1
                    print(log_file)
                elif (err[0]['error'] == 'runtime out'):
                    err_stat['runtime out'] += 1
                elif (err[0]['error'] == 'compile error'):
                    err_stat['compile error'] += 1
                elif (err[0]['msg'].find('solcx.exceptions.UnsupportedVersionError') != -1) or (err[0]['error'] == 'unsupported solc'):
                    err_stat['unsupported solc'] += 1
                else:
                    err_stat['other'] += 1
                if (len(err) > 0):
                    print(err)
                    print('\n')

    print('Tổng số file phân tích: ', len(logs))
    print('Tổng số file chạy lỗi: ', err_cnt)
    print(sample_type_cnt)
    print(suspect_cnt)
    print(total_time)
    print(err_stat)

survey()
# filter()
# stat()
