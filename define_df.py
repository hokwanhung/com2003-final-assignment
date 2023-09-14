import numpy as np


def add_sma_crossover(df):
    copy = df.copy()
    # Calculates the and assign the moving average for the specified window size.
    copy["SMA_50"] = copy["Close"].rolling(50).mean()
    copy["SMA_200"] = copy["Close"].rolling(200).mean()
    return copy


def add_sma_crossover_with_signals(df):
    copy = df.copy()
    # Calculates the and assign the moving average for the specified window size.
    copy["SMA_50"] = copy["Close"].rolling(50).mean()
    copy["SMA_200"] = copy["Close"].rolling(200).mean()

    # Generate signals with regards to bullish signals and bearish signals.
    # SMA_50 > SMA_200 (crosses above) = bullish signals.
    # SMA_50 < SMA_200 (crosses below) = bearish signals.
    copy["Signal"] = 0
    copy.loc[(copy["SMA_50"] > copy["SMA_200"]) & (
        copy["SMA_50"].shift() < copy["SMA_200"].shift()), "Signal"] = 1
    copy.loc[(copy["SMA_50"] < copy["SMA_200"]) & (
        copy["SMA_50"].shift() > copy["SMA_200"].shift()), "Signal"] = -1

    return copy


def add_stochastic_oscillator(df, periods=14):
    # 14, 3, 3:
    # 14 specfies the number of periods used t0 calculate the %K line (i.e. fast line).
    # 3 specifies the number of periods used to calculate the %D line (i.e. slow line).
    # 3 specifies the smoothing factor used for the %D line.

    # The longer the more reliable; the shorter the more fluctuate.
    copy = df.copy()

    high_roll = copy["High"].rolling(periods).max()
    low_roll = copy["Low"].rolling(periods).min()
    print(high_roll)
    print(low_roll)

    # Fast stochastic indicator
    # %K = 100 * [(Close - Lowest Low in Period)/(Highest High in Period - Lowest Low in Period)]
    # More volatile.
    num = copy["Close"] - low_roll
    denom = high_roll - low_roll
    copy["%K"] = (num / denom) * 100

    # Slow stochastic indicator
    # Uses Simple Moving Average of the last 3 %K values using rolling() and mean() functions.
    # Less sensitive to price changes and provides a smoother representation.
    copy["%D"] = copy["%K"].rolling(3).mean()

    return copy


def add_stochastic_oscillator_strats_with_signals(df, periods=14, strat=0):
    # 14, 3, 3:
    # 14 specfies the number of periods used t0 calculate the %K line (i.e. fast line).
    # 3 specifies the number of periods used to calculate the %D line (i.e. slow line).
    # 3 specifies the smoothing factor used for the %D line.

    # The longer the more reliable; the shorter the more fluctuate.
    copy = df.copy()

    high_roll = copy["High"].rolling(periods).max()
    low_roll = copy["Low"].rolling(periods).min()
    print(high_roll)
    print(low_roll)

    # Fast stochastic indicator
    # %K = 100 * [(Close - Lowest Low in Period)/(Highest High in Period - Lowest Low in Period)]
    # More volatile.
    num = copy["Close"] - low_roll
    denom = high_roll - low_roll
    copy["%K"] = (num / denom) * 100

    # Slow stochastic indicator
    # Uses Simple Moving Average of the last 3 %K values using rolling() and mean() functions.
    # Less sensitive to price changes and provides a smoother representation.
    copy["%D"] = copy["%K"].rolling(3).mean()

    copy["Signal"] = 0
    if strat == 1:
        # Generate signals with regards to overbought signals and oversold signals.
        # %K > 80 = overbought signals.
        # %K < 20 = oversold signals.
        copy.loc[copy["%K"] < 20, "Signal"] = 1
        copy.loc[copy["%K"] > 80, "Signal"] = -1
    elif strat == 2:
        # Generate signals with regards to overbought divergence signals.
        # Price diff > 0 && %K Diff < 0 = bullish signals.
        # Price diff < 0 && %K Diff > 0 = bearish signals.
        copy.loc[(copy["Close"].diff() > 0) & (
            copy["%K"].diff() < 0), "Signal"] = 1
        copy.loc[(copy["Close"].diff() < 0) & (
            copy["%K"].diff() > 0), "Signal"] = -1
    elif strat == 3:
        # Generate signals with regards to
        copy.loc[(copy["%K"] > copy["%D"]), "Signal"] = 1
        copy.loc[(copy["%K"] < copy["%D"]), "Signal"] = -1
    else:
        print("WARN: no strategy has been applied.")

    return copy
