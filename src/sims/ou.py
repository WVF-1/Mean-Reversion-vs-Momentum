"""Ornstein-Uhlenbeck process simulation"""

import numpy as np
import pandas as pd
from src.utils import set_seed, trading_days_per_year


def simulate_ou(theta=0.10, sigma=0.10, mean_level=4.605, years=15, seed=None):
    """
    Simulate Ornstein-Uhlenbeck process
    
    dX_t = θ(μ - X_t)dt + σ dW_t
    
    Applied to log prices for geometric mean reversion
    
    Parameters:
    -----------
    theta : float
        Mean reversion speed (higher = faster reversion)
    sigma : float
        Noise amplitude
    mean_level : float
        Long-run mean (in log space, e.g., log(100) = 4.605)
    years : int
        Number of years to simulate
    seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame with columns: ['close', 'returns', 'log_returns', 'log_price']
    """
    if seed is not None:
        set_seed(seed)
    
    # Time parameters
    dt = 1 / trading_days_per_year()
    n_steps = int(years * trading_days_per_year())
    
    # Initialize log price array
    log_prices = np.zeros(n_steps + 1)
    log_prices[0] = mean_level
    
    # Simulate OU process
    for t in range(1, n_steps + 1):
        dW = np.random.normal(0, np.sqrt(dt))
        log_prices[t] = log_prices[t-1] + theta * (mean_level - log_prices[t-1]) * dt + sigma * dW
    
    # Convert to prices
    prices = np.exp(log_prices[1:])
    
    # Create DataFrame
    df = pd.DataFrame({
        'close': prices,
        'log_price': log_prices[1:]
    })
    
    df['returns'] = df['close'].pct_change()
    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
    
    return df


def half_life(theta):
    """Calculate mean reversion half-life in days"""
    return np.log(2) / theta


def main():
    """Generate and save OU data"""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Generate OU synthetic data')
    parser.add_argument('--theta', type=float, default=0.10, help='Mean reversion speed')
    parser.add_argument('--sigma', type=float, default=0.10, help='Noise amplitude')
    parser.add_argument('--mean_level', type=float, default=4.605, help='Long-run mean (log space)')
    parser.add_argument('--years', type=int, default=15, help='Years to simulate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--output', type=str, default='data/synthetic/ou/ou_data.csv')
    
    args = parser.parse_args()
    
    # Generate data
    df = simulate_ou(
        theta=args.theta,
        sigma=args.sigma,
        mean_level=args.mean_level,
        years=args.years,
        seed=args.seed
    )
    
    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Generated OU data: {len(df)} bars")
    print(f"Mean reversion half-life: {half_life(args.theta):.1f} days")
    print(f"Saved to: {output_path}")
    print(f"\nSummary statistics:")
    print(f"  Mean price: ${df['close'].mean():.2f}")
    print(f"  Std price: ${df['close'].std():.2f}")
    print(f"  Mean daily return: {df['returns'].mean()*100:.4f}%")


if __name__ == '__main__':
    main()
