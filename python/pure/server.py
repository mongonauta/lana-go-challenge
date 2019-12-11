# coding: utf-8
import argparse
import socket

from python.core.basket import BasketManager
from python.core.messages import Message, MessageManager


class Server(object):
    """
    The Server.

    Accepts connections by socket and listen the messages in host + port.

    In addition to that, keep the BasketManager control (a database)

    TODO: Multi-threading. Currently, only one message is handled.
    """
    host = None
    port = None
    sock = None
    manager = None

    def __init__(self, inventory_path, host, port):
        self.host = host
        self.port = port
        self.manager = BasketManager(data_file_path=inventory_path)

    def listen(self):
        print(f'Listening in {self.host}:{self.port}...\n\n')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))

            while True:
                sock.listen()
                conn, addr = sock.accept()

                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            raise Exception('Client disconnected')

                        print(f'Received: {data}')

                        try:
                            message_resp = self.message_handler(message=Message.deserialize(data))
                        except:
                            message_resp = MessageManager.create_invalid_message()

                        conn.sendall(str.encode(f'{message_resp.serialize()}'))

                        break

    def message_handler(self, message):
        """
        Message handler. Translate every received message in a valid manager action and returns a valid message
        with the response of the action.

        message: MessageItem object
        return: MessageItem object
        """
        if message.code == Message.CREATE_BASKET_MESSAGE:
            basket_code = self.manager.create()
            return MessageManager.create_basket_message(basket_code)

        if message.code == Message.REMOVE_BASKET_MESSAGE:
            basket_code = message.content['basket_code']
            self.manager.remove(basket_code)
            return MessageManager.create_ack_message()

        if message.code == Message.ADD_PRODUCT_MESSAGE:
            basket_code = message.content['basket_code']
            product_code = message.content['product_code']

            self.manager.add_product(basket_code, product_code)
            return MessageManager.create_ack_message()

        if message.code == Message.REMOVE_PRODUCT_MESSAGE:
            basket_code = message.content['basket_code']
            product_code = message.content['product_code']

            self.manager.remove_product(basket_code, product_code)
            return MessageManager.create_ack_message()

        if message.code == Message.GET_PRODUCTS_MESSAGE:
            basket_code = message.content['basket_code']
            products = self.manager.get_products(basket_code)

            return MessageManager.get_products_message(products=products)

        if message.code == Message.GET_CHECKOUT_MESSAGE:
            basket_code = message.content['basket_code']
            total = self.manager.checkout(basket_code)

            return MessageManager.get_checkout_message(total=total)

        return MessageManager.create_invalid_message()


def main(**params):
    inventory_path = params.get('inventory', None)
    host = params.get('host')
    port = int(params.get('port'))

    Server(inventory_path=inventory_path, host=host, port=port).listen()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pure Python server", add_help=False)
    parser.add_argument("-i", "--inventory", help="Path to JSON inventory file", required=True)
    parser.add_argument(
        "-h", "--host", help="Host where the server must listen. Default: 127.0.0.1",
        required=False, default='127.0.0.1'
    )
    parser.add_argument(
        "-p", "--port", help="Port the server must listen. Default: 65432",
        required=False,
        default=65432
    )
    parser.set_defaults(local_mode=False)

    args = parser.parse_args()
    main(**vars(args))
