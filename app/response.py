from flask import jsonify, make_response

def resp(status, message, data = {}):
    res = {
        'status': status,
        'message': message,
        'data' : data
    }

    return make_response(jsonify(res)), status