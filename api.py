import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time
import datetime


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.bars = None
        self.nextValidOrderId = None
        self.event_connect = threading.Event()
        self.event_datadone = threading.Event()
        self.event_position_change = threading.Event()

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        self.event_connect.set()

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId, errorCode, errorString))

    def contractDetails(self, reqId, contractDetails):
        print("redID: {}, contract:{}".format(reqId, contractDetails))

    def historicalData(self, reqId, bar):
        self.bars.append((bar.date, bar.open, bar.high, bar.low, bar.close,
                          float(bar.volume), float(bar.wap)))

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        # df = pd.DataFrame(self.bars, columns="date open high low close volume wap".split()).set_index('date')
        self.event_datadone.set()

    def get_barsDF(self, duration: str) -> pd.DataFrame:
        self.event_datadone.clear()
        self.bars = []
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        self.reqHistoricalData(reqId=1,
                               contract=contract,
                               endDateTime="",
                               durationStr=duration,
                               barSizeSetting='1 min',
                               whatToShow='TRADES',
                               useRTH=1,
                               formatDate=1,
                               keepUpToDate=False,
                               chartOptions=[])
        self.event_datadone.wait()
        df = pd.DataFrame(self.bars, columns="date open high low close volume wap".split())
        return df

    def placeBUYOrder(self, quantity=1) -> int:
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        order = Order()
        order.action = "BUY"
        order.orderType = "MKT"
        order.totalQuantity = 1
        oid = self.nextOrderId()
        self.placeOrder(oid, contract, order)
        return oid

    def placeSELLOrder(self, quantity=1) -> int:
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        order = Order()
        order.action = "SELL"
        order.orderType = "MKT"
        order.totalQuantity = quantity
        oid = self.nextOrderId()
        self.placeOrder(oid, contract, order)
        return oid

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    def positionEnd(self):
        super().positionEnd()
        print("PositionEnd")
        self.event_position_change.set()



if __name__ == '__main__':
    app = TradingApp()

    df = app.get_bars('2700 S')
    print(df)



    time.sleep(5)
    app.disconnect()



    print('DONE DONE DONE')