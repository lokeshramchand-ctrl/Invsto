import pandas as pd
from decimal import Decimal

def calculate_strategy(records):
    """
    Implements a Moving Average Crossover Strategy.
    Short Window: 10 periods
    Long Window: 50 periods
    """
    if not records:
        return {"error": "No data available"}

    # Convert Prisma objects to DataFrame
    data = [
        {
            "datetime": r.datetime,
            "close": float(r.close)  # Convert Decimal to float for pandas
        } 
        for r in records
    ]
    
    df = pd.DataFrame(data)
    df.sort_values('datetime', inplace=True)
    
    # Calculate Moving Averages
    df['SMA_Short'] = df['close'].rolling(window=10).mean()
    df['SMA_Long'] = df['close'].rolling(window=50).mean()
    
    # Generate Signals (1 = Buy, -1 = Sell, 0 = Hold)
    # Signal is 1 when Short > Long
    df['Signal'] = 0
    df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] = 1
    df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1
    
    # Detect Crossovers (where signal changes)
    df['Position'] = df['Signal'].diff()
    
    # Filter for buy/sell events
    buy_signals = df[df['Position'] == 2].shape[0]  # -1 to 1
    sell_signals = df[df['Position'] == -2].shape[0] # 1 to -1
    
    # Basic Performance Metric: Last Signal
    current_signal = "BUY" if df.iloc[-1]['Signal'] == 1 else "SELL"
    if df.iloc[-1]['Signal'] == 0:
        current_signal = "NEUTRAL"

    return {
        "strategy": "Moving Average Crossover (10/50)",
        "total_records": len(df),
        "buy_signals_count": buy_signals,
        "sell_signals_count": sell_signals,
        "current_market_position": current_signal,
        "last_close_price": df.iloc[-1]['close'],
        "sma_short_last": df.iloc[-1]['SMA_Short'],
        "sma_long_last": df.iloc[-1]['SMA_Long']
    }