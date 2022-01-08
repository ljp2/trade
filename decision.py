import pandas as pd
from joblib import load
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from position import Position, open_long, close_long, open_short, close_short
from ring import Ring

rf: RandomForestClassifier = load("Models/RF.joblib")
scaler: StandardScaler = load("Models/Scaler.joblib")


def evaluate(df: pd.DataFrame) -> int:
    global scaler, rf
    decision_bar = df.iloc[-1].copy()
    decision_bar.drop(
        ["date", "open", "high", "low", "close", "volume", "wap", "atr"], inplace=True
    )
    decision_bar_scaled = scaler.transform(decision_bar.to_frame().transpose())
    pred = rf.predict(decision_bar_scaled)
    return pred


def noPosition(ring: Ring, pos: Position, current_bar: pd.Series):
    if ring.sum() <= -ring.N:
        open_short(pos, current_bar)
    elif ring.sum() >= ring.N:
        open_long(pos, current_bar)
    else:
        pass
    pass


def shortPosition(ring: Ring, pos: Position, current_bar: pd.Series):
    if current_bar.close >= pos.stop:
        print("short position hit stop -- closing")
        close_short(pos, current_bar)
        return

    if ring.sum() >= 2:
        print("change from sell to buy - closing short")
        close_short(pos, current_bar)
    elif ring.sum() <= -2:
        # still negative
        pass
    else:
        # neutral stay the course
        pass


def longPosition(ring: Ring, pos: Position, current_bar: pd.Series):
    if current_bar.close <= pos.stop:
        print("hit stop -- closing long")
        close_long(pos, current_bar)
        return
    if ring.sum() >= 2:
        # still positive
        pass
    elif ring.sum() <= -2:
        print("change from buy to sell - closing long")
        close_long(pos, current_bar)
    else:
        # neutral stay the course
        pass
