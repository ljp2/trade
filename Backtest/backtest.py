import os, sys

sys.path.append('..')

import numpy as np
import pandas as pd
from joblib import load
from sklearn.utils.sparsefuncs import inplace_column_scale
from ManageData.add_indicators import add_indicators
from ta.volatility import AverageTrueRange

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class Position:
    holding = 0
    price = None
    stop = None
    total_profit = 0

    def __repr__(self):
        s =  "hold {}   price {:.2f}   stop {:.2f}"
        return s.format(self.holding, self.price, self.stop)


class Ring:
    def __init__(self, n: int):
        self.N = n
        self.buf = np.zeros(n, dtype="int8")
        self.index: int = 0
        self.last_val: int = None

    def push(self, pred: int):
        val = 1 if pred == 1 else -1
        self.last_val = val
        self.buf[self.index] = val
        self.index = (self.index + 1) % 2

    def last_pred(self):
        return self.last_val

    def sum(self):
        return self.buf.sum()

    def __repr__(self) -> str:
        return "{}:{}".format(self.last_val, self.buf)


BARS_DIRECTORY = "../DATA/"
BARS1_DIRECTORY = BARS_DIRECTORY + "bars1/"

rf: RandomForestClassifier = load("../Models/RF.joblib")
scaler: StandardScaler = load("../Models/Scaler.joblib")


def getBar(day):
    bars = pd.read_csv(BARS1_DIRECTORY + day)
    for index, row in bars.iterrows():
        yield row


def shortPosition(ring, position, working_bars):
    current_bar = working_bars.iloc[-1].copy()
    if current_bar.close >= position.stop:
        print("short position hit stop -- closing")
        close_short(position, working_bars)
        return
    if ring.sum() >= 2:
        print("change from sell to buy - closing short")
        close_short(position, working_bars)
    elif ring.sum() <= -2:
        # still negative
        pass
    else:
        # neutral stay the course
        pass


def longPosition(ring, position, working_bars):
    current_bar = working_bars.iloc[-1].copy()
    if current_bar.close <= position.stop:
        print("hit stop -- closing long")
        close_long(position, working_bars)
        return
    if ring.sum() >= 2:
        # still positive
        pass
    elif ring.sum() <= -2:
        print("change from buy to sell - closing long")
        close_long(position, working_bars)
    else:
        # neutral stay the course
        pass


def noPosition(ring, position, working_bars):
    if ring.sum() <= -ring.N:
        open_short(position, working_bars)
    elif ring.sum() >= ring.N:
        open_long(position, working_bars)
    else:
        pass
    pass


def open_long(position, working_bars):
    current_bar = working_bars.iloc[-1]
    price = current_bar.close
    atr = current_bar.atr
    position.holding = 1
    position.price = price
    position.stop = price - atr
    print()
    print(current_bar['time'], "Long opening position")
    print("\tprice {:.2f}   stop {:.2f}".format(price, position.stop))


def open_short(position, working_bars):
    current_bar = working_bars.iloc[-1]
    price = current_bar.close
    atr = current_bar.atr
    position.holding = -1
    position.price = price
    position.stop = price + atr
    print()
    print(current_bar['time'], "Short opening position")
    print("\tprice {:.2f}   stop {:.2f}".format(price, position.stop))


def close_long(position, working_bars):
    current_bar = working_bars.iloc[-1]
    price = current_bar.close
    transaction_profit_loss: float = price - position.price
    position.holding = 0
    position.price = None
    print(current_bar['time'], "Long closing position")
    position.total_profit += transaction_profit_loss
    print("\tprice {:.2f}   transaction {:.2f}".format(price, transaction_profit_loss))

def close_short(position, working_bars):
    current_bar = working_bars.iloc[-1]
    cover_price: float = current_bar.close
    transaction_profit_loss: float = position.price - cover_price
    position.holding = 0
    position.price = None
    print("\tprice {:.2f}   transaction {:.2f}".format(cover_price, transaction_profit_loss))


def trade_bars(bars, position, ring):
    global scaler, rf
    working_bars = bars.iloc[-39:].copy()
    add_indicators(working_bars, gain=False)

    current_bar = working_bars.iloc[-1].copy()
    current_bar.drop(
        ["time", "open", "high", "low", "close", "volume", "wap", "atr"], inplace=True
    )
    current_bar_scaled = scaler.transform(current_bar.to_frame().transpose())

    pred = rf.predict(current_bar_scaled)
    ring.push(pred)

    if position.holding < 0:
        shortPosition(ring, position, working_bars)
    elif position.holding > 0:
        longPosition(ring, position, working_bars)
    elif position.holding == 0:
        noPosition(ring, position, working_bars)
    else:
        raise Exception("ILLEGAL position")


def trade_day(day: str):
    bars = pd.DataFrame()
    position = Position()
    ring = Ring(2)
    for bar in getBar(day):
        bars = bars.append(bar, ignore_index=True)
        if bars.shape[0] > 39:
            trade_bars(bars, position, ring)
    print("DAY PROFIT = {:.3f}".format(position.total_profit))

def main():
    days = os.listdir("../Data/bars1")
    days.sort(reverse=True)
    for day in days[0:1]:
        trade_day(day)


if __name__ == "__main__":
    main()
