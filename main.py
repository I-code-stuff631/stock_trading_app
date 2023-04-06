import random
from typing import Final
import time
from enum import Enum, auto
from queue import PQueue
from rich.console import Console
from rich.table import Table
from collections import deque
from datetime import datetime
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
    dt = datetime.now()
    with open(f"{dt.date()}_{dt.hour}-{dt.minute}-{dt.second}.{dt.microsecond}.log", "w") as f:
        sell = PQueue(
            lambda new, old:  # Lowest sells get priority
            (new["price"] < old["price"]) or (new["price"] == old["price"] and new["timestamp"] < old["timestamp"])
        )
        buy = PQueue(
            lambda new, old:  # Highest buys get priority
            (new["price"] > old["price"]) or (new["price"] == old["price"] and new["timestamp"] < old["timestamp"])
        )

        def new_matched_table():
            table = Table(title="Matched Stocks")
            table.add_column("ID", style="green", no_wrap=True)
            table.add_column("Sell Orders", style="cyan")
            table.add_column("ID", style="green", no_wrap=True)
            table.add_column("Buy Orders", style="magenta")
            return table

        matched_table = new_matched_table()
        matched_transactions: deque[(Transaction, Transaction)] = deque(maxlen=10)
        start_time: float = time.time()
        for trans in incoming():
            if trans.is_buy:
                buy.push(trans, {"price": trans.price, "timestamp": trans.timestamp})
            else:
                sell.push(trans, {"price": trans.price, "timestamp": trans.timestamp})

            if (time.time() - start_time) >= 5:
                start_time = time.time()
                length_min = min(len(buy) // 2, len(sell) // 2)

                def sleep(secs: float):
                    nonlocal start_time
                    time.sleep(secs)
                    start_time += secs

                sell_list: list[Transaction] = []
                buy_list: list[Transaction] = []
                for _ in range(length_min):
                    sell_list.append(sell.pop())
                    buy_list.append(buy.pop())
                f.write(f"Sell chunk length: {len(sell_list)}\n")
                f.write(f"Buy chunk length: {len(buy_list)}\n")

                while True:
                    restart = False
                    for buying_trans in buy_list:
                        matched_sell_trans = None

                        def new_app_table():
                            table = Table(title="Stock Trading App")
                            table.add_column("Finding match for", style="red", no_wrap=True)
                            table.add_column("Current match", style="green", no_wrap=True)
                            table.add_column("Looking at", style="blue", no_wrap=True)
                            return table

                        # So app_table is always bound
                        app_table = new_app_table()
                        app_table.add_row(str(buying_trans), str(matched_sell_trans), str(None))

                        def refresh_console():
                            console.clear()
                            console.print(app_table)
                            console.print(matched_table)

                        # Find matching
                        for selling_trans in sell_list:
                            app_table = new_app_table()
                            app_table.add_row(str(buying_trans), str(matched_sell_trans), str(selling_trans))
                            refresh_console()
                            # sleep(.5)

                            if buying_trans.symbol == selling_trans.symbol and selling_trans.price <= buying_trans.price:
                                if matched_sell_trans is None:
                                    matched_sell_trans = selling_trans
                                elif abs(selling_trans.price - buying_trans.price) < abs(
                                        matched_sell_trans.price - buying_trans.price):
                                    matched_sell_trans = selling_trans

                        if matched_sell_trans is not None:  # There is a match
                            app_table = Table(title="Stock Trading App")
                            app_table.add_column("Found match for", style="magenta", no_wrap=True)
                            app_table.add_column("Match", style="cyan", no_wrap=True)
                            app_table.add_row(str(buying_trans), str(matched_sell_trans))
                            refresh_console()
                            sleep(1)

                            matched_transactions.appendleft((buying_trans, matched_sell_trans))
                            f.write(f"{hex(buying_trans.id)[:4]} - {buying_trans} --- {hex(matched_sell_trans.id)[:4]} - {matched_sell_trans}\n")
                            buy_list.remove(buying_trans)
                            sell_list.remove(matched_sell_trans)

                            matched_table = new_matched_table()
                            id_len = 4
                            for buy_trans, sell_trans in matched_transactions:
                                matched_table.add_row(
                                    hex(sell_trans.id)[:id_len],
                                    str(sell_trans),
                                    hex(buy_trans.id)[:id_len],
                                    str(buy_trans),
                                )
                            refresh_console()
                            sleep(5)

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
