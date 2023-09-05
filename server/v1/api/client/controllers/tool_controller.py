from flask import Flask, jsonify

def handle_tool():
    return jsonify({"message": "access_tool_route"})