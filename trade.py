import datetime
from time import sleep

from position import Position
from webapi import get_bars
from indicators import add_indicators


def setup_for_trading():
    position = Position()
    return position


def close_open_positions():
    pass


def trade_next_bar():
    bars = get_bars()
    df = add_indicators(bars)

    pass


def main():
    setup_for_trading()
    stop_trading_time = datetime.datetime.now().replace(hour=15, minute=55, second=0, microsecond=0)
    while datetime.datetime.now() < stop_trading_time:
        trade_next_bar()
        sleep(1)
    close_open_positions()


if __name__ == '__main__':
    trade_next_bar()



print("DONE")
