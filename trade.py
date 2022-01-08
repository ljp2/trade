import datetime
from time import sleep
import threading

from api import TradingApp
from position import Position
from webapi import get_bars
from indicators import add_indicators
import decision
from ring import Ring


def close_open_position(position: Position):
    if position.holding < 0:
        pass
    else:
        pass


def wait_for_next_minute():
    current_time = datetime.datetime.now()
    new_time = current_time.replace(second=0, microsecond=0)
    uptime = new_time + datetime.timedelta(minutes=1, seconds=5)
    # delay = uptime - current_time
    # sleep(delay.total_seconds())
    tnow = datetime.datetime.now()
    while tnow < uptime:
        # print("waiting", tnow.strftime("%H:%M:%S"), "for", uptime.strftime("%H:%M:%S"))
        sleep(5)
        tnow = datetime.datetime.now()


def trade_next_bar(app: TradingApp, ring: Ring, position: Position):
    df = app.get_barsDF('2400 S')
    df = add_indicators(df)
    pred = decision.evaluate(df)
    ring.push(pred)

    current_bar = df.iloc[-1]
    if position.holding < 0:
        decision.shortPosition(ring, position, current_bar)
        pass
    elif position.holding == 0:
        decision.noPosition(ring, position, current_bar)
        pass
    else:
        decision.longPosition(ring, position, current_bar)
        pass
    pass


def websocket_con(app):
    app.run()


def main():
    # stop_trading_time = datetime.datetime.now().replace(hour=15, minute=55, second=0, microsecond=0)
    stop_trading_time = datetime.datetime.now() + datetime.timedelta(hours = 1)

    position = Position()
    ring = Ring(2)

    app = TradingApp()
    app.event_connect.clear()
    app.connect("127.0.0.1", 7497, clientId=1)

    con_thread = threading.Thread(target=websocket_con, args=(app,), daemon=True)
    con_thread.start()
    app.event_connect.wait()

    i = 0
    while datetime.datetime.now() < stop_trading_time:
        wait_for_next_minute()
        trade_next_bar(app, ring, position)
        i += 1
        if i >= 30:
            break
    if position.holding != 0:
        close_open_position(position)

    sleep(1)
    app.disconnect()
    return


if __name__ == '__main__':
    main()
    print("DONE")
