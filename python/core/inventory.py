import json


class InventoryItemExistException(Exception):
    """
    There is an item in the Inventory with the same code -> Integrity Error
    """
    def __init__(self):
        pass


class InventoryItemDoesNotExistException(Exception):
    """
    Requested item not exists
    """
    def __init__(self):
        pass


class InventoryItem(object):
    """
    Class for items
    """
    code = None
    name = None
    price = 0

    def __init__(self, code, name, price):
        """
        Constructor
        """
        self.code = code
        self.name = name
        self.price = price

    @classmethod
    def create_item(cls, code, name, price):
        """
        Item creator. Useful if we need to adapt or format any field from the data source
        """
        formatted_price = float(price) if type(price) == str else price

        return InventoryItem(code, name, formatted_price)


class Inventory(object):
    """
    As we don't have a database, this class is a replacement
    """
    _products = None

    def __init__(self, file_path):
        """
            Reads the inventory from a file, converting every json object in an InventoryItem object.
        """
        with open(file_path) as fp:
            self._products = {
                i['code']: InventoryItem.create_item(code=i['code'], name=i['name'], price=i['price'])
                for i in json.load(fp)
            }

    def add_item(self, item):
        """
            Add new item to the inventory

            item: InventoryItem
            return: none
        """
        if item.code in self._products:
            raise InventoryItemExistException

        self._products[item.code] = item

    def get_item_by_code(self, code):
        """
            Returns an item from the inventory based on the code

            code: code
            return: InventoryItem
        """
        if code not in self._products:
            raise InventoryItemDoesNotExistException

        return self._products[code]
