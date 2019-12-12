# coding: utf-8
import argparse
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


def main(**params):
    output = params.get('output')
    with open(output, 'w') as fp:
        json.dump(products, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="JSON file generator", add_help=False)
    parser.add_argument("-o", "--output", help="Path to the output file")
    parser.set_defaults(local_mode=False)

    args = parser.parse_args()
    main(**vars(args))
