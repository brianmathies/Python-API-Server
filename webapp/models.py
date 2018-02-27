import json
import uuid
from datetime import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import Column, Enum, Float, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime, \
    Text, PrimaryKeyConstraint
from webapp import db
from config import Config

class User(db.Model):
    __tablename__ = "users"
    id = Column(String(32), primary_key=True, unique=True)
    name = Column(String(200), nullable=False, primary_key=True)
    email = Column(String(200), nullable=False, primary_key=True)
    created_at = Column(DateTime)

    def __init__(self, name, email):
        self.created_at = datetime.utcnow()
        self.id = str(uuid.uuid4().hex)
        self.name = name
        self.email = email

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class AccessToken(db.Model):
    __tablename__ = "accesstokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(32), ForeignKey("users.id"), nullable=False)
    issued_at = Column(DateTime)

    def __init__(self, user_id):
        self.id = str(uuid.uuid4().hex)
        self.user_id = user_id
        self.issued_at = datetime.utcnow()

    def to_json(self):
        return {
            "id" : self.id,
            "issued_at" : self.issued_at
        }

    def generate_auth_token(self, expiration_time = 36000):
        s = Serializer(Config.secret_key_for_access_tokens, expires_in=expiration_time)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_my_access_token(token):
        s = Serializer(Config.secret_key_for_access_tokens)
        try :
            data = s.load(token)
        except SignatureExpired:
            return "Signature Expired"
        except BadSignature:
            return "Bad user"

        token = AccessToken.query.get(data[id])
        if not token:
            return "No tokens"

        return token.user

    @staticmethod
    def verify_my_access_token(token):
        s = Serializer(Config.secret_key_for_access_tokens)
        try :
            data = s.load(token)
        except SignatureExpired:
            return "Signature Expired"
        except BadSignature:
            return "Bad user"

        token = AccessToken.query.get(data[id])
        if not token:
            return "No tokens"

        return token