from flask import request, jsonify, Response
from webapp.mod_auth import mod_auth
from webapp import  db as webdb
from webapp.models import *
from webapp.helpers import json_helpers


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
    email = email=data["email"]
    password = password=data["password"]
    user = webdb.session.query(User).filter_by(email=data["email"]).first()
    if not user:
        Response.status = 404
        Response.data = "Invalid User"
        return Response
    if not user.check_password(password):
        return Response == 404
        Response.data = "Invalid Password"
        return Response

    token = AccessToken(user_id=user.id)
    token_string = token.generate_auth_token(expiration_time=3000)
    user_json = user.to_json()
    user_json["token"] = token_string
    user_json = jsonify(user_json)
    return user_json

@mod_auth.route("/access_token",methods)

