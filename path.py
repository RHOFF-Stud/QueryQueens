from flask import Flask
from flask_mongoengine import MongoEngine


app = Flask(__name__)
try:
    db = MongoEngine()
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": "bhhshop",
            "host": "localhost",
            "port": 27017,
            "user": "apiuser",
            "password": "Start1234!"
        }
    ]

    db.init_app(app)

    db = MongoEngine(app=app)
except Exception as e:
    print(e)
