import json


products = [
    {
        'code': 'PEN',
        'name': 'Lana Pen',
        'price': 5.00
    },
    {
        'code': 'TSHIRT',
        'name': 'Lana T-Shirt',
        'price': 20.00
    },
    {
        'code': 'MUG',
        'name': 'Lana Coffee Mug',
        'price': 7.50
    }
]

with open('../data/products.json', 'w') as fp:
    json.dump(products, fp)
