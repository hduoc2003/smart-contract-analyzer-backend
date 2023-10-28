from flask import Blueprint
from server.v1.api.client.routes.tool.submit.submit_route import submit_route
from server.v1.api.client.routes.tool.file.file_route import file_route

tool_route = Blueprint("tool_bp", __name__, url_prefix="/tool")
tool_route.register_blueprint(submit_route)
tool_route.register_blueprint(file_route)


# @tool_route.route('/handle_file_id', methods=["GET"])
# @cross_origin(supports_credentials=True)
# def handle_file_id():
#     id_param = request.args.get('id')
#     if id_param is None:
#         return "No file_id provided"
#     file: FileDoc = get_file_by_id(id_param)

#     if file is not None:
#         return file.to_json()
#     else:
#         return "File not found", StatusCode.NotFound.value  # Return a 404 Not Found status code

# def update_result(result: FinalResult, detach: bool = False):
#     def main():
#         tool_name: str = result.tool_name
#         duration: float = result.duration
#         solc: str = result.solc
#         analysis: AnalysisResult = result.analysis

#         file_id: str = result.file_name.replace(".sol", "")
#         status: AnalyzeStatus = AnalyzeStatus.ERROR if len(analysis.errors) != 0 else AnalyzeStatus.COMPLETED

#         try:
#             update_one(doc=FileDoc, data={
#                 "status": status,
#                 "tool_name": tool_name,
#                 "duration": duration,
#                 "solc": solc,
#                 "analysis": obj_to_json(analysis)

#             }, id=file_id)

#         except Exception as exc:
#             # for field in vars(FileDoc):    # You could also loop in User._fields to make something generic
#             #     if field in str(exc):
#             FlaskLog.err(exc)
#             # FlaskLog.err('field {} is not unique'.format(field))
#             # FlaskLog.err(new_file.id)

#         del map_id_to_name[result.file_name]

#     if detach:
#         Async.run_functions([main], [[]], True)
#     else:
#         main()
    # return files_id
