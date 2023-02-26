import random
from typing import Final
import time

# My discord is Adrian_Torpedo#7154, if you don't have discord my phone number is 905-933-5563. You should message me
# on one of them so if you run into problems, or I am doing someting you need to know about we can communicate about it.

# I sent you a friend request on discord!

symbolList = ["AAPL", "TSLA", "MSFT", "GOOGL", "SPOT", "NFLX"]
start_time = int(time.time())


class Transaction:

    # noinspection PyShadowingBuiltins
    def __init__(self, buy: bool, symbol: str, price, timestamp, id: int):
        self.buy: Final = buy
        self.symbol: Final = symbol
        self.price: Final = price
        self.timestamp: Final = timestamp
        self.id: Final = id


def incoming():
    two_power_128: int = 2 ** 128
    while True:
        yield Transaction(
            random.randint(0, 1) == 1,
            "",
            random.uniform(5, 100),
            time.time() + random.randint(-5, 5),
            random.randrange(two_power_128),
        )


def main():
    for transaction in incoming():
        # using end_time - start_time to create a unique timestamp for each transaction

        end_time = int(time.time())
        final_time = end_time - start_time

        return Transaction(random.randint(0, 1), random.choice(symbolList), random.randint(100, 150), final_time, 0)
        pass


if __name__ == '__main__':
    main()
