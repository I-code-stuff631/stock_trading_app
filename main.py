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
            random.normalvariate(50, 1),
            time.time() + random.uniform(-5, 5),
            random.randrange(two_power_128),
        )


def main():
    buy = PQueue(
        lambda new, old:
        (new["price"] < old["price"]) or (new["price"] == old["price"] and new["timestamp"] < old["timestamp"])
    )
    sell = PQueue(
        lambda new, old:
        (new["price"] > old["price"]) or (new["price"] == old["price"] and new["timestamp"] < old["timestamp"])
    )

    start_time: float = time.time()
    for trans in incoming():
        if trans.is_buy:
            buy.push(trans, {"price": trans.price, "timestamp": trans.timestamp})
        else:
            sell.push(trans, {"price": trans.price, "timestamp": trans.timestamp})

        if (time.time() - start_time) >= 5:
            start_time = time.time()
            length_min = min(len(buy) // 2, len(sell) // 2)
            for i in range(length_min):
                sell_item: Transaction = sell.pop()
                buy_item: Transaction = buy.pop()
                fmt_str = "{buy_or_sell} {symbol} for {price}$"
                print(fmt_str.format(
                    buy_or_sell="buy" if buy_item.is_buy else "sell",
                    symbol=buy_item.symbol,
                    price=round(buy_item.price, ndigits=2)
                ), end=" and ")
                print(fmt_str.format(
                    buy_or_sell="buy" if sell_item.is_buy else "sell",
                    symbol=sell_item.symbol,
                    price=round(sell_item.price, ndigits=2)
                ))


if __name__ == '__main__':
    main()
