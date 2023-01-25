from path import *

from models import *

import json
import time


@app.route('/api/db_populate', methods=['GET', 'POST'])
def db_populate():
    try:
        with open("preconfig_data.json", "r") as d:
            data = json.load(d)
            for o in data:
                try:
                    for t in o["TShirts"]:
                        new_shirt = TShirt(**t)
                        new_shirt.save()
                        dump = json.dumps(new_shirt.toJSON())

                    return dump
                except Exception as e:
                    return {"Exception": str(e)}
    finally:
        pass


@app.route('/api/Products/TShirt', methods=['GET', 'POST'])
def api_TShirts():
    pass


@app.route('/api/TShirts/<tshirt_id>', methods=['GET', 'PUT', 'DELETE'])
def db_each_TShirt(tshirt_id):
    pass


if __name__ == '__main__':
    app.run(port=7777)
