import random
from typing import Final
import time
from enum import Enum, auto
from queue import PQueue
from rich.console import Console
from rich.table import Table
from rust_queue import DoublePriorityQueue
console = Console()


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
    sell = DoublePriorityQueue(lambda item: item.price)  # Key extractor - takes an item and prouduces a key for it
    buy = DoublePriorityQueue(lambda item: item.price)

    matched_table = Table(title="Matched Stocks")
    # matched_table.add_column("ID", style="green", no_wrap=True)
    matched_table.add_column("Sell Orders", style="cyan")
    # matched_table.add_column("ID", style="green", no_wrap=True)
    matched_table.add_column("Buy Orders", style="magenta")

    matched_transactions: list[(Transaction, Transaction)] = []
    start_time: float = time.time()
    for trans in incoming():
        if trans.is_buy:
            buy.push(trans)
        else:
            sell.push(trans)

        if (time.time() - start_time) >= 5:
            matched_buy_trans = []
            for buy_trans in buy:
                matched_sell: Transaction | None = sell.pop_closest_satisfying(  # This only works if the key is numeric
                    buy_trans,  # << It might be better to make this a key instead of an item that the key is extracted from
                    lambda item: item.price <= buy_trans.price and item.symbol == buy_trans.symbol
                )
                if matched_sell is not None:
                    matched_buy_trans.append(buy_trans)
                    matched_transactions.append((buy_trans, matched_sell))

            # Remove all buy transactions that now have a matching sell
            for buy_trans in matched_buy_trans:
                buy.remove(buy_trans)
            matched_buy_trans.clear()


if __name__ == '__main__':
    main()
