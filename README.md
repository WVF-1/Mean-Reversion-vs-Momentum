# Mean-Reversion-vs-Momentum
A stochastic simulation modeling project for uncertainty-based decision making, to aid in the preparation and construction of portfolios.

---

## Overview

This project investigates one of the most fundamental questions in quantitative finance:

Do asset prices trend, or do they revert to a mean — and under what conditions does each behavior dominate?

We implement and compare two classic rules-based trading strategies:

Mean Reversion — buy dips, sell spikes

Momentum — trend-following via moving average crossovers

To isolate why each strategy works (or fails), we combine:

Synthetic price simulations generated from stochastic processes

Real-world market data for validation

All strategies are transparent, interpretable, and intentionally free of machine learning.

---


## Objectives

Understand how market regimes affect strategy performance

Compare mean reversion vs momentum under controlled conditions

Measure risk using professional metrics (Sharpe, drawdowns, volatility)

Demonstrate decision-making under uncertainty

Build a reusable, modular backtesting framework in Python

This project is designed for entry-level quantitative finance and sets the stage for portfolio construction and risk management topics.

---

## Core Questions

Do prices trend or revert?

When does each strategy outperform?

How do drawdowns differ across regimes?

What happens when the market regime shifts mid-strategy?

---

## Strategies
### Mean Reversion

Rolling mean and standard deviation

Z-score–based entry and exit rules

Designed for range-bound, stationary behavior

### Momentum

Moving average crossover rules

Long exposure during persistent trends

Exit when trend weakens or reverses

All strategies are fully rules-based with fixed, auditable logic.

---

## Stochastic Price Simulations

To create controlled market environments, we generate synthetic price series using:

Geometric Brownian Motion (GBM)

Models trending markets with drift and volatility

Baseline environment for momentum strategies

Ornstein–Uhlenbeck (OU) Process

Canonical mean-reverting process

Ideal for testing mean reversion logic

Regime-Switching Model

Two-state Markov process alternating between:

Trending (GBM-like)

Mean-reverting (OU-like)

Mimics realistic market regime changes

Synthetic data provides ground-truth regimes, allowing us to verify whether strategy behavior aligns with theory before testing on real markets.

---

## Experimental Design

Synthetic Experiments

Run both strategies on simulated price paths

Vary drift, volatility, and mean-reversion speed

Analyze returns, risk, and drawdowns by regime

Real-World Validation

Apply identical strategies to real assets

Compare results to buy-and-hold benchmarks

Regime-Based Analysis

Examine performance conditional on regime

Study drawdowns during regime transitions

---

## Evaluation Metrics

Each strategy is evaluated using:

- Annualized Return

- Annualized Volatility

- Sharpe Ratio

- Maximum Drawdown

- Calmar Ratio

- Win Rate

- Average Trade Duration

- Trade Count

Results are presented via equity curves, drawdown plots, and comparison tables.

---

## Tech Stack

Python

NumPy, pandas, matplotlib

Custom backtesting framework

No machine learning — rules only

---

## Key Takeaways

Strategy performance is regime-dependent

Mean reversion and momentum succeed under different assumptions

Drawdowns often reveal more than raw returns

Synthetic data is a powerful tool for validating strategy logic

Understanding when a strategy fails is as important as knowing when it works.

---

## Future Extensions

Volatility targeting and position sizing

Transaction cost sensitivity analysis

Regime detection using observable market features

Portfolio-level combinations of strategies
