import json


class Message(object):
    INVALID_CODE_MESSAGE = -1
    ACK_MESSAGE = 0

    CREATE_BASKET_MESSAGE = 1
    REMOVE_BASKET_MESSAGE = 2

    ADD_PRODUCT_MESSAGE = 3
    REMOVE_PRODUCT_MESSAGE = 4

    GET_PRODUCTS_MESSAGE = 5

    code = 0
    content = None

    def __init__(self, code, content):
        self.code = code
        self.content = content

    def serialize(self):
        return json.dumps(
            {
                'code': self.code,
                'content': self.content
            }
        )

    @classmethod
    def deserialize(cls, s):
        json_obj = json.loads(s)
        return Message(
            code=json_obj['code'],
            content=json_obj['content']
        )


class MessageManager(object):
    @classmethod
    def create_ack_message(cls):
        return Message(
            code=Message.ACK_MESSAGE,
            content=None
        )

    @classmethod
    def create_invalid_message(cls):
        return Message(
            code=Message.INVALID_CODE_MESSAGE,
            content=None
        )

    @classmethod
    def create_basket_message(cls, basket_code):
        return Message(
            code=Message.CREATE_BASKET_MESSAGE,
            content={
                'basket_code': basket_code
            }
        )

    @classmethod
    def remove_basket_message(cls, basket_code):
        return Message(
            code=Message.REMOVE_BASKET_MESSAGE,
            content={
                'basket_code': basket_code
            }
        )

    @classmethod
    def add_product_message(cls, basket_code, product_code):
        return Message(
            code=Message.ADD_PRODUCT_MESSAGE,
            content={
                'basket_code': basket_code,
                'product_code': product_code
            }
        )

    @classmethod
    def remove_product_message(cls, basket_code, product_code):
        return Message(
            code=Message.REMOVE_PRODUCT_MESSAGE,
            content={
                'basket_code': basket_code,
                'product_code': product_code
            }
        )

    @classmethod
    def get_products_message(cls, basket_code=None, products=None):
        return Message(
            code=Message.GET_PRODUCTS_MESSAGE,
            content={
                'basket_code': basket_code,
                'products': products
            }
        )
