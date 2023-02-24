import random


class Transation:
    # noinspection PyShadowingBuiltins
    def __init__(self, price, buy: bool, timestamp, symbol: str, id: int):
        self.id = id
        self.price = price
        self.symbol = symbol
        self.timestamp = timestamp
        self.buy = buy


def random_transation():
    pass


def main():
    random_transation()


if __name__ == '__main__':
    main()
