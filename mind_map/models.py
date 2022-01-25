from sqlalchemy import Integer, Enum, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Node(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=True)
    description = db.Column(String(200), nullable=False)

class Parent2Child(db.Model):
    parent_id = db.Column(Integer, db.ForeignKey('node.id'), nullable=False)
    child_id = db.Column(Integer, db.ForeignKey('node.id'), unique=True, nullable=False, primary_key=True)
