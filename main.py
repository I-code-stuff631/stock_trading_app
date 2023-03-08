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

    def __str__(self):
        return "{buy_or_sell} {symbol} for ${price}".format(
            buy_or_sell="buy" if self.is_buy else "sell",
            symbol=self.symbol,
            price=round(self.price, ndigits=2),
        )


def incoming():
    two_power_128: int = 2 ** 128
    while True:
        yield Transaction(
            random.randint(0, 1) == 1,
            random.choice(list(Symbol)),
            random.normalvariate(50, 5),
            time.time() + random.uniform(-5, 5),
            random.randrange(two_power_128),
        )


def main():
    sell = PQueue(
        lambda new, old:  # Lowest sells get priority
        (new["price"] < old["price"]) or (new["price"] == old["price"] and new["timestamp"] < old["timestamp"])
    )
    buy = PQueue(
        lambda new, old:  # Highest buys get priority
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

            sell_list: list[Transaction] = []
            buy_list: list[Transaction] = []
            for _ in range(length_min):
                sell_list.append(sell.pop())
                buy_list.append(buy.pop())

            while True:
                restart = False
                for buying_trans in buy_list:
                    matched_sell_trans = None

                    # Find matching
                    for selling_trans in sell_list:
                        if buying_trans.symbol == selling_trans.symbol and selling_trans.price <= buying_trans.price:
                            if matched_sell_trans is None:
                                matched_sell_trans = selling_trans
                            elif abs(selling_trans.price - buying_trans.price) < abs(matched_sell_trans.price - buying_trans.price):
                                matched_sell_trans = selling_trans

                    # If there is a match
                    if matched_sell_trans is not None:
                        print(buying_trans)
                        print(matched_sell_trans)
                        print()
                        buy_list.remove(buying_trans)
                        sell_list.remove(matched_sell_trans)
                        # Restart buy list for loop
                        restart = True
                        break
                    else:  # No match
                        buy.push(buying_trans, {"price": buying_trans.price, "timestamp": buying_trans.timestamp})
                        buy_list.remove(buying_trans)
                        # Restart for loop
                        restart = True
                        break
                if restart:
                    continue
                assert len(buy_list) == 0
                for selling_trans in sell_list:  # Push all unmatched sells back on
                    sell.push(selling_trans, {"price": selling_trans.price, "timestamp": selling_trans.timestamp})
                break


if __name__ == '__main__':
    main()
