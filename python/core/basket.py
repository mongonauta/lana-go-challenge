import uuid

from .inventory import Inventory


class BasketItem(object):
    code = None
    _products = None

    def __init__(self, code):
        self.code = code
        self._products = []

    def add_to_basket(self, item):
        self._products.append(item)

    def remove_from_basket(self, item):
        self._products.pop(item)

    def total_amount(self):
        return sum(item.price for item in self._products)

    def get_products(self):
        return [item.code for item in self._products]

    @classmethod
    def create(cls):
        return BasketItem(code=uuid.uuid4())


class BasketManager(object):
    _inventory = None
    _baskets = None

    def __init__(self, data_file_path):
        self._inventory = Inventory(data_file_path)
        self._baskets = {}

    def create(self):
        item = BasketItem.create()
        self._baskets[item.code] = item
        return item.code

    def remove(self, code):
        self._baskets.pop(code)

    def add_product(self, code, product_code):
        self._baskets[code].add_to_basket(
            item=self._inventory.get_item_by_code(code=product_code)
        )

    def remove_product(self, code, product_code):
        self._baskets[code].remove_from_basket(
            item=self._inventory.get_item_by_code(code=product_code)
        )

    def get_products(self, code):
        return self._baskets[code].get_products()

    def checkout(self, code):
        return self._baskets[code].total_amount()
