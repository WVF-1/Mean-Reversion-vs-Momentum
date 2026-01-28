"""Mean Reversion Strategy"""

import numpy as np
import pandas as pd
from src.indicators import z_score


class MeanReversionStrategy:
    """
    Mean Reversion Strategy using Z-Score
    
    Entry: When price deviates significantly from rolling mean (|z-score| > entry_z)
    Exit: When price returns closer to mean (|z-score| < exit_z)
    Stop Loss: When z-score exceeds stop_loss_z
    """
    
    def __init__(self, window=20, entry_z=2.0, exit_z=0.5, stop_loss_z=3.0):
        self.window = window
        self.entry_z = entry_z
        self.exit_z = exit_z
        self.stop_loss_z = stop_loss_z
        
        self.z_scores = None
        self.in_position = False
        self.position_type = None  # 'long' or 'short'
    
    def initialize(self, data):
        """Calculate indicators"""
        prices = data['close']
        self.z_scores = z_score(prices, self.window)
    
    def generate_signal(self, idx):
        """
        Generate trading signal
        Returns: 1 (buy), 0 (hold), -1 (sell)
        """
        if idx < self.window:
            return 0
        
        current_z = self.z_scores.iloc[idx]
        
        if pd.isna(current_z):
            return 0
        
        # Entry logic
        if not self.in_position:
            if current_z < -self.entry_z:
                # Price too low - buy (expect reversion up)
                self.in_position = True
                self.position_type = 'long'
                return 1
            # Note: We're only trading long for simplicity
            # Could add short logic here for current_z > self.entry_z
        
        # Exit logic
        else:
            # Stop loss
            if abs(current_z) > self.stop_loss_z:
                self.in_position = False
                self.position_type = None
                return -1
            
            # Take profit
            if abs(current_z) < self.exit_z:
                self.in_position = False
                self.position_type = None
                return -1
        
        return 0
