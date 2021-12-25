import os, sys
import numpy as np
import pandas as pd
from joblib import load
from sklearn.utils.sparsefuncs import inplace_column_scale
from ManageData.add_indicators import add_indicators
from ta.volatility import AverageTrueRange

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class Position:
    def __init__(self):
        self.holding: int = 0
        self.price: float = None
        self.stop: float = None


class Ring:
    def __init__(self, n: int):
        self.N = n
        self.buf = np.zeros(n, dtype='int8')
        self.index: int = 0
        self.last_val: int = None

    def push(self, pred: int):
        val = 1 if pred == 1 else -1
        self.last_val = val
        self.buf[self.index] = val
        self.index = (self.index + 1) % 2

    def last_pred(self):
        return self.last_val

    def OK(self):
        return self.buf.sum()

    def __str__(self) -> str:
        return "{}:{}".format(self.last_val, self.buf)


BARS_DIRECTORY = "./DATA/"
BARS1_DIRECTORY = BARS_DIRECTORY + "bars1/"

rf: RandomForestClassifier = load("Models/RF.joblib")
scaler: StandardScaler = load("Models/Scaler.joblib")


def getBar(day):
    bars = pd.read_csv(BARS1_DIRECTORY + day)
    for index, row in bars.iterrows():
        yield row


def shortPosition(ring, position, current_bar, working_bars):
    current_bar = working_bars.iloc[-1].copy()
    print(current_bar.time, ring)
    pass


def longPosition(ring, position, working_bars):
    current_bar = working_bars.iloc[-1].copy()
    print(current_bar.time, ring)
    pass


def noPosition(ring, position, working_bars):
    current_bar = working_bars.iloc[-1].copy()

    print(current_bar.time, str(ring))

    print(current_bar.time, ring)
    if ring.OK() <= -ring.N:
        open_short(position, working_bars)
    elif ring.OK() >= ring.N:
        open_long(position, working_bars)
    else:
        pass
    pass


def evaluate_position(position, working_bars):
    pass


def open_long(position, working_bars):
    current_bar = working_bars.iloc[-1]
    price = current_bar.close
    atr = current_bar.atr
    position.holding = 1
    position.price = price
    position.stop = price - atr
    pass


def open_short(position, working_bars):
    current_bar = working_bars.iloc[-1]
    price = current_bar.close
    atr = current_bar.atr
    position.holding = -1
    position.price = price
    position.stop = price + atr
    pass


def close_long(position, working_bars):
    current_bar = working_bars.iloc[-1]
    price = current_bar.close
    transaction_profit_loss : float = price - position.price
    position.holding = 0
    position.price = None
    return transaction_profit_loss


def close_short(position, working_bars):
    current_bar = working_bars.iloc[-1]
    price: float = current_bar.close
    transaction_profit_loss: float = price - position.price
    position.holding = 0
    position.price = None
    return transaction_profit_loss


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


def main():
    days = os.listdir("./Data/bars1")
    days.sort(reverse=True)
    for day in days[2:3]:
        trade_day(day)


if __name__ == "__main__":
    main()
