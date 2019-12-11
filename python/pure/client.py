# coding: utf-8
import argparse

import socket
from python.core.messages import MessageManager, Message


class Client(object):
    """
    Class to create a connection and send messages to a server listening in Host and Port.
    """
    host = None
    port = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _send_message(self, message_str):
        """
        Helper to send messages to the server. Also receives the answer from the server.

        message_str: json string
        return: json string
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(message_str.encode())
            return s.recv(1024).decode()

    def send_create_basket_message(self):
        """
        Send a create basket message.

        return: basket code (uuid)
        """
        message = MessageManager.create_basket_message(basket_code=None)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.content['basket_code']

    def send_remove_basket_message(self, basket_code):
        """
        Send a remove basket message

        basket_code: uuid
        return: Message object
        """
        message = MessageManager.remove_basket_message(basket_code)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.serialize()

    def send_add_product(self, basket_code, product_code):
        """
        Send an add product to basket message

        basket_code: uuid
        product_code: Code of a products (str)
        return: Message object
        """
        message = MessageManager.add_product_message(
            basket_code=basket_code,
            product_code=product_code
        )
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.serialize()

    def send_get_products_message(self, basket_code):
        """
        Send a get products from a basket message

        basket_code: uuid

        return: Message object
        """
        message = MessageManager.get_products_message(basket_code=basket_code)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.content['products']

    def send_get_checkout_message(self, basket_code):
        """
        Send a get checkout from a basket message

        basket_code: uuid
        return: total value (float)
        """
        message = MessageManager.get_checkout_message(basket_code=basket_code)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.content['total']


test_cases = [
    ['PEN', 'TSHIRT', 'MUG'],
    ['PEN', 'TSHIRT', 'PEN'],
    ['TSHIRT', 'TSHIRT', 'TSHIRT', 'PEN', 'TSHIRT'],
    ['PEN', 'TSHIRT', 'PEN', 'PEN', 'MUG', 'TSHIRT', 'TSHIRT'],
]


def main(**params):
    host = params.get('host')
    port = int(params.get('port'))

    client = Client(host=host, port=port)

    for t in test_cases:
        # GET BASKET CODE
        basket_code = client.send_create_basket_message()

        # ADD PRODUCTS
        for product_code in t:
            client.send_add_product(basket_code, product_code)

        # CHECKOUT
        products_str = ', '.join(client.send_get_products_message(basket_code))
        print(f'Items: {products_str}')
        print(f'Total: {client.send_get_checkout_message(basket_code)}€\n')

        # CLOSING BASKET
        client.send_remove_basket_message(basket_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pure Python Client", add_help=False)
    parser.add_argument(
        "-h", "--host", help="Host where the server is listening. Default: 127.0.0.1",
        required=False, default='127.0.0.1'
    )
    parser.add_argument(
        "-p", "--port", help="Port where the server is listening. Default: 65432",
        required=False,
        default=65432
    )
    parser.set_defaults(local_mode=False)

    args = parser.parse_args()
    main(**vars(args))
