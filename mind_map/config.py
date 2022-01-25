import os

HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', 9999)
DEBUG = os.getenv('DEBUG', True)

DB_URI = 'sqlite:///app.db'
TRACK_MODS = False
