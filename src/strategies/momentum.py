"""Momentum Strategy"""

import numpy as np
import pandas as pd
from src.indicators import moving_average_crossover, simple_moving_average


class MomentumStrategy:
    """
    Momentum Strategy using Moving Average Crossover
    
    Entry: When fast MA crosses above slow MA (golden cross)
    Exit: When fast MA crosses below exit MA or below slow MA (death cross)
    """
    
    def __init__(self, fast_ma=20, slow_ma=50, exit_ma=10):
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.exit_ma = exit_ma
        
        self.fast_ma_series = None
        self.slow_ma_series = None
        self.exit_ma_series = None
        self.signals = None
        self.in_position = False
    
    def initialize(self, data):
        """Calculate indicators"""
        prices = data['close']
        
        self.signals, self.fast_ma_series, self.slow_ma_series = moving_average_crossover(
            prices, self.fast_ma, self.slow_ma
        )
        self.exit_ma_series = simple_moving_average(prices, self.exit_ma)
    
    def generate_signal(self, idx):
        """
        Generate trading signal
        Returns: 1 (buy), 0 (hold), -1 (sell)
        """
        if idx < self.slow_ma:
            return 0
        
        current_signal = self.signals.iloc[idx]
        prev_signal = self.signals.iloc[idx-1] if idx > 0 else 0
        
        current_price = self.fast_ma_series.index[idx]
        fast_ma_val = self.fast_ma_series.iloc[idx]
        exit_ma_val = self.exit_ma_series.iloc[idx]
        
        if pd.isna(fast_ma_val) or pd.isna(exit_ma_val):
            return 0
        
        # Entry: Golden cross (fast crosses above slow)
        if not self.in_position and current_signal == 1 and prev_signal != 1:
            self.in_position = True
            return 1
        
        # Exit: Death cross or fast MA drops below exit MA
        if self.in_position:
            if current_signal == -1 or fast_ma_val < exit_ma_val:
                self.in_position = False
                return -1
        
        return 0
