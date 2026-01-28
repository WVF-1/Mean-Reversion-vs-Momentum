"""Performance metrics calculation"""

import numpy as np
import pandas as pd
from src.utils import trading_days_per_year


def annualized_return(returns):
    """Calculate annualized return from daily returns"""
    total_return = (1 + returns).prod() - 1
    n_years = len(returns) / trading_days_per_year()
    return (1 + total_return) ** (1 / n_years) - 1


def annualized_volatility(returns):
    """Calculate annualized volatility from daily returns"""
    return returns.std() * np.sqrt(trading_days_per_year())


def sharpe_ratio(returns, risk_free_rate=0.02):
    """Calculate Sharpe ratio"""
    annual_ret = annualized_return(returns)
    annual_vol = annualized_volatility(returns)
    
    if annual_vol == 0:
        return 0
    
    return (annual_ret - risk_free_rate) / annual_vol


def maximum_drawdown(equity_curve):
    """Calculate maximum drawdown from equity curve"""
    if isinstance(equity_curve, pd.DataFrame):
        equity = equity_curve['equity'].values
    else:
        equity = equity_curve
    
    running_max = np.maximum.accumulate(equity)
    drawdown = (equity - running_max) / running_max
    return drawdown.min()


def calmar_ratio(returns, equity_curve):
    """Calculate Calmar ratio (return / max drawdown)"""
    annual_ret = annualized_return(returns)
    max_dd = maximum_drawdown(equity_curve)
    
    if max_dd == 0:
        return 0
    
    return annual_ret / abs(max_dd)


def win_rate(trades_df):
    """Calculate percentage of profitable trades"""
    if len(trades_df) == 0:
        return 0
    
    # Match buys with sells
    buys = trades_df[trades_df['type'] == 'BUY']
    sells = trades_df[trades_df['type'] == 'SELL']
    
    if len(buys) == 0 or len(sells) == 0:
        return 0
    
    profitable = 0
    total = min(len(buys), len(sells))
    
    for i in range(total):
        if sells.iloc[i]['price'] > buys.iloc[i]['price']:
            profitable += 1
    
    return profitable / total if total > 0 else 0


def calculate_all_metrics(portfolio):
    """Calculate all metrics for a portfolio"""
    returns = portfolio.get_returns()
    equity_curve = portfolio.get_equity_curve()
    trades = portfolio.get_trades()
    
    metrics = {
        'Total Return': (equity_curve['equity'].iloc[-1] / portfolio.initial_capital - 1) * 100,
        'Annualized Return': annualized_return(returns) * 100,
        'Annualized Volatility': annualized_volatility(returns) * 100,
        'Sharpe Ratio': sharpe_ratio(returns),
        'Maximum Drawdown': maximum_drawdown(equity_curve) * 100,
        'Calmar Ratio': calmar_ratio(returns, equity_curve),
        'Win Rate': win_rate(trades) * 100,
        'Total Trades': len(trades),
        'Final Equity': equity_curve['equity'].iloc[-1]
    }
    
    return metrics
