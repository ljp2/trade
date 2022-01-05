import pandas as pd
import requests
import urllib3
from time import sleep
from datetime import datetime, timedelta

urllib3.disable_warnings()
SPY = 756733


def get(url, params=None):
    return requests.get(url, params=params, verify=False).json()


def post(url, data=None):
    return requests.post(url, data, verify=False)


def validate():
    return post("https://localhost:5000/v1/api/sso/validate")


def status():
    return post("https://localhost:5000/v1/api/iserver/auth/status")


def reauthenticate():
    return post("https://localhost:5000/v1/api/iserver/reauthenticate")


def logout():
    return post("https://localhost:5000/v1/api/logout")


def get_SPY_position():
    r = get("https://localhost:5000/v1/api/portfolio/DU276200/position/756733")
    print(r)


def wait_for_next_minute():
    current_time = datetime.now()
    new_time = current_time.replace(second=0, microsecond=0)
    uptime = new_time + timedelta(minutes=1, seconds=5)
    delay = uptime - current_time
    sleep(delay.total_seconds())


def trim_last_bar(bars: list):
    current_time = datetime.utcnow()
    last_bar = bars[-1]
    last_bar_time = datetime.fromtimestamp(last_bar['t'] // 1000)
    diff_seconds = (current_time - last_bar_time).total_seconds()
    if diff_seconds < 30:
        bars.pop()
    return bars


def _get_bars(conid, period, bar, outsideRth=False) -> list:
    payload = {"conid": conid, "period": period, "bar": bar, "outsideRth": outsideRth}
    r = get("https://localhost:5000/v1/api/iserver/marketdata/history", params=payload)
    return r['data']


# nn = 41
# nn_bars = pd.read_csv('Data/bars1/20211207.csv')


def get_bars() -> list:
    conid = SPY
    period = '40min'
    bar = '1min'
    outsideRth = False
    wait_for_next_minute()
    bars = _get_bars(conid, period, bar, outsideRth)
    bars = trim_last_bar(bars)
    return bars

    # global nn
    # nn += 1
    # if nn < len(nn_bars):
    #     return nn_bars.iloc[nn - 40:nn].to_dict('records')
    # else:
    #     return None


def bar_time(bar):
    bar_seconds = bar['t'] // 1000
    return datetime.fromtimestamp(bar_seconds)


def print_bars(bars):
    for bar in bars:
        print(bar, bar_time(bar))


if __name__ == '__main__':
    # conid = SPY
    # period = '3min'
    # bar = '1min'
    # outsideRth = False
    # # wait_for_next_minute()
    # print(datetime.utcnow(), datetime.now())
    # bars = _get_bars(conid, period, bar, True)
    # print(bar_time(bars[-1]))
    # print_bars(bars)
    # bars = trim_last_bar(bars)
    # print()
    # print(bar_time(bars[-1]))
    # print_bars(bars)
    get_SPY_position()
