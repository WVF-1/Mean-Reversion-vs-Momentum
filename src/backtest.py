"""Core backtesting engine"""

import pandas as pd
import numpy as np
from src.portfolio import Portfolio


class Backtest:
    """Strategy-agnostic backtesting engine"""
    
    def __init__(self, strategy, data, initial_capital=100000, 
                 transaction_cost=0.001, slippage=0.0005):
        self.strategy = strategy
        self.data = data
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        
        self.portfolio = Portfolio(initial_capital)
    
    def run(self):
        """Execute backtest"""
        print(f"Running backtest for {self.strategy.__class__.__name__}...")
        
        # Initialize strategy
        self.strategy.initialize(self.data)
        
        # Iterate through price data
        for idx in range(len(self.data)):
            timestamp = self.data.index[idx]
            current_price = self.data.iloc[idx]['close']
            
            # Get strategy signal
            signal = self.strategy.generate_signal(idx)
            
            # Execute trades based on signal
            self._execute_signal(signal, current_price, timestamp)
            
            # Update portfolio equity
            self.portfolio.update_equity(current_price, timestamp)
        
        # Close any open positions at the end
        if self.portfolio.position > 0:
            final_price = self.data.iloc[-1]['close']
            self.portfolio.sell(
                final_price, 
                self.portfolio.position, 
                self.data.index[-1],
                cost=self._calculate_cost(final_price, self.portfolio.position)
            )
        
        print(f"Backtest complete. Final equity: ${self.portfolio.equity:,.2f}")
        return self.portfolio
    
    def _execute_signal(self, signal, price, timestamp):
        """Execute trade based on strategy signal"""
        # Apply slippage
        execution_price = price * (1 + self.slippage) if signal > 0 else price * (1 - self.slippage)
        
        if signal > 0 and self.portfolio.position == 0:
            # Buy signal and no position - enter long
            shares = int(self.portfolio.cash / execution_price)
            cost = self._calculate_cost(execution_price, shares)
            self.portfolio.buy(execution_price, shares, timestamp, cost)
            
        elif signal < 0 and self.portfolio.position > 0:
            # Sell signal and have position - exit
            cost = self._calculate_cost(execution_price, self.portfolio.position)
            self.portfolio.sell(execution_price, self.portfolio.position, timestamp, cost)
    
    def _calculate_cost(self, price, shares):
        """Calculate transaction cost"""
        return price * shares * self.transaction_cost
