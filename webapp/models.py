import json
import uuid, hashlib
from datetime import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import Column, Enum, Float, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime, \
    Text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from webapp import db
from config import Config

class User(db.Model):
    __tablename__ = "users"
    id = Column(String(32), primary_key=True, unique=True)
    name = Column(String(200), nullable=False, primary_key=True)
    email = Column(String(200), nullable=False, primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    created_at = Column(DateTime)
    accesstokens = relationship("AccessToken" ,back_populates="users")

    def __init__(self, name, email, password):
        self.created_at = datetime.utcnow()
        self.id = str(uuid.uuid4().hex)
        self.name = name
        self.email = email
        self.salt = uuid.uuid4().hex
        self.password_hash = User.hash_password(salt=self.salt, password=password)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def check_password(self,password):
        current_password = self.hash_password(self.salt, password)
        if(current_password == self.password_hash):
            return True
        else:
            return False

    @staticmethod
    def hash_password(salt, password):
        return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

class AccessToken(db.Model):
    __tablename__ = "accesstokens"
    id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey("users.id"), nullable=False)
    issued_at = Column(DateTime)
    users = relationship("User" , back_populates="accesstokens")

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
        return s.dumps({"id": self.id}).decode()

    @staticmethod
    def verify_my_access(token):
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
            data = s.loads(token)
        except SignatureExpired:
            return ({"status": 404,"result": "Signature Expired"})
        except BadSignature:
            return ({"status": 404,"result": "Bad User"})

        token = AccessToken.query.get(data["id"])
        if not token:
            return ({"status": 404,"result": "No tokens for user"})

        return ({"status": 200,"result": token})