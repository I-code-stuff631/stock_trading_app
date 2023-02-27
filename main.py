import random
from typing import Final
import time
from enum import Enum, auto
from queue import PQueue


class Symbol(Enum):
    AAPL = auto()
    TSLA = auto()
    MSFT = auto()
    GOOGL = auto()
    SPOT = auto()
    NFLX = auto()


class Transaction:

    # noinspection PyShadowingBuiltins
    def __init__(self, buy: bool, symbol: Symbol, price, timestamp, id: int):
        self.is_buy: Final = buy
        self.symbol: Final = symbol
        self.price: Final = price
        self.timestamp: Final = timestamp
        self.id: Final = id


def incoming():
    two_power_128: int = 2 ** 128
    while True:
        yield Transaction(
            random.randint(0, 1) == 1,
            random.choice(list(Symbol)),
            random.uniform(5, 100),
            time.time() + random.uniform(-5, 5),
            random.randrange(two_power_128),
        )


def main():
    buy = PQueue()
    sell = PQueue()
    for trans in incoming():
        if trans.is_buy:
            buy.push(trans, (trans.price, trans.timestamp))
        else:
            sell.push(trans, (trans.price, trans.timestamp))


if __name__ == '__main__':
    main()
