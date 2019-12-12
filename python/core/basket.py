import uuid

from python.core.inventory import Inventory


class BasketDoesNotExistException(Exception):
    """
    Basket code not found -> Integrity Error
    """
    def __init__(self):
        pass


class BasketItem(object):
    """
    This item is a basket representation.

    code: uuid. Unique identifier for a basket
    products: list of products in the basket
    """
    code = None
    _products = None

    def __init__(self, code):
        self.code = code
        self._products = []

    def add_to_basket(self, item):
        """
        Add new item/product to the basket

        item: Product item
        return:
        """
        self._products.append(item)

    def remove_from_basket(self, item):
        """
        Remove item from the basket

        item: Product item
        return:
        """
        self._products.pop(item)

    def get_products(self):
        """
        Returns all the codes of all items inside the basket

        return: Array of codes (str)
        """
        return [item.code for item in self._products]

    def total_amount(self):
        """
        Returns the full price of the basket based on the price of every product and applying the discounts

        return: total price of all products - discounts (float)
        """
        full_price = sum(item.price for item in self._products) if self._products else 0.0
        return full_price - self._get_discount()

    def _get_discount(self):
        """
        Based on the products in the basket and discounts logic, calculates the discount

        TODO: This function is too specific and not flexible. Refactor needed

        return: total discount (float)
        """

        # For every 2 PENS, one free discount
        number_of_pens = len([x for x in self._products if x.code == 'PEN'])
        discount = 5.0 * int(number_of_pens / 2)

        # If there are more than 3 T-Shirts in the basket, 5 EUR of discount in every of them (25%)
        number_of_tshirts = len([x for x in self._products if x.code == 'TSHIRT'])
        if number_of_tshirts >= 3:
            discount += 5.0 * number_of_tshirts

        return discount

    @classmethod
    def create(cls):
        """
        Creates and empty basket with an auto generated UUID as code
        """
        return BasketItem(code=str(uuid.uuid4()))


class BasketManager(object):
    """
    Handles all baskets

    inventory: list of available products
    baskets: list of all baskets
    """
    _inventory = None
    _baskets = None

    def __init__(self, data_file_path):
        """
        Constructor. Loads all products in the inventory and initializes the baskets container
        """
        self._inventory = Inventory(data_file_path)
        self._baskets = {}

    def create(self):
        """
        Adds a new basket and returns the code for future location

        return: UUID
        """
        item = BasketItem.create()
        self._baskets[item.code] = item
        return item.code

    def remove(self, code):
        """
        Removes a basket.

        code: UUID to locate the basket to remove

        return:
        """
        if code not in self._baskets:
            raise BasketDoesNotExistException()

        self._baskets.pop(code)

    def add_product(self, code, product_code):
        """
        Add a product from the inventory to a basket

        code: UUID/code of the basket
        product_code: code of the product to add

        return:
        """
        if code not in self._baskets:
            raise BasketDoesNotExistException()

        self._baskets[code].add_to_basket(
            item=self._inventory.get_item_by_code(code=product_code)
        )

    def remove_product(self, code, product_code):
        """
        Removed a product from a basket

        code: UUID/code of the basket
        product_code: code of the product to add

        return:
        """
        if code not in self._baskets:
            raise BasketDoesNotExistException()

        self._baskets[code].remove_from_basket(
            item=self._inventory.get_item_by_code(code=product_code)
        )

    def get_products(self, code):
        """
        Get all code products from a basket.

        code: UUID/code of the basket

        return:
        """
        if code not in self._baskets:
            raise BasketDoesNotExistException()
        return self._baskets[code].get_products()

    def checkout(self, code):
        """
        Calculate the total value of a basket, including discounts.

        code: UUID/code of the basket

        return: float
        """
        if code not in self._baskets:
            raise BasketDoesNotExistException()

        return self._baskets[code].total_amount()
