"""Utility functions for the project"""

import numpy as np
import random


def set_seed(seed=42):
    """Set random seed for reproducibility"""
    np.random.seed(seed)
    random.seed(seed)


def trading_days_per_year():
    """Return number of trading days per year"""
    return 252


def daily_to_annual(value, is_return=True):
    """Convert daily metrics to annual"""
    if is_return:
        return value * trading_days_per_year()
    else:  # volatility
        return value * np.sqrt(trading_days_per_year())


def annual_to_daily(value, is_return=True):
    """Convert annual metrics to daily"""
    if is_return:
        return value / trading_days_per_year()
    else:  # volatility
        return value / np.sqrt(trading_days_per_year())
