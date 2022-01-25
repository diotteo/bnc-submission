from flask import Flask

from models import db

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app.config['TRACK_MODS'] # Disable Flask-SQLAlchemy event system
db.app = app
db.init_app(app)

from routes import *

if __name__ == '__main__':
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])
