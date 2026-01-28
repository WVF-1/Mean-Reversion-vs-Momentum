"""Technical indicators for strategy implementation"""

import numpy as np
import pandas as pd


def simple_moving_average(prices, window):
    """Calculate simple moving average"""
    return prices.rolling(window=window).mean()


def rolling_std(prices, window):
    """Calculate rolling standard deviation"""
    return prices.rolling(window=window).std()


def z_score(prices, window):
    """
    Calculate z-score for mean reversion
    z = (price - rolling_mean) / rolling_std
    """
    ma = simple_moving_average(prices, window)
    std = rolling_std(prices, window)
    return (prices - ma) / std


def moving_average_crossover(prices, fast_window, slow_window):
    """
    Generate signals based on MA crossover
    Returns: 1 (bullish), 0 (neutral), -1 (bearish)
    """
    fast_ma = simple_moving_average(prices, fast_window)
    slow_ma = simple_moving_average(prices, slow_window)
    
    signal = pd.Series(0, index=prices.index)
    signal[fast_ma > slow_ma] = 1
    signal[fast_ma < slow_ma] = -1
    
    return signal, fast_ma, slow_ma
