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

    def get_products(self):
        return [item.code for item in self._products]

    def total_amount(self):
        full_price = sum(item.price for item in self._products)
        return full_price - self._get_discount()

    def _get_discount(self):
        number_of_pens = len([x for x in self._products if x.code == 'PEN'])
        number_of_tshirts = len([x for x in self._products if x.code == 'TSHIRT'])

        discount = 5.0 * int(number_of_pens / 2)

        if number_of_tshirts >= 3:
            discount += 5.0 * number_of_tshirts

        return discount

    @classmethod
    def create(cls):
        return BasketItem(code=str(uuid.uuid4()))


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
