# coding: utf-8
import argparse
import requests


class HTTPClient(object):
    host = None
    port = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _get_url(self, end_point, params=None):
        url = f'http://{self.host}:{self.port}/{end_point}/'
        if params:
            url += '/'.join(params) + '/'

        return url

    def _send_message(self, action, params=None):
        return requests.get(self._get_url(end_point=action, params=params)).json()

    def send_create_basket_message(self):
        """
        Send a create basket message.

        return: basket code (uuid)
        """
        message_response = self._send_message(action='create_basket', params=None)
        return message_response['content']['basket_code']

    def send_remove_basket_message(self, basket_code):
        """
        Send a remove basket message

        basket_code: uuid
        return: Message object
        """
        return self._send_message(action='remove_basket', params=[basket_code])

    def send_add_product(self, basket_code, product_code):
        """
        Send an add product to basket message

        basket_code: uuid
        product_code: Code of a products (str)
        return: Message object
        """
        return self._send_message(action='add_product', params=[basket_code, product_code])

    def send_get_products_message(self, basket_code):
        """
        Send a get products from a basket message

        basket_code: uuid

        return: Message object
        """
        message_response = self._send_message(action='get_products', params=[basket_code])
        return message_response['content']['products']

    def send_get_checkout_message(self, basket_code):
        """
        Send a get checkout from a basket message

        basket_code: uuid
        return: total value (float)
        """
        message_response = self._send_message(action='checkout', params=[basket_code])
        return message_response['content']['total']


test_cases = [
    ['PEN', 'TSHIRT', 'MUG'],
    ['PEN', 'TSHIRT', 'PEN'],
    ['TSHIRT', 'TSHIRT', 'TSHIRT', 'PEN', 'TSHIRT'],
    ['PEN', 'TSHIRT', 'PEN', 'PEN', 'MUG', 'TSHIRT', 'TSHIRT'],
]


def main(**params):
    host = params.get('host')
    port = int(params.get('port'))

    client = HTTPClient(host=host, port=port)

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
        "-h", "--host", help="Host where the Flask server is listening. Default: 127.0.0.1",
        required=False, default='127.0.0.1'
    )
    parser.add_argument(
        "-p", "--port", help="Port where the Flask server is listening. Default: 5000",
        required=False,
        default=5000
    )
    parser.set_defaults(local_mode=False)

    args = parser.parse_args()
    main(**vars(args))
