"""Data loading utilities"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_csv(filepath):
    """Load price data from CSV file"""
    df = pd.read_csv(filepath)
    
    # Ensure we have the required columns
    if 'close' not in df.columns and 'Close' not in df.columns:
        raise ValueError("CSV must contain 'close' or 'Close' column")
    
    # Standardize column names
    df.columns = [col.lower() for col in df.columns]
    
    return df


def load_synthetic(filepath):
    """Load synthetic price data"""
    df = pd.read_csv(filepath)
    return df


def prices_to_returns(prices):
    """Convert prices to log returns"""
    return np.log(prices / prices.shift(1)).dropna()
