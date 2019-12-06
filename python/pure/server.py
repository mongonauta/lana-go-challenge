import socket

from python.core.basket import BasketManager
from python.core.messages import Message, MessageManager


class Server(object):
    host = None
    port = None
    sock = None
    manager = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.manager = BasketManager(
            data_file_path='/Users/jose/Development/lana-go-challenge/data/products.json'
        )

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

            return MessageManager.get_products_message(products)

        return MessageManager.create_invalid_message()


if __name__ == "__main__":
    Server(host='127.0.0.1', port=65432).listen()
