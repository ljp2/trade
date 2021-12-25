import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import datetime
import os

BARS1_DIRECTORY = 'Data/bars1'
BAR_MINUTES_1 = '1 min'
BAR_MINUTES_5 = '5 mins'
BARS5_DIRECTORY = 'Data/bars5'

BARS_DIRECTORY = BARS1_DIRECTORY
BAR_MINUTES = BAR_MINUTES_1

def get_most_current_file_date(dir_name):
    s = max(os.listdir(dir_name)).split('.')[0]
    d = datetime.datetime.strptime(s, '%Y%m%d')
    return d.strftime("%Y-%m-%d")

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.bars = None
        self.end_date = None

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        event_connect.set()

    def historicalData(self, reqId, bar):
        bartime = bar.date.split()[1]
        self.bars.append((bartime, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.average))

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        df = pd.DataFrame(self.bars, columns='time open high low close volume wap'.split()).set_index('time')
        bars_date = self.end_date.split()[0]
        df.to_csv(f'{BARS_DIRECTORY}/{bars_date}.csv',  line_terminator='\n')
        event_datadone.set()

    def get_data(self, contract, queryTime):
        self.bars = []
        self.end_date = queryTime.strftime("%Y%m%d %H:%M:%S")
        app.reqHistoricalData(reqId=1,
                              contract=contract,
                              endDateTime=self.end_date,
                              durationStr='1 D',
                              barSizeSetting=BAR_MINUTES,
                              whatToShow='TRADES',
                              useRTH=1,
                              formatDate=1,
                              keepUpToDate=False,
                              chartOptions=[])


def websocket_con():
    app.run()

event_connect = threading.Event()
event_datadone = threading.Event()
app = TradingApp()

app.connect("127.0.0.1", 4002, clientId=1)

threading.Thread(target=websocket_con, daemon=True).start()
event_connect.wait()
time.sleep(1)

contract = Contract()
contract.symbol = "SPY"
contract.exchange = "SMART"
contract.secType = "STK"
contract.currency = "USD"

today = datetime.datetime.today()
dd = datetime.timedelta(days=1)
if today.time() < datetime.time(16, 30):
    startday = today.date() - dd
else:
    startday = today.date()

query_time_start = datetime.datetime(startday.year, startday.month, startday.day, 16, 30)
most_current_file_date = get_most_current_file_date(BARS_DIRECTORY)

print(most_current_file_date, query_time_start)

for i in range(300):
    queryTime = query_time_start - i * dd

    if queryTime.strftime("%Y-%m-%d") == most_current_file_date:
        break

    weekday = queryTime.weekday()
    if weekday <= 4:
        print(queryTime, weekday,
              ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday])
        event_datadone.clear()
        app.get_data(contract, queryTime)
        event_datadone.wait()
    time.sleep(1)

time.sleep(1)
app.disconnect()
print('DONE DONE DONE')
