from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

db = MongoEngine()
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "project1",
        "host": "localhost",
        "port": 27017,
        "alias": "default",
    }
]
db.init_app(app)
DB_URI = ""
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine(app=app)
