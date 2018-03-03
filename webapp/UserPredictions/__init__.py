from flask import Blueprint

print(__name__)
StaticPredictorsBluePrint = Blueprint("data", __name__)

from webapp.UserPredictions import StaticPredictors