from flask import request, jsonify, Response
from webapp.models import *

def validate_json(*args,**kwargs):
    def wrapper(func):
        def validator(*args):
            user_data = request.get_json(force=True)
            schema_keys = kwargs["schema"].keys
            print("-----------------------------------------------------")
            print(schema_keys)
            func(*args)
        return validator
    return wrapper