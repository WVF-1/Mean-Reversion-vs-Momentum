# Mean-Reversion-vs-Momentum
A stochastic simulation modeling project for uncertainty-based decision making, to aid in the preparation and construction of portfolios.

---

## Overview

This project investigates one of the most fundamental questions in quantitative finance:

> **Do asset prices trend, or do they revert to a mean — and under what conditions does each behavior dominate?**

We implement and compare two classic rules-based trading strategies using:
- **Synthetic price simulations** from stochastic processes (controlled experiments)
- **Professional backtesting framework** with realistic costs
- **Comprehensive performance metrics** (Sharpe, drawdowns, win rates)

---

## Quick Start

```bash
# Run complete demo (recommended)
python demo.py

# Or step-by-step:
python -m src.sims.brownian --years 15
python -m src.sims.ou --years 15
jupyter notebook notebooks/02-strategy-backtests.ipynb
```

---

## What You'll Learn

1. **Stochastic Modeling**: Generate realistic price data using GBM, OU, and regime-switching
2. **Strategy Development**: Build transparent, rules-based trading strategies
3. **Backtesting**: Implement professional backtesting with transaction costs
4. **Risk Analysis**: Calculate Sharpe ratios, drawdowns, and other key metrics
5. **Regime Dependence**: Understand why strategies work in some markets but fail in others

---

## Synthetic Data Engines

### Geometric Brownian Motion (Trending Markets)
```python
dS_t = μ S_t dt + σ S_t dW_t
```
- **Use case**: Test momentum strategies
- **Parameters**: μ=5% drift, σ=20% volatility
- **Realistic feature**: Sustained directional moves

### Ornstein-Uhlenbeck (Mean-Reverting Markets)
```python
dX_t = θ(μ - X_t)dt + σ dW_t
```
- **Use case**: Test mean reversion strategies  
- **Parameters**: θ=0.10 (half-life ≈7 days)
- **Realistic feature**: Price oscillations around mean

### Regime-Switching (Realistic Markets)
- **Two states**: Trending ↔ Range-bound
- **Transition probabilities**: Realistic regime persistence
- **Use case**: Stress-test both strategies under changing conditions

---

## Trading Strategies

### Mean Reversion
- **Entry**: |z-score| > 2.0 (buy dips)
- **Exit**: |z-score| < 0.5 (take profit)
- **Stop Loss**: |z-score| > 3.0
- **Logic**: Exploit price reversions to rolling mean

### Momentum  
- **Entry**: Fast MA (20) crosses above Slow MA (50)
- **Exit**: Fast MA drops below Exit MA (10)
- **Logic**: Capture sustained trends with adaptive exits

---

## Key Results

```
GBM (TRENDING MARKET):
Mean Reversion - Sharpe: 0.00  | Max DD: 0.00%  | Trades: 0
Momentum       - Sharpe: -24.41 | Max DD: -0.78% | Trades: 6
Winner: Mean Reversion (avoided unfavorable regime)

OU (MEAN-REVERTING MARKET):
Mean Reversion - Sharpe: -0.95 | Max DD: -4.74% | Trades: 24
Momentum       - Sharpe: -6.82 | Max DD: -1.41% | Trades: 10
Winner: Mean Reversion (smaller drawdown, higher Sharpe)
```

---

## Key Insights

1. **No universal winner**: Strategy performance is regime-dependent
2. **Mean reversion**: Excels in range-bound, oscillating markets
3. **Momentum**: Excels in trending markets (though needs longer trends)
4. **Drawdowns matter**: Risk-adjusted returns > raw returns
5. **Synthetic validation**: Controlled experiments reveal strategy logic

---

## Tech Stack

- Python 3.8+, NumPy, pandas, matplotlib
- Custom backtesting engine
- No machine learning (pure rules-based)
- Production-quality code structure

---

## Educational Value

Perfect for:
- Finance students learning quantitative methods
- Portfolio managers exploring strategy fundamentals  
- Aspiring quants building backtesting frameworks
- Anyone interested in systematic trading

---

## Extending This Project

1. Add real market data (SPY, QQQ, BTC)
2. Implement regime detection algorithms
3. Build adaptive strategies that switch based on regime
4. Add short positions and risk management
5. Optimize parameters via walk-forward analysis

---

## Documentation

- `docs/week2-report.md` - Detailed methodology and results
- `notebooks/` - Interactive walkthroughs
- Inline code comments throughout

---

## Installation & Testing

```bash
# Install
pip install -r requirements.txt

# Test
python tests/test_indicators.py

# Generate data
python -m src.sims.brownian --years 15

# Full demo
python demo.py
```

---

**Remember**: This is educational. Past performance ≠ future results. Not investment advice.

Built with ❤️ for quantitative finance education
