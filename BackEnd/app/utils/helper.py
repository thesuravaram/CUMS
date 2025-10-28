from flask import jsonify

def success_response(message, data=None):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), 200

def error_response(message):
    return jsonify({
        "status": "error",
        "message": message
    }), 400
