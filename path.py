from flask import Flask
from flask_mongoengine import MongoEngine


app = Flask(__name__)
try:
    db = MongoEngine()
    app.config["MONGODB_SETTINGS"] = [
        {
    #        "db": "test",
            "host": "mongodb+srv://queryqueens:SuperSicher123.@cluster0.r9xszy9.mongodb.net/shop",
    #        "port": 27017,
        }
    ]

    db.init_app(app)

    db = MongoEngine(app=app)
except Exception as e:
    print(e)
