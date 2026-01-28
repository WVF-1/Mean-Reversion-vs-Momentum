"""Geometric Brownian Motion simulation"""

import numpy as np
import pandas as pd
from src.utils import set_seed, trading_days_per_year, annual_to_daily


def simulate_gbm(mu=0.05, sigma=0.20, years=15, start_price=100, seed=None):
    """
    Simulate Geometric Brownian Motion
    
    dS_t = μ S_t dt + σ S_t dW_t
    
    Parameters:
    -----------
    mu : float
        Annual drift (default: 0.05 = 5% per year)
    sigma : float
        Annual volatility (default: 0.20 = 20% per year)
    years : int
        Number of years to simulate
    start_price : float
        Initial price
    seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame with columns: ['close', 'returns', 'log_returns']
    """
    if seed is not None:
        set_seed(seed)
    
    # Convert annual parameters to daily
    dt = 1 / trading_days_per_year()
    mu_daily = annual_to_daily(mu, is_return=True)
    sigma_daily = annual_to_daily(sigma, is_return=False)
    
    # Number of steps
    n_steps = int(years * trading_days_per_year())
    
    # Generate random shocks
    dW = np.random.normal(0, np.sqrt(dt), n_steps)
    
    # Initialize price array
    prices = np.zeros(n_steps + 1)
    prices[0] = start_price
    
    # Simulate GBM
    for t in range(1, n_steps + 1):
        drift = mu_daily * dt
        diffusion = sigma_daily * dW[t-1]
        prices[t] = prices[t-1] * np.exp(drift + diffusion)
    
    # Create DataFrame
    df = pd.DataFrame({
        'close': prices[1:],  # Skip initial price
    })
    
    df['returns'] = df['close'].pct_change()
    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
    
    return df


def main():
    """Generate and save GBM data"""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Generate GBM synthetic data')
    parser.add_argument('--mu', type=float, default=0.05, help='Annual drift')
    parser.add_argument('--sigma', type=float, default=0.20, help='Annual volatility')
    parser.add_argument('--years', type=int, default=15, help='Years to simulate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--output', type=str, default='data/synthetic/gbm/gbm_data.csv')
    
    args = parser.parse_args()
    
    # Generate data
    df = simulate_gbm(
        mu=args.mu,
        sigma=args.sigma,
        years=args.years,
        seed=args.seed
    )
    
    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Generated GBM data: {len(df)} bars")
    print(f"Saved to: {output_path}")
    print(f"\nSummary statistics:")
    print(f"  Final price: ${df['close'].iloc[-1]:.2f}")
    print(f"  Mean daily return: {df['returns'].mean()*100:.4f}%")
    print(f"  Daily volatility: {df['returns'].std()*100:.4f}%")


if __name__ == '__main__':
    main()
