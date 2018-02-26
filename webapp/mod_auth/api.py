from flask import Flask
from webapp.mod_auth import mod_auth
print(mod_auth.name)
@mod_auth.route("/auth",methods=["get"])
def simpleAPI():
    return "hello world"