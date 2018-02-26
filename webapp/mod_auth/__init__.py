from flask import Blueprint

print(__name__)
mod_auth = Blueprint("mod_auth",__name__)

@mod_auth.route("/auth",methods=["get"])
def auth_user():
    return "hello world"
