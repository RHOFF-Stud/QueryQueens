from path import *

from models import *

import json

from flask import jsonify

import time

@app.route('/api')
def helloWorld():
    return "I'm fine!"

@app.route('/api/testing', methods=['GET'])
def testreturn():
    return "testing"

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
@app.route('/api/cart/add/<group>/<ID>/<amount>', methods=['GET', 'POST'])
@app.route('/api/cart/add/<group>/<ID>/<amount>/<cart_id>', methods=['GET', 'POST'])
def db_cart_add(group: str, ID: str, cart_id: str, amount: int):
    product = json.loads(Product.objects(product=group, id=ID).to_json())
    if product.__len__() == 0:
        return "No product with that ID found", 404
    else:
        if cart_id is not None:
            cart = json.loads(Cart.objects(id=cart_id).to_json())
            if cart.__len__() == 0:
                new_cart = Cart()
                new_cart.__setattr__(ID, int(amount))
                new_cart.save()
                Log.objects().update(upsert=True, **{"Last": time.time()})
                return "New Cart created", 201
            else:
                if ID in cart[0].keys():
                    Cart.objects(id=cart_id).update(**{ID: int(cart[0][ID]) + int(amount)})
                    Log.objects().update(upsert=True, **{"Last": time.time()})
                else:
                    Cart.objects(id=cart_id).update(upsert=True, **{ID: int(amount)})
                    Log.objects().update(upsert=True, **{"Last": time.time()})
                return "Cart updated",
        else:
            new_cart = Cart()
            new_cart.__setattr__(ID, int(amount))
            new_cart.save()
            Log.objects().update(upsert=True, **{"Last": time.time()})
            return "New Cart created", 201


# For clearing the entire cart
# In 2.0: Method to only clear specific items
@app.route('/api/cart/nuke/<cart_id>', methods=['GET', 'POST'])
def db_nuke_cart(cart_id: str):
    Cart.objects(id=cart_id).delete()
    return "Cart deleted", 300


# For Placing an Order as a Guest
# Shipment data is passed as a string in the API-Call, this could be optimized
@app.route('/api/order/guest/<cart_id>/<data>', methods=['GET', 'POST'])
def db_guest_order(cart_id: str, data: str):
    cart = json.loads(Cart.objects(id=cart_id).fields(id=0).to_json())

    if cart.__len__() == 0:
        return "Cart not found", 404
    else:
        for entry in cart[0]:
            product = json.loads(Product.objects(id=entry).to_json())[0]
            Product.objects(id=entry).update(**{"amount": product["amount"] - cart[0][entry]})

        # Placing the Order (Missing price calculation)
        new_order = Order()
        new_order.shipment_data = data
        new_order.order_time = time.time()
        new_order.items = cart[0]
        new_order.save()
        Log.objects().update(upsert=True, **{"Last": time.time()})

        # Deleting the cart
        Cart.objects(id=cart_id).delete()
        return "Order created", 200


# Version 2.0
# create a new user with the given username nad password
@app.route('/api/user/create/<username>/<password>', methods=['GET', 'POST'])
def user_create(username: str, password: str):
    user = json.loads(User.objects(username=username).to_json())
    if user.__len__() == 0:
        new_user = User()
        new_user.username = username
        new_user.password = password
        new_user.save()
        Log.objects().update(upsert=True, **{"Last": time.time()})
        return "User created", 200
    else:
        return "User with that username already exists", 403


# Match the given username and password to ones in the database
@app.route('/api/user/authenticate/<username>/<password>', methods=['GET', 'POST'])
def user_authenticate(username: str, password: str):
    user = json.loads(User.objects(username=username).to_json())

    if user.__len__() == 0:
        return "No User with that Username was found", 404
    else:
        if user[0]["password"] == password:
            return "User authenticated", 200
        else:
            return "Incorrect password", 402


# Return all user data except their password
@app.route('/api/user/data/<username>', methods=['GET', 'POST'])
def user_data(username: str):
    user = User.objects(username=username).fields(password=0, id=0)
    return jsonify(user)


# Optional
# Last Change on Database
@app.route('/api/log/last', methods=['GET', 'POST'])
def lastcall():
    last_call = Log.objects().fields(id=0)
    return jsonify(last_call)

# Order from Supplier
# Order as User


if __name__ == '__main__':
    app.run(port=7777)
