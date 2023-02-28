import random
from typing import Final
import time
from enum import Enum, auto
from queue import PQueue
run_time = time.time()

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
    buy_length = 0  # You don't need these anymore because PQueue now tracks its length :)
    sell_length = 0
    for trans in incoming():
        if trans.is_buy:
            buy_length += 1
            buy.push(trans, {'price': trans.price, 'timestamp': trans.timestamp})
            if buy_length == 100:
                buy.pop()
        else:
            sell.push(trans, {'price': trans.price, 'timestamp': trans.timestamp})
            sell_length += 1
            if sell_length == 100:
                sell.pop()


if __name__ == '__main__':
    main()
