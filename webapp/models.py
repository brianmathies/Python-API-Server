import json
import uuid
from datetime import datetime
from sqlalchemy import Column, Enum, Float, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime, \
    Text, PrimaryKeyConstraint
from webapp import  db

class User(db.Model):
    __tablename__ = "users"
    id = Column(String(32),primary_key=True)
    name = Column(String(200),nullable=False,primary_key=True)
    email = Column(String(200),nullable=False,primary_key=True)
    created_at = Column(DateTime)

    def __init__(self,name,email):
        self.created_at = datetime.utcnow()
        self.id = str(uuid.uuid4().hex)
        self.name = name
        self.email = email

    def to_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "email": self.email
        }