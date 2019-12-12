import json
import os

from flask import Flask, jsonify, request
from functools import wraps

from python.core.basket import BasketManager
from python.core.messages import MessageManager

app = Flask(__name__)

manager = BasketManager(
    data_file_path=os.getenv('INVENTORY')
)


def message_to_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        return jsonify(
            json.loads(
                f(*args, **kw).serialize()
            )
        )
    return wrapper


@app.route("/create_basket/", methods=['GET'])
@message_to_json
def create_basket():
    basket_code = manager.create()
    return MessageManager.create_basket_message(basket_code)


@app.route("/remove_basket/<basket_code>/", methods=['GET'])
@message_to_json
def remove_basket(basket_code):
    manager.remove(basket_code)
    return MessageManager.create_ack_message()


@app.route("/add_product/<basket_code>/<product_code>/", methods=['GET'])
@message_to_json
def add_product(basket_code, product_code):
    manager.add_product(basket_code, product_code)
    return MessageManager.create_ack_message()


@app.route("/remove_product/<basket_code>/<product_code>/", methods=['GET'])
@message_to_json
def remove_product(basket_code, product_code):
    manager.remove_product(basket_code, product_code)
    return MessageManager.create_ack_message()


@app.route("/get_products/<basket_code>/", methods=['GET'])
@message_to_json
def get_products(basket_code):
    products = manager.get_products(basket_code)
    return MessageManager.get_products_message(products=products)


@app.route("/checkout/<basket_code>/", methods=['GET'])
@message_to_json
def checkout(basket_code):
    total = manager.checkout(basket_code)
    return MessageManager.get_checkout_message(total=total)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '404 Not Found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
