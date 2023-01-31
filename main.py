from path import *

from models import *

import json

from flask import jsonify

import time


@app.route('/api')
def helloWorld():
    return "I'm fine!"


@app.route('/api/test', methods=['GET'])
def test_return():
    return "test"


# For initial data population based on a preconfigured data set
# not for production
@app.route('/api/populate', methods=['GET', 'POST'])
def db_populate():
    try:
        with open("preconfig_data.json", "r") as config_file:
            data = json.load(config_file)
            for collection in data:
                for model in data[collection]:
                    new_doc = models[model]()
                    for key in model:
                        new_doc.__setattr__(key, model[key])
                    new_doc.save()
            config_file.close()
        return "Saved successfully"
    except Exception as e:
        return str(e), 400


# Return all existing data
@app.route('/api/dump', methods=['GET'])
def db_get_all():
    try:
        objects = {}
        for key in models:
            objects[key] = models[key].objects()
        return jsonify(objects), 200
    except Exception as e:
        return str(e), 400


# Products:
# Return all existing Products
@app.route('/api/product', methods=['GET'])
# Return a subset of all existing Products based on a set of parameters as follows:
# color=black&size=medium&type=regular...
@app.route('/api/product/<parameters>', methods=['GET'])
def db_get_products(parameters: str):
    try:
        if parameters is None:
            products = Product.objects()
            return jsonify(products), 200
        else:
            if parameters.find("&") < 0:
                param_list = [parameters]
            else:
                param_list = parameters.split("&")
            param_dict = {}
            for param in param_list:
                param_key, param_value = param.split("=")
                param_dict[param_key] = param_value
            products = Product.objects(**param_dict)
            return jsonify(products), 200
    except Exception as e:
        return str(e), 400


# Adding a product based on ID to the Shopping Cart
# Beta version, uses the cart-ID which could be circumvented by session management
@app.route('/api/cart/add/<group>/<ID>/<amount>', methods=['GET', 'POST'])
@app.route('/api/cart/add/<group>/<ID>/<amount>/<cart_id>', methods=['GET', 'POST'])
def db_cart_add(group: str, ID: str, cart_id: str, amount: int):
    try:
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
    except Exception as e:
        return str(e), 400


# For clearing the entire cart
# In 2.0: Method to only clear specific items
@app.route('/api/cart/nuke/<cart_id>', methods=['GET', 'POST'])
def db_nuke_cart(cart_id: str):
    try:
        Cart.objects(id=cart_id).delete()
        return "Cart deleted", 202
    except Exception as e:
        return str(e), 400


# For Placing an Order as a Guest
# Shipment data is passed as a string in the API-Call, this could be optimized
@app.route('/api/order/guest/<cart_id>/<data>', methods=['GET', 'POST'])
def db_guest_order(cart_id: str, data: str):
    try:
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
            return "Order created", 201
    except Exception as e:
        return str(e), 400


# Version 2.0
# create a new user with the given username nad password
@app.route('/api/user/create/<username>/<password>', methods=['GET', 'POST'])
def user_create(username: str, password: str):
    try:
        user = json.loads(User.objects(username=username).to_json())
        if user.__len__() == 0:
            new_user = User()
            new_user.username = username
            new_user.password = password
            new_user.save()
            Log.objects().update(upsert=True, **{"Last": time.time()})
            return "User created", 201
        else:
            return "User with that username already exists", 409
    except Exception as e:
        return str(e), 400


# Match the given username and password to ones in the database
@app.route('/api/user/authenticate/<username>/<password>', methods=['GET', 'POST'])
def user_authenticate(username: str, password: str):
    try:
        user = json.loads(User.objects(username=username).to_json())

        if user.__len__() == 0:
            return "No User with that Username was found", 404
        else:
            if user[0]["password"] == password:
                return "User authenticated", 200
            else:
                return "Incorrect password", 401
    except Exception as e:
        return str(e), 400


# Return all user data except their password
@app.route('/api/user/data/<username>', methods=['GET', 'POST'])
def user_data(username: str):
    try:
        user = User.objects(username=username).fields(password=0, id=0)
        return jsonify(user), 200
    except Exception as e:
        return str(e), 400


# Last Change on Database
@app.route('/api/log/last', methods=['GET', 'POST'])
def last_call():
    try:
        last = Log.objects().fields(id=0)
        return jsonify(last)
    except Exception as e:
        return str(e), 400

# Delete User
# Change User Data
# Order as User


if __name__ == '__main__':
    app.run(port=7777)
