from flask import Flask
from flask_mongoengine import MongoEngine
import json
import time


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


@app.route('/', methods=['GET'])
def home_page():
    data_set = {'Page': 'Home', 'Message': 'Successfully loaded', 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)

    return json_dump


class DataObject:
    def toJSON(self):
        dump = json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
        return json.loads(dump)

    def __init__(self):
        pass


class TShirt(DataObject, db.Document):
    def __init__(self):
        super().__init__()
        self.tshirt_id = int
        self.name = ""


@app.route('/api/db_populate', methods=['GET', 'POST'])
def db_populate():
    try:
        new_Tshirt = TShirt()

        new_Tshirt.tshirt_id = 5
        new_Tshirt.name = "Test"

        dump = json.dumps(new_Tshirt.toJSON())

        return dump
    except Exception as e:
        return {"Exception": str(e)}


@app.route('/api/Products/TShirt', methods=['GET', 'POST'])
def api_TShirts():
    pass


@app.route('/api/TShirts/<tshirt_id>', methods=['GET', 'PUT', 'DELETE'])
def db_each_TShirt(tshirt_id):
    pass


if __name__ == '__main__':
    app.run(port=7777)
