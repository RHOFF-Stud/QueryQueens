import json

from path import db


class DataObject:
    def toJSON(self):
        dump = json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
        return json.loads(dump)

    def __init__(self):
        pass


class TShirt(DataObject, db.Document):
    def __init__(self, ID: int, name: str):
        super().__init__()
        self.tshirt_id = ID
        self.name = name
