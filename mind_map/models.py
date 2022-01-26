from sqlalchemy import Integer, Enum, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Node(db.Model):
    id = db.Column(Integer, primary_key=True)
    slug = db.Column(String(100), nullable=True)
    text = db.Column(String(200), nullable=False)
    parent_id = db.Column(Integer, db.ForeignKey('node.id'), nullable=True)

    @property
    def as_json(self):
        return {'slug': self.slug, 'text': self.text}

    @staticmethod
    def from_json(json):
        slug = json['slug']
        text = json['text']
        return Node(slug=slug, text=text)
