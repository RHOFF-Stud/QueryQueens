from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
try:
    db = MongoEngine()
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": os.getenv('bhhshop'),
            "host": os.getenv('HOST'),
            "port": int(os.getenv('PORT')),
            #"user": os.getenv('USER'),
            #"password": os.getenv('PASSWORD')
        }
    ]

    db.init_app(app)

    db = MongoEngine(app=app)
except Exception as e:
    print(e)
