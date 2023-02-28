import random
from typing import Final
import time
from enum import Enum, auto
from queue import PQueue

start_run = time.time()


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
    buy = PQueue(
        lambda new, old:
        (new['price'] < old['price']) or (new['price'] == old['price'] and new['timestamp'] < old['timestamp'])
    )
    sell = PQueue(
        lambda new, old:
        (new['price'] > old['price']) or (new['price'] == old['price'] and new['timestamp'] < old['timestamp'])
    )

    n = 5
    for trans in incoming():
        if trans.is_buy:
            buy.push(trans, {'price': trans.price, 'timestamp': trans.timestamp})
        else:
            sell.push(trans, {'price': trans.price, 'timestamp': trans.timestamp})

        end_run = time.time()
        time_final = end_run - start_run
        if time_final >= n:
            n += 5
            length_min = min(len(buy) // 2, len(sell) // 2)
            for i in range(length_min):
                print(sell.pop(), buy.pop())


if __name__ == '__main__':
    main()
