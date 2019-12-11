# Purpose

This is a technical test proposed by Lana. The description of the test is detailed 
[here.](https://gist.github.com/samlown/17abc235580fb291dd153b9c45e441d0)

# Index

* [Description](#description)
* [Core](#core)
* [Pure Python solution](#pure_python)
* [Flask Solution](#flask)

# <a href="description"></a>Description

To solve the challenge, I tried to fins 2 solutions: one in pure python without any dependency, based on sockets,
and other using [Flask](https://palletsprojects.com/p/flask/), a lightweight python web framework.

Both uses the same core functionality so, basically, the business logic is the same but the way to handle it is
different.

# <a href="core"></a>Core

The core functionality is designed in 3 files: `basket.py`, `inventory.py` and `messages.py`.

NOTE: There is another file necessary,
[products.json](https://github.com/mongonauta/lana-go-challenge/blob/master/data/products.json) that contains the list
of available products in JSON format. This is because there is no database.


# <a href="pure_python"></a>Pure Python Solution

## Prerequisites

* Python3.7 or higher.

## How to configure and build it

NA

## How to run the server

To run the server you must use the command:

```
python pure/server.py -i ~/lana-go-challenge/data/products.json
```

The script will wait until a client send a message and will print what receives.

NOTE: Default socket configuration is `127.0.0.1:65432`. If you want to modify it, you can use `-h` and `-p` params.
For example:

```
python pure/server.py -i ~/lana-go-challenge/data/products.json -h 192.0.0.1 -p 8000
```


## How to run the client

To run the client you must use the command:

```
python pure/client.py
```

NOTE: Default socket configuration is `127.0.0.1:65432`. If you want to modify it, you can use `-h` and `-p` params.
For example:

```
python pure/client.py -h 192.0.0.1 -p 8000
```

The client has hardcoded some use tests so, the expected output should be:

```
Items: PEN, TSHIRT, MUG
Total: 32.5€

Items: PEN, TSHIRT, PEN
Total: 25.0€

Items: TSHIRT, TSHIRT, TSHIRT, PEN, TSHIRT
Total: 65.0€

Items: PEN, TSHIRT, PEN, PEN, MUG, TSHIRT, TSHIRT
Total: 62.5€
```

# <a href="pure_python"></a>Flask Solution

## Prerequisites

* Python3.7 or higher.
* Pip
* Virtualenv

## How to configure and build it

To run the Flask application, you need to create and environment and install the dependencies.

```
> virtualenv -p python3.7 venv
> source venv/bin/activate
> pip install -r requirements.txt
```

NOTE: In addition to Flask dependency, I added Requests to make client more simple.

## How to run the server

To run the server you must use the command:

```
python flask/server.py
```

and the Flask application will run and will wait in the default host and port, `http://127.0.0.1:5000`.

## How to run the client

To run the client you must use the command:

```
python flask/client.py
```

NOTE: Default Flask server configuration is `127.0.0.1:5000`. If you want to modify it, you can use `-h` and `-p` params.
For example:

```
python flask/client.py -h 192.0.0.1 -p 8000
```

The client has hardcoded some use tests so, the expected output should be:

```
Items: PEN, TSHIRT, MUG
Total: 32.5€

Items: PEN, TSHIRT, PEN
Total: 25.0€

Items: TSHIRT, TSHIRT, TSHIRT, PEN, TSHIRT
Total: 65.0€

Items: PEN, TSHIRT, PEN, PEN, MUG, TSHIRT, TSHIRT
Total: 62.5€
```