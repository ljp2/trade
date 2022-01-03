import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from joblib import load
from ring import ring
from position import Position

rf: RandomForestClassifier = load("Models/RF.joblib")
scaler: StandardScaler = load("Models/Scaler.joblib")


def noPosition(ring, position, working_bars):
    if ring.sum() <= -ring.N:
        open_short(position, working_bars)
    elif ring.sum() >= ring.N:
        open_long(position, working_bars)
    else:
        pass
    pass


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


def decision(df: pd.DataFrame, position: Position):
    global scaler, rf
    decision_bar = df.iloc[-1].copy()
    decision_bar.drop(
        ["time", "open", "high", "low", "close", "volume", "wap", "atr"], inplace=True
    )
    decision_bar_scaled = scaler.transform(decision_bar.to_frame().transpose())
    pred = rf.predict(decision_bar_scaled)
    ring.push(pred)

    if position.holding < 0:
        shortPosition(ring, position, working_bars)
    elif position.holding > 0:
        longPosition(ring, position, working_bars)
    elif position.holding == 0:
        noPosition(ring, position, working_bars)
    else:
        raise Exception("ILLEGAL position")
