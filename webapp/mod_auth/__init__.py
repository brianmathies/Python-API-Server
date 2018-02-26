from flask import Blueprint

print(__name__)
mod_auth = Blueprint("mod_auth",__name__)

from webapp.mod_auth import api


