
from typing import List
from tools.types import FinalResult, AnalysisIssue, AnalysisResult
import os
from tools.utils.Log import Log
from tools.utils.parsers import obj_to_jsonstr
import copy

class DuplicateIssue():
    dup_issues = [
        {"slither": "suicidal", "mythril": "Unprotected Selfdestruct"},
        {"slither": "reentrancy-eth", "mythril": "External Call To User-Supplied Address"},
        {"slither": "reentrancy-event", "mythril": "External Call To User-Supplied Address"},
        {"slither": "controlled-delegatecall", "mythril": "Delegatecall to user-supplied address"},
        {"slither": "controlled-delegatecall", "mythril": ""},#false positive
        {"slither": "assembly", "mythril": "Jump to an arbitrary instruction"}
        # Add more mappings here
    ]
    merge_issues = ["false-positive", "duplicate"]

    @classmethod
    def export_duplicate_result(cls, file_name: str, result):
        split_parts = file_name.split("-")
        swc_number = ''.join(filter(str.isdigit, split_parts[1]))
        directory_path = os.path.join("tools", "utils", "duplicate_issues", f"swc-{swc_number}",f"{os.path.splitext(file_name)[0]}")
        os.makedirs(directory_path, exist_ok=True)  # Create directories if they don't exist

        try:
            # if isinstance(result, AnalysisIssue):
                file_name1 = os.path.splitext(file_name)[0] + '-duplicate-issues.json'
                file_path1 = os.path.join(directory_path, file_name1)
                with open(file_path1, 'w') as json_file:
                    json_file.write(obj_to_jsonstr(result))
                Log.info("Export merge successful")

        except Exception as e:
            Log.err(f'Error occured when export duplicate of file {file_name}')
            Log.err(e)

    @classmethod
    def checkFalsePositive(cls, slither_issue: AnalysisIssue, mythril_issue: AnalysisIssue) ->bool:
        if slither_issue.issue_title != "controlled-delegatecall":
            return False
        if mythril_issue.issue_title == "Delegatecall to user-supplied address":
            if isinstance(mythril_issue.line_no, list) and len(mythril_issue.line_no) == 1:
                mythril_line_no = mythril_issue.line_no[0]
            else:
                mythril_line_no = mythril_issue.line_no
            if mythril_line_no in slither_issue.line_no:
                return False
        return True
    @classmethod
    def classifyIssues(cls, slither_issues: List[AnalysisIssue], mythril_issues: List[AnalysisIssue], file_name) -> List[AnalysisIssue]:
        """_summary_

        Args:
            slither_issues (List[AnalysisIssue]): Là list lỗi của riêng slither
            mythril_issues (List[AnalysisIssue]): Là list lỗi của riêng mythril
            file_name (_type_): tên từng file

        Returns:
            List[AnalysisIssue]: kết quả sau khi đã merge, sắp xếp theo merged->slither->mythril
        """
        analysis_issues: List[AnalysisIssue] = []

        #các issue của từng tool không cần merge sẽ điền vào đây để xếp theo thứ tự merge-issue- slither-issue- mythril-issue
        slither_issues_left: List[AnalysisIssue] = copy.deepcopy(slither_issues)
        mythril_issues_left: List[AnalysisIssue] = copy.deepcopy(mythril_issues)

        if len(slither_issues) == 0 and len(mythril_issues) ==0:
            return []
        if len(mythril_issues) == 0:
            for slither_issue in slither_issues:
                if slither_issue.issue_title == "controlled-delegatecall":
                    slither_issues_left.remove(slither_issue)
            return slither_issues_left
        if len(slither_issues) == 0:
            return mythril_issues
        #dùng để print, TODO: xoá khi confirm
        duplicate_issues_detected: List[AnalysisIssue] = []

        for slither_issue in slither_issues:
            for mythril_issue in mythril_issues:
                checkFP = cls.checkFalsePositive(slither_issue, mythril_issue)
                if checkFP == True:
                    #bỏ đi vì slither check sai
                    slither_issues_left.remove(slither_issue)
                    break
                check= False
                for mapping in cls.dup_issues:

                    if mapping["slither"] == slither_issue.issue_title and mapping["mythril"] == mythril_issue.issue_title :
                        if isinstance(mythril_issue.line_no, list) and len(mythril_issue.line_no) == 1:
                            mythril_line_no = mythril_issue.line_no[0]
                        else:
                            mythril_line_no = mythril_issue.line_no
                        if mythril_line_no in slither_issue.line_no: #kiểm tra có cùng một đoạn lỗi
                            check = True
                            slither_issues_left.remove(slither_issue)
                            mythril_issues_left.remove(mythril_issue)
                            merged_issue = AnalysisIssue(
                                contract=slither_issue.contract or mythril_issue.contract,
                                source_map=mythril_issue.source_map,
                                line_no=mythril_issue.line_no,
                                code=mythril_issue.code,
                                description=slither_issue.description + '\n' + mythril_issue.description,
                                hint=slither_issue.hint,
                                issue_title=slither_issue.issue_title or mythril_issue.issue_title,
                                swcID=mythril_issue.swcID,
                                swc_title=mythril_issue.swc_title,
                                swc_link=mythril_issue.swc_link,
                                severity="chua lam"
                            )
                            duplicate_issues_detected.append(merged_issue)
        analysis_issues.extend(duplicate_issues_detected)
        analysis_issues.extend(slither_issues_left)
        analysis_issues.extend(mythril_issues_left)

        return analysis_issues

    @classmethod
    def merge(cls, final_slither: FinalResult, final_mythril: FinalResult) -> AnalysisResult:
        file_name = final_slither.file_name
        if len(final_mythril.analysis.errors) == 0 and len(final_slither.analysis.errors) != 0:
            return AnalysisResult(
                errors = final_slither.analysis.errors,
                issues = final_mythril.analysis.issues
            )
        if len(final_mythril.analysis.errors) != 0 and len(final_slither.analysis.errors) == 0:
            return AnalysisResult(
                errors = final_mythril.analysis.errors,
                issues = final_slither.analysis.issues
            )

        slither_issues = final_slither.analysis.issues
        mythril_issues = final_mythril.analysis.issues
        return AnalysisResult(
            errors= final_mythril.analysis.errors + final_slither.analysis.errors,
            issues = cls.classifyIssues(slither_issues, mythril_issues, file_name)
        )



