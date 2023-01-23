from flask import Flask
from flask_mongoengine import MongoEngine
import json
import time


app = Flask(__name__)


DB_URI = ""
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine(app)


@app.route('/', methods=['GET'])
def home_page():
    data_set = {'Page': 'Home', 'Message': 'Successfully loaded', 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)

    return json_dump


class TShirt(db.Document):
    tshirt_id = int
    name = ""


@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    pass


@app.route('/api/Products/TShirt', methods=['GET', 'POST'])
def api_TShirts():
    pass


@app.route('/api/TShirts/<tshirt_id>', methods=['GET', 'PUT', 'DELETE'])
def db_each_TShirt(tshirt_id):
    pass


if __name__ == '__main__':
    app.run(port=7777)
