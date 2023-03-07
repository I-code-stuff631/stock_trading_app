import random
from typing import Final
import time
from enum import Enum, auto
from queue import PQueue
import collections


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
        return ("buy" if self.is_buy else "sell") + ' ' + str(self.symbol) + " for " + str(round(self.price, ndigits=2))


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
    global sell_list, buy_list

    sell = PQueue(
        lambda new, old:
        (new["price"] < old["price"]) or (new["price"] == old["price"] and new["timestamp"] < old["timestamp"])
    )
    buy = PQueue(
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

            sell_list = list()
            buy_list = list()

            for _ in range(length_min):
                sell_item: Transaction = sell.pop()
                buy_item: Transaction = buy.pop()

                sell_list.append(sell_item)
                buy_list.append(buy_item)

            sell_index_a = 0
            buy_index_a = 0

            for _ in range(len(sell_list)):
                if sell_list[sell_index_a].symbol == buy_list[buy_index_a].symbol:
                    print("\n")
                    print(sell_list[sell_index_a])
                    print(buy_list[buy_index_a])

                    sell_list.pop(sell_index_a)
                    buy_list.pop(buy_index_a)
                if buy_index_a < len(buy_list):
                    buy_index_a += 1
                if sell_index_a < len(sell_list) and buy_index_a == len(buy_list):
                    sell_index_b = 0
                    buy_index_b = 0
                    for _ in range(len(sell_list)):
                        if sell_list[sell_index_b].symbol == buy_list[buy_index_b].symbol:
                            print("\n")
                            print(sell_list[sell_index_b])
                            print(buy_list[buy_index_b])
                            sell_list.pop(sell_index_b)
                            buy_list.pop(buy_index_b)
                            sell_index_a = 0
                            buy_index_a = 0
                            sell_index_b = 0
                            buy_index_b = 0
                        if sell_index_b < len(sell_list):
                            sell_index_b += 1
                        elif buy_index_b < len(buy_list) and sell_index_b == len(sell_list):
                            for i in sell_list:
                                sell.push(i, {"price": i.price, "timestamp": i.timestamp})
                            for i in buy_list:
                                buy.push(i, {"price": i.price, "timestamp": i.timestamp})
                                sell_list = list()
                                buy_list = list()
                                sell_index_a = 0
                                buy_index_a = 0
                                sell_index_b = 0
                                buy_index_b = 0


if __name__ == '__main__':
    main()
