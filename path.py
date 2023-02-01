from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)

CORS(app)

try:
    db = MongoEngine()
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": os.getenv('DATABASE'),
            "host": os.getenv('HOST'),
            #"host": "mongodb+srv://queryqueens:SuperSicher123.@cluster0.r9xszy9.mongodb.net/test"
            "port": int(os.getenv('PORT')),
            "user": os.getenv('USER'),
            "password": os.getenv('PASSWORD')
        }
    ]

    db.init_app(app)

    db = MongoEngine(app=app)
except Exception as e:
    print(e)
