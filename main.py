import random

class Order:
    def __init__(self, id, price, symbol, timestamp):
        self.id = id
        self.price = price
        self.symbol = symbol
        self.timestamp = timestamp


def random_order() -> Order:
    return Order(random.randrange(100), random.randint(100, 150), 0, 0)


def main():
    random_order()
    pass


if __name__ == '__main__':
    main()













