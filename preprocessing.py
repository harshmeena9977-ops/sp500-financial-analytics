import pandas as pd
import numpy as np

def load_and_clean_data(filepath):
    """Loads the S&P 500 dataset, parses dates, and handles missing values."""
    print("Loading dataset...")
    df = pd.read_csv(filepath)
    
    # Parse date and sort chronologically per symbol
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['symbol', 'date']).reset_index(drop=True)
    
    # Handle missing values using modern ffill grouped by stock symbol
    for col in ['open', 'high', 'low']:
        df[col] = df.groupby('symbol')[col].transform(lambda x: x.ffill())
        
    print(f"Data cleaned successfully. Shape: {df.shape}")
    return df

def add_technical_indicators(df):
    """Engineers standard financial features: returns, moving averages, and volatility."""
    print("Engineering technical features...")
    
    # Daily percentage return
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()
    
    # Moving Averages (20-day and 50-day)
    df['sma_20'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(window=20).mean())
    df['sma_50'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(window=50).mean())
    
    # Rolling Volatility (20-day standard deviation of returns)
    df['volatility_20'] = df.groupby('symbol')['daily_return'].transform(lambda x: x.rolling(window=20).std())
    
    # Target Variable: Next day direction (1 if price goes up, 0 if down)
    df['next_close'] = df.groupby('symbol')['close'].shift(-1)
    df['target'] = (df['next_close'] > df['close']).astype(int)
    
    return df

if __name__ == "__main__":
    # Execute pipeline
    file_path = "S&P 500 Stock Prices 2014-2017.csv"
    raw_df = load_and_clean_data(file_path)
    processed_df = add_technical_indicators(raw_df)
    
    # Save processed dataframe for modeling
    processed_df.to_csv("sp500_processed.csv", index=False)
    print("Processed data saved to 'sp500_processed.csv'.")