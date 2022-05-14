from flask import request, jsonify, Response
from webapp.mod_auth import mod_auth
from webapp import  db as webdb
from webapp.models import *
from webapp.helpers import json_helpers
import base64
import os

@mod_auth.route("/register", methods=["post"])
def register_user():
    data = request.get_json(force=True)
    user = User(name=data["name"], email=data["email"],password=data["password"])
    webdb.session.add(user)
    webdb.session.commit()
    return jsonify({"result": "User created"})


@mod_auth.route("/login", methods=["post"])
def login_user():
    data = request.get_json(force=True)
    email = data["email"]
    password = data["password"]
    user = webdb.session.query(User).filter_by(email=data["email"]).first()
    if not user:
        return Response(json.dumps({"result": "no user"}) , status=404 , mimetype='application/json')
    if not user.check_password(password):
        return Response(json.dumps({"result": "wrong password"}) , status=404 , mimetype='application/json')


    token = AccessToken(user_id=user.id)
    token_string = token.generate_auth_token(expiration_time=3000)
    user.accesstokens.append(token)
    user_json = user.to_json()
    user_json["token"] = token_string
    user_json = jsonify(user_json)
    webdb.session.commit()
    return user_json

@mod_auth.route("access_token",methods=["post"])
def verify_access_token():
    data = request.get_json(force=True)
    token_result = AccessToken.verify_my_access_token(data["accesstoken"])
    if(token_result["status"] != 200):
        return Response(json.dumps({"result": token_result["result"]}), status=404, mimetype='application/json')
    return Response(json.dumps({"result": token_result["result"].id}), status=200, mimetype='application/json')

@mod_auth.route("/pronounce-it-right/phonemes",methods=['POST'])
def post():
# decode base64 string to original binary sound object
    # b64 = request.get_json(force=True)
    return Response(json.dumps({"result": "hello"}), status=200, mimetype='application/json')
    '''
    decodedData = base64.b64decode(b64.payload)
    outdir = os.getcwd()

    with open(wavfile, 'wb') as file:
        data = request.get_json(force=True)
    '''
