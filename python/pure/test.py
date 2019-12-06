from python.core.basket import BasketManager

"""
Items: PEN, TSHIRT, MUG
Total: 32.50€

Items: PEN, TSHIRT, PEN
Total: 25.00€

Items: TSHIRT, TSHIRT, TSHIRT, PEN, TSHIRT
Total: 65.00€

Items: PEN, TSHIRT, PEN, PEN, MUG, TSHIRT, TSHIRT
Total: 62.50€
"""

test_cases = [
    ['PEN', 'TSHIRT', 'MUG'],
    ['PEN', 'TSHIRT', 'PEN'],
    ['TSHIRT', 'TSHIRT', 'TSHIRT', 'PEN', 'TSHIRT'],
    ['PEN', 'TSHIRT', 'PEN', 'PEN', 'MUG', 'TSHIRT', 'TSHIRT'],
]

manager = BasketManager(data_file_path='/Users/jose/Development/lana-go-challenge/data/products.json')

for t in test_cases:
    basket_code = manager.create()

    for product_code in t:
        manager.add_product(basket_code, product_code)

    print(f'Items: {manager.get_products(basket_code)}')
    print(f'Total: {manager.checkout(basket_code)} EUR')

    manager.remove(basket_code)
