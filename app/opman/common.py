from flask import Response,jsonify

def success(message={},data=None):
    response = {'code':200,'message':message,'data':data}
    return jsonify(response)

def error(message=None):
    response = {'code':400,'message':message}
    return jsonify(response)