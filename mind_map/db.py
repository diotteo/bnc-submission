from flask_sqlalchemy import SQLAlchemy

import mind_mapper
from models import db

if __name__ == "__main__":
    db.create_all()
