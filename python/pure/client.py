import socket
from python.core.messages import MessageManager, Message


class Client(object):
    sock = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _send_message(self, message_str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(message_str.encode())
            return s.recv(1024).decode()

    def send_create_basket_message(self):
        message = MessageManager.create_basket_message(basket_code=None)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.content['basket_code']

    def send_remove_basket_message(self, basket_code):
        message = MessageManager.remove_basket_message(basket_code)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.serialize()

    def send_add_product(self, basket_code, product_code):
        message = MessageManager.add_product_message(
            basket_code=basket_code,
            product_code=product_code
        )
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.serialize()

    def send_get_products_message(self, basket_code):
        message = MessageManager.get_products_message(basket_code=basket_code)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.content['products']

    def send_get_checkout_message(self, basket_code):
        message = MessageManager.get_checkout_message(basket_code=basket_code)
        message_response = Message.deserialize(self._send_message(message.serialize()))

        return message_response.content['total']

    def close(self):
        if self.sock:
            self.sock.close()


test_cases = [
    ['PEN', 'TSHIRT', 'MUG'],
    ['PEN', 'TSHIRT', 'PEN'],
    ['TSHIRT', 'TSHIRT', 'TSHIRT', 'PEN', 'TSHIRT'],
    ['PEN', 'TSHIRT', 'PEN', 'PEN', 'MUG', 'TSHIRT', 'TSHIRT'],
]

if __name__ == "__main__":
    client = Client('127.0.0.1', 65432)

    for t in test_cases:
        # GET BASKET CODE
        basket_code = client.send_create_basket_message()

        # ADD PRODUCTS
        for product_code in t:
            client.send_add_product(basket_code, product_code)

        # CHECKOUT
        print(f'Items: {client.send_get_products_message(basket_code)}')
        print(f'Total: {client.send_get_checkout_message(basket_code)} EUR')

        # CLOSING BASKET
        client.send_remove_basket_message(basket_code)

    client.close()
