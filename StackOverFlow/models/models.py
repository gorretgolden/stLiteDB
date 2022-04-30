from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from   flask_marshmallow import Marshmallow
from marshmallow import fields
from dataclasses import dataclass
db = SQLAlchemy()


@dataclass
class User(db.Model):
   id: int
   email: str
   username:str
   created_at:datetime
   questions:list
   answers:list
   __tablename__ = 'users'   
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.Text(), nullable=False)
   created_at = db.Column(db.DateTime, default=datetime.now())
   updated_at = db.Column(db.DateTime, onupdate=datetime.now())
   questions = db.relationship('Question', backref="user")
   answers = db.relationship('Answer', backref="user")

   def __repr__(self):
        return "<User %r>" % self.username

   def tojson(self):
       return self.__dict__

     #creating all database schema
# class UserSchema(ma.SQLAlchemyAutoSchema):
#   class Meta:  
#    model = User
#    #sqla_session = db.session
#    id = fields.Number(dump_only=True)
#    username = fields.String(required=True)
#    email = fields.String(required=True)
#    password = fields.String(required=True)
  
    
@dataclass
class Question(db.Model):
    id: int
    title:str
    body:str
    tag:str
    user_id:int
    created_at:datetime
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,unique=True,nullable=False)
    body = db.Column(db.Text,unique=True, nullable=False)
    tag = db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),ondelete='SET NULL')
    created_at = db.Column(db.DateTime, default=datetime.now())

    
    def __repr__(self):
        return "<Question %r>" % self.id
@dataclass
class Answer(db.Model):
    id: int
    body:str
    question_id:int
    user_id:int
    created_at:datetime
    is_accepted:bool
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),ondelete='SET NULL')
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'),ondelete='SET NULL')
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_accepted = db.Column(db.Boolean,default=False,nullable=False)
      
    def __repr__(self):
        return "<Answers %r>" % self.id

    
    



 