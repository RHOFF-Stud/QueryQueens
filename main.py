from path import *

from models import *

import json

from flask import jsonify

import time


# For initial data population based on a preconfigured data set
@app.route('/api/db_populate', methods=['GET', 'POST'])
def db_populate():
    with open("preconfig_data.json", "r") as config_file:
        data = json.load(config_file)
        for collection in data:
            if collection == "Customer":
                for customer in data[collection]:
                    new_customer = Customer()
                    for key in customer:
                        new_customer.__setattr__(key, customer[key])
                    new_customer.save()

            if collection == "Product":
                for product in data[collection]:
                    new_product = Product()
                    for key in product:
                        new_product.__setattr__(key, product[key])
                    new_product.save()

            if collection == "Storage":
                for storage in data[collection]:
                    new_storage = Storage()
                    for key in storage:
                        new_storage.__setattr__(key, storage[key])
                    new_storage.save()

            if collection == "Supplier":
                for supplier in data[collection]:
                    new_supplier = Supplier()
                    for key in supplier:
                        new_supplier.__setattr__(key, supplier[key])
                    new_supplier.save()
        config_file.close()
    return "Saved successfully"


# Return of the full set or subset of all existing TShirts
@app.route('/api/Products/TShirt', methods=['GET'])
def db_get_product_tshirt():
    tshirts = Product.objects.only('TShirt')
    return jsonify(tshirts), 200


# Return of a specific TShirt based on ID
@app.route('/api/TShirts/<tshirt_id>', methods=['GET', 'PUT', 'DELETE'])
def db_each_TShirt(tshirt_id):
    pass


if __name__ == '__main__':
    app.run(port=7777)
