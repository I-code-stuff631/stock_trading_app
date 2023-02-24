import random
from typing import Final
import time
# My discord is Adrian_Torpedo#7154, if you don't have discord my phone number is 905-933-5563. You should message me
# on one of them so if you run into problems, or I am doing someting you need to know about we can communicate about it.


class Transation:
    # noinspection PyShadowingBuiltins
    def __init__(self, buy: bool, symbol: str, price, timestamp, id: int):
        self.buy: Final = buy
        self.symbol: Final = symbol
        self.price: Final = price
        self.timestamp: Final = timestamp
        self.id: Final = id


def incoming():
    two_power_128: int = 2**128
    while True:
        yield Transation(
            random.randint(0, 1) == 1,
            "",
            random.uniform(5, 100),
            time.time() + random.randint(-5, 5),
            random.randrange(two_power_128),
        )


def main():
    for transation in incoming():
        pass


if __name__ == '__main__':
    main()
