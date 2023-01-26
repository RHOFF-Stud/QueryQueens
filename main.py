from path import *

from models import *

import json

from flask import jsonify

import time


# For initial data population based on a preconfigured data set
# not for production
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

            if collection == "Supplier":
                for supplier in data[collection]:
                    new_supplier = Supplier()
                    for key in supplier:
                        new_supplier.__setattr__(key, supplier[key])
                    new_supplier.save()
        config_file.close()
    return "Saved successfully"


# Return all existing data
@app.route('/api/dump', methods=['GET'])
def db_get_all():
    objects = {}
    for key in models:
        objects[key] = models[key].objects()
    return jsonify(objects), 200


# Return all existing Products
@app.route('/api/product/all', methods=['GET'])
def db_get_all_products():
    products = Product.objects()
    return jsonify(products), 200


# Return a subset of all existing Products
@app.route('/api/product/<group>', methods=['GET'])
def db_get_product(group: str):
    products = Product.objects.only(group)
    return jsonify(products), 200


# 127.0.0.1:7777/api/product/TShirt/color=black&size=medium&type=regular
# Return a subset of all existing Products based on a set of parameters
@app.route('/api/product/<group>/<parameters>', methods=['GET'])
def db_get_product_parameters(group: str, parameters: str):
    products = json.loads(Product.objects.only(group).to_json())

    matches = {group: []}

    index = parameters.find("&")
    if index < 0:
        param_list = [parameters]
    else:
        param_list = parameters.split("&")

    for product in products:
        for obj in product[group]:
            param_key, param_value = param_list[0].split("=")
            for key in obj:
                if key == param_key and obj[key] == param_value:
                    matches[group].append(obj)

            if index > 0:
                for p in param_list[1:]:
                    param_key, param_value = p.split("=")
                    for match in matches[group]:
                        found_match = False
                        for key in match:
                            if key == param_key and match[key] == param_value:
                                found_match = True
                                break
                        if not found_match:
                            matches[group].remove(match)

    return jsonify(matches, 200)


# Return of a specific product based on ID
@app.route('/api/product/<group>/<id>', methods=['GET', 'PUT', 'DELETE'])
def db_each_TShirt(group: str, ID: str):
    product = Product.objects.only(group).where(object_id=ID)
    return jsonify(product), 200

# Use Cases to build:
# Last Change on Database (PROBLEMO)
# Shopping Cart
# Order as Guest
# Order as User
# Order from Supplier
# Registration
# Login/Authentication
# User Profile


if __name__ == '__main__':
    app.run(port=7777)
