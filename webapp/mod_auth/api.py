from flask import  request , jsonify
from webapp.mod_auth import mod_auth
from webapp import  db as webdb
from webapp.models import User




@mod_auth.route("/auth",methods=["post"])
def register_user():
    data = request.get_json(force=True)
    user = User(name=data["name"],email=data["email"])
    webdb.session.add(user)
    webdb.session.commit()
    return "success"

