from path import *

from models import *

import json

from flask import jsonify

import time


# Return all existing data
@app.route('/api/dump', methods=['GET'])
def db_get_all():
    objects = {}
    for key in models:
        objects[key] = models[key].objects()
    return jsonify(objects), 200


# Products:
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


# Adding a product based on ID to the Shopping Cart
# Beta version, uses the cart-ID which could be circumvented by session management
@app.route('/api/cart/add/<group>/<ID>/<cart_id>/<amount>', methods=['GET', 'POST'])
def db_cart_add(group: str, ID: str, cart_id: str, amount: int):
    product = json.loads(Storage.objects(product=group, id=ID).to_json())
    if product.__len__() == 0:
        return "No product with that ID found", 404
    else:
        cart = json.loads(Cart.objects(id=cart_id).to_json())
        if cart.__len__() == 0:
            new_cart = Cart()
            new_cart.__setattr__(ID, int(amount))
            new_cart.save()
            return "New Cart created", 201
        else:
            if ID in cart[0].keys():
                Cart.objects(id=cart_id).update(**{ID: int(cart[0][ID]) + int(amount)})
            else:
                Cart.objects(id=cart_id).update(upsert=True, **{ID: int(amount)})
            return "Cart updated", 202


# For clearing the entire cart
# In 2.0: Method to only clear specific items
@app.route('/api/cart/nuke/<cart_id>', methods=['GET', 'POST'])
def db_nuke_cart(cart_id: str):
    Cart.objects(id=cart_id).delete()
    return "Cart deleted", 300


# For Placing an Order as a Guest (Only option to place orders in 1.0)
# Shipment data is passed as a string in the API-Call, this could be optimized
@app.route('/api/order/guest/<cart_id>/<data>', methods=['GET', 'POST'])
def db_guest_order(cart_id: str, data: str):
    cart = json.loads(Cart.objects(id=cart_id).to_json())[0]

    # changing the storage amounts for all ordered items (2.0 feature)

    # Placing the Order
    new_order = Order()
    new_order.shipment_data = data
    new_order.order_time = time.time()
    new_order.items = cart["items"]
    new_order.save()

    # Deleting the cart
    #Cart.objects(id=cart_id).delete()
    return "Order created", 200


# Version 2.0
# Order from Supplier
@app.route('/test/<group>/<parameters>', methods=['GET', 'POST'])
def test_func(group: str, parameters: str):
    products = json.loads(Product.objects.only(group).to_json())


# Registration
# Login/Authentication
# User Profile
# Order as User


# Optional
# Last Change on Database


if __name__ == '__main__':
    app.run(port=7777)
