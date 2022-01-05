import datetime
from time import sleep

from api import TradingApp
from position import Position
from webapi import get_bars
from indicators import add_indicators
import decision
from ring import Ring


def setup_for_trading():
    position = Position()
    ring = Ring(2)
    return ring, position


def close_open_position(position: Position):
    if position.holding < 0:
        pass
    else:
        pass


def trade_next_bar(ring: Ring, position: Position):
    bars = get_bars()
    df = add_indicators(bars)
    pred = decision.evaluate(df)
    ring.push(pred)
    current_bar = df.iloc[-1]
    if position.holding < 0:
        decision.shortPosition(ring, position, current_bar)
        pass
    elif position.holding == 0:
        decision.noPosition(ring, position)
        pass
    else:
        decision.longPosition(ring, position, current_bar)
        pass

    pass


def main():
    ring, position = setup_for_trading()
    stop_trading_time = datetime.datetime.now().replace(hour=15, minute=55, second=0, microsecond=0)
    while datetime.datetime.now() < stop_trading_time:
        trade_next_bar(ring, position)
        sleep(1)
    if position.holding != 0:
        close_open_position(position)


if __name__ == '__main__':
    ring, position = setup_for_trading()
    app = TradingApp()
    df = app.get_barsDF('2700 S')
    df = add_indicators(df)
    pred = decision.evaluate(df)

    print('pred = ', pred)
    app.disconnect()
    print("DONE")
