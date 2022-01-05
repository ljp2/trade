import pandas as pd


class Position:
    def __init__(self, holding: int = 0, total_profit: float = 0):
        self.holding = holding
        self.price = None
        self.stop = None
        self.total_profit = total_profit


def open_long(position: Position):
    pass
    # price = current_bar.close
    # atr = current_bar.atr
    # position.holding = 1
    # position.price = price
    # position.stop = price - atr
    # print()
    # print(current_bar['time'], "Long opening position")
    # print("\tprice {:.2f}   stop {:.2f}".format(price, position.stop))


def close_long(position: Position):
    pass
    # price = current_bar['close']
    # transaction_profit_loss: float = price - position.price
    # position.holding = 0
    # position.price = None
    # print(current_bar['time'], "Long closing position")
    # position.total_profit += transaction_profit_loss
    # print("\tprice {:.2f}   transaction {:.2f}".format(price, transaction_profit_loss))


def open_short(position: Position):
    pass
    # price = current_bar['close']
    # atr = current_bar.atr
    # position.holding = -1
    # position.price = price
    # position.stop = price + atr
    # print()
    # print(current_bar['time'], "Short opening position")
    # print("\tprice {:.2f}   stop {:.2f}".format(price, position.stop))
    pass

def close_short(position: Position):
    # cover_price: float = current_bar['close']
    # transaction_profit_loss: float = position.price - cover_price
    # position.holding = 0
    # position.price = None
    # print("\tprice {:.2f}   transaction {:.2f}".format(cover_price, transaction_profit_loss))
    pass