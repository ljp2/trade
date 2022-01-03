import pandas as pd
import warnings

from ta.momentum import TSIIndicator, UltimateOscillator, WilliamsRIndicator
from ta.volume import (
    AccDistIndexIndicator,
    ChaikinMoneyFlowIndicator,
    EaseOfMovementIndicator,
    ForceIndexIndicator,
    MFIIndicator,
    NegativeVolumeIndexIndicator
)
from ta.momentum import (
    AwesomeOscillatorIndicator,
    PercentagePriceOscillator,
    PercentageVolumeOscillator,
    ROCIndicator,
    RSIIndicator,
    StochRSIIndicator,
    StochasticOscillator,
)
from ta.trend import ADXIndicator, AroonIndicator, CCIIndicator, DPOIndicator
from ta.volatility import KeltnerChannel, UlcerIndex, AverageTrueRange


def add_indicators(bars: list) -> pd.DataFrame:
    df = pd.DataFrame(bars)
    atr = AverageTrueRange(df.high, df.low, df.close)
    df["atr"] = atr.average_true_range()

    awesome_oscillator = AwesomeOscillatorIndicator(df.high, df.low)
    df["awesome"] = awesome_oscillator.awesome_oscillator()

    ppo = PercentagePriceOscillator(df.close)
    df["ppo"] = ppo.ppo()
    df["pposig"] = ppo.ppo_signal()

    pvo = PercentageVolumeOscillator(df.volume)
    df["pvo"] = pvo.pvo()
    df["pvosig"] = pvo.pvo_signal()

    roc = ROCIndicator(df.close)
    df["roc"] = roc.roc()

    rsi = RSIIndicator(df.close)
    df["rsi"] = rsi.rsi()

    stochrsi = StochRSIIndicator(df.close)
    df["stochrsi"] = stochrsi.stochrsi()
    df["stochrsi_d"] = stochrsi.stochrsi_d()
    df["stochrsi_k"] = stochrsi.stochrsi_k()

    stoch = StochasticOscillator(df.high, df.low, df.close)
    df["stoch"] = stoch.stoch()
    df["stoch_sig"] = stoch.stoch_signal()

    tsi = TSIIndicator(df.close)
    df["tsi"] = tsi.tsi()

    ultosc = UltimateOscillator(df.high, df.low, df.close)
    df["ultosc"] = ultosc.ultimate_oscillator()

    williamsR = WilliamsRIndicator(df.high, df.low, df.close)
    df["williamsR"] = williamsR.williams_r()

    acc_dist_index = AccDistIndexIndicator(df.high, df.low, df.close, df.volume)
    df["acc_dist_index"] = acc_dist_index.acc_dist_index()

    chaikinMF = ChaikinMoneyFlowIndicator(df.high, df.low, df.close, df.volume)
    df["chaikinMF"] = chaikinMF.chaikin_money_flow()

    ease_move = EaseOfMovementIndicator(df.high, df.low, df.volume)
    df["ease_mov"] = ease_move.ease_of_movement()
    df["sig_ease_mov"] = ease_move.sma_ease_of_movement()

    force_index = ForceIndexIndicator(df.close, df.volume)
    df["force_index"] = force_index.force_index()

    mfi = MFIIndicator(df.high, df.low, df.close, df.volume)
    df["mfi"] = mfi.money_flow_index()

    neg_vol_index = NegativeVolumeIndexIndicator(df.close, df.volume)
    df["neg_vol_index"] = neg_vol_index.negative_volume_index()

    adx = ADXIndicator(df.high, df.low, df.close)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df["adx"] = adx.adx()
    df["adx_pos"] = adx.adx_pos()
    df["adx_neg"] = adx.adx_neg()

    aroon = AroonIndicator(df.close)
    df["aroon"] = aroon.aroon_indicator()
    df["aroon_up"] = aroon.aroon_up()
    df["aroon_down"] = aroon.aroon_down()

    cci = CCIIndicator(df.high, df.low, df.close)
    df["cci"] = cci.cci()

    dpo = DPOIndicator(df.close)
    df["dpo"] = dpo.dpo()

    keltner = KeltnerChannel(df.high, df.low, df.close)
    kelt_width = keltner.keltner_channel_wband()
    df["kelt_from_low"] = (kelt_width - df["close"]) / df["close"]
    df["kelt_width"] = kelt_width / df["close"]

    ulcer = UlcerIndex(df.close)
    df["ulcer"] = ulcer.ulcer_index()

    return df
