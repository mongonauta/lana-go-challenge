import json


class Message(object):
    """
    This class tries to be a helper to keep consistent between client and servers of the app.

    The app only understand this class objects BUT, using the serializers, we can use the objects in sockets, APIs...
    """
    INVALID_CODE_MESSAGE = -1
    ACK_MESSAGE = 0

    CREATE_BASKET_MESSAGE = 1
    REMOVE_BASKET_MESSAGE = 2

    ADD_PRODUCT_MESSAGE = 3
    REMOVE_PRODUCT_MESSAGE = 4

    GET_PRODUCTS_MESSAGE = 5
    GET_CHECKOUT_MESSAGE = 6

    code = 0
    content = None

    def __init__(self, code, content):
        """
        Constructor. Every message must have a valid code and a content, different from every type of message.

        code: valid message code. int
        content: content of the message. Can be whatever BUT must be json serializable.
        """
        self.code = code
        self.content = content

    def serialize(self):
        """
        Transforms the message in a valid JSON string

        return: json str
        """
        return json.dumps(
            {
                'code': self.code,
                'content': self.content
            }
        )

    @classmethod
    def deserialize(cls, s):
        """
        Transform a valid json (with the right format) in a Message object.

        s: json str

        return: Message
        """
        json_obj = json.loads(s)
        return Message(
            code=json_obj['code'],
            content=json_obj['content']
        )


class MessageManager(object):
    """
    Helper manager to create right Message objects
    """
    @classmethod
    def create_ack_message(cls):
        """
        Confirmation Message

        return: Message object
        """
        return Message(
            code=Message.ACK_MESSAGE,
            content=None
        )

    @classmethod
    def create_invalid_message(cls):
        """
        Invalid code Message

        return: Message object
        """
        return Message(
            code=Message.INVALID_CODE_MESSAGE,
            content=None
        )

    @classmethod
    def create_basket_message(cls, basket_code=None):
        """
        Create a *create basket* Message.
        - If *basket_code* is None, is a client request.
        - If *basket_code* has a value, is a server response.

        basket_code: UUID

        return: Message object
        """
        return Message(
            code=Message.CREATE_BASKET_MESSAGE,
            content={
                'basket_code': basket_code
            }
        )

    @classmethod
    def remove_basket_message(cls, basket_code):
        """
        Create a *remove basket* Message.

        basket_code: UUID

        return: Message object
        """
        return Message(
            code=Message.REMOVE_BASKET_MESSAGE,
            content={
                'basket_code': basket_code
            }
        )

    @classmethod
    def add_product_message(cls, basket_code, product_code):
        """
        Create a *add product to basket* Message.

        basket_code: UUID
        product_code: Code of a product (str)

        return: Message object
        """
        return Message(
            code=Message.ADD_PRODUCT_MESSAGE,
            content={
                'basket_code': basket_code,
                'product_code': product_code
            }
        )

    @classmethod
    def remove_product_message(cls, basket_code, product_code):
        """
        Create a *remove product from a basket* Message.

        basket_code: UUID
        product_code: Code of a product (str)

        return: Message object
        """
        return Message(
            code=Message.REMOVE_PRODUCT_MESSAGE,
            content={
                'basket_code': basket_code,
                'product_code': product_code
            }
        )

    @classmethod
    def get_products_message(cls, basket_code=None, products=None):
        """
        Create a *get products from a basket* Message.

        - If *basket_code* has a value, is a client request and products is ignored.
        - If *basket_code* is null, is the response of the server and products will have values.

        basket_code: UUID
        products: List of codes from all products inside a basket (array of str)

        return: Message object
        """
        return Message(
            code=Message.GET_PRODUCTS_MESSAGE,
            content={
                'basket_code': basket_code,
                'products': products
            }
        )

    @classmethod
    def get_checkout_message(cls, basket_code=None, total=None):
        """
        Create a *get checkout from a basket* Message.

        - If *basket_code* has a value, is a client request and total is ignored.
        - If *basket_code* is null, is the response of the server and total will have value.

        basket_code: UUID
        total: Total value of all products inside the basket (float)

        return: Message object
        """
        return Message(
            code=Message.GET_CHECKOUT_MESSAGE,
            content={
                'basket_code': basket_code,
                'total': total
            }
        )
