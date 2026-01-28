"""Portfolio tracking and P&L calculation"""

import numpy as np
import pandas as pd


class Portfolio:
    """Track portfolio state during backtest"""
    
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0  # number of shares
        self.equity = initial_capital
        
        # History tracking
        self.equity_curve = []
        self.positions = []
        self.trades = []
        
    def buy(self, price, shares, timestamp, cost=0):
        """Execute buy order"""
        total_cost = price * shares + cost
        if total_cost <= self.cash:
            self.cash -= total_cost
            self.position += shares
            self.trades.append({
                'timestamp': timestamp,
                'type': 'BUY',
                'price': price,
                'shares': shares,
                'cost': cost
            })
            return True
        return False
    
    def sell(self, price, shares, timestamp, cost=0):
        """Execute sell order"""
        if shares <= self.position:
            self.cash += price * shares - cost
            self.position -= shares
            self.trades.append({
                'timestamp': timestamp,
                'type': 'SELL',
                'price': price,
                'shares': shares,
                'cost': cost
            })
            return True
        return False
    
    def update_equity(self, current_price, timestamp):
        """Update portfolio equity value"""
        self.equity = self.cash + self.position * current_price
        self.equity_curve.append({
            'timestamp': timestamp,
            'equity': self.equity,
            'cash': self.cash,
            'position': self.position,
            'price': current_price
        })
    
    def get_equity_curve(self):
        """Return equity curve as DataFrame"""
        return pd.DataFrame(self.equity_curve)
    
    def get_trades(self):
        """Return trade history as DataFrame"""
        return pd.DataFrame(self.trades)
    
    def get_returns(self):
        """Calculate portfolio returns"""
        df = self.get_equity_curve()
        returns = df['equity'].pct_change().dropna()
        return returns
