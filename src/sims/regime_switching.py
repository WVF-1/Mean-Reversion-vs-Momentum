"""Regime-switching model simulation"""

import numpy as np
import pandas as pd
from src.utils import set_seed, trading_days_per_year, annual_to_daily


def simulate_regime_switching(
    trend_mu=0.06,
    trend_sigma=0.18,
    ou_theta=0.08,
    ou_sigma=0.12,
    p_trend_to_range=0.03,
    p_range_to_trend=0.05,
    years=15,
    start_price=100,
    seed=None
):
    """
    Simulate two-state regime-switching model
    
    States:
    - 0: Trending (GBM-like)
    - 1: Mean-reverting (OU-like)
    
    Parameters:
    -----------
    trend_mu : float
        Annual drift in trending regime
    trend_sigma : float
        Annual volatility in trending regime
    ou_theta : float
        Mean reversion speed in range-bound regime
    ou_sigma : float
        Noise amplitude in range-bound regime
    p_trend_to_range : float
        Probability of switching from trend to range
    p_range_to_trend : float
        Probability of switching from range to trend
    years : int
        Number of years to simulate
    start_price : float
        Initial price
    seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame with columns: ['close', 'returns', 'log_returns', 'regime']
    """
    if seed is not None:
        set_seed(seed)
    
    # Time parameters
    dt = 1 / trading_days_per_year()
    n_steps = int(years * trading_days_per_year())
    
    # Convert trend parameters to daily
    trend_mu_daily = annual_to_daily(trend_mu, is_return=True)
    trend_sigma_daily = annual_to_daily(trend_sigma, is_return=False)
    
    # Initialize arrays
    log_prices = np.zeros(n_steps + 1)
    log_prices[0] = np.log(start_price)
    regimes = np.zeros(n_steps, dtype=int)
    
    # Start in trending regime
    current_regime = 0
    
    # Calculate initial mean level for OU
    mean_level = log_prices[0]
    
    # Transition matrix
    P = np.array([
        [1 - p_trend_to_range, p_trend_to_range],
        [p_range_to_trend, 1 - p_range_to_trend]
    ])
    
    # Simulate
    for t in range(n_steps):
        # Record regime
        regimes[t] = current_regime
        
        # Generate shock
        dW = np.random.normal(0, np.sqrt(dt))
        
        if current_regime == 0:
            # Trending regime (GBM)
            drift = trend_mu_daily * dt
            diffusion = trend_sigma_daily * dW
            log_prices[t+1] = log_prices[t] + drift + diffusion
            
        else:
            # Mean-reverting regime (OU)
            # Update mean level periodically to avoid drift
            if t % 50 == 0:
                mean_level = log_prices[t]
            
            reversion = ou_theta * (mean_level - log_prices[t]) * dt
            diffusion = ou_sigma * dW
            log_prices[t+1] = log_prices[t] + reversion + diffusion
        
        # Regime transition
        if np.random.random() < P[current_regime, 1 - current_regime]:
            current_regime = 1 - current_regime
    
    # Convert to prices
    prices = np.exp(log_prices[1:])
    
    # Create DataFrame
    df = pd.DataFrame({
        'close': prices,
        'regime': regimes,
        'log_price': log_prices[1:]
    })
    
    df['returns'] = df['close'].pct_change()
    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
    
    return df


def main():
    """Generate and save regime-switching data"""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Generate regime-switching synthetic data')
    parser.add_argument('--trend_mu', type=float, default=0.06)
    parser.add_argument('--trend_sigma', type=float, default=0.18)
    parser.add_argument('--ou_theta', type=float, default=0.08)
    parser.add_argument('--ou_sigma', type=float, default=0.12)
    parser.add_argument('--p_trend_to_range', type=float, default=0.03)
    parser.add_argument('--p_range_to_trend', type=float, default=0.05)
    parser.add_argument('--years', type=int, default=15)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=str, default='data/synthetic/markov_regime/regime_data.csv')
    
    args = parser.parse_args()
    
    # Generate data
    df = simulate_regime_switching(
        trend_mu=args.trend_mu,
        trend_sigma=args.trend_sigma,
        ou_theta=args.ou_theta,
        ou_sigma=args.ou_sigma,
        p_trend_to_range=args.p_trend_to_range,
        p_range_to_trend=args.p_range_to_trend,
        years=args.years,
        seed=args.seed
    )
    
    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    # Calculate regime statistics
    trend_days = (df['regime'] == 0).sum()
    range_days = (df['regime'] == 1).sum()
    
    print(f"Generated regime-switching data: {len(df)} bars")
    print(f"Saved to: {output_path}")
    print(f"\nRegime distribution:")
    print(f"  Trending days: {trend_days} ({trend_days/len(df)*100:.1f}%)")
    print(f"  Range-bound days: {range_days} ({range_days/len(df)*100:.1f}%)")
    print(f"\nSummary statistics:")
    print(f"  Final price: ${df['close'].iloc[-1]:.2f}")
    print(f"  Mean daily return: {df['returns'].mean()*100:.4f}%")


if __name__ == '__main__':
    main()
