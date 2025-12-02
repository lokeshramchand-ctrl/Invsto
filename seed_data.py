import asyncio
import pandas as pd
from prisma import Prisma
from decimal import Decimal
from datetime import datetime

async def main():
    try:
        df = pd.read_csv('data.csv')
        print(f"Loaded {len(df)} rows from CSV.")
    except FileNotFoundError:
        print("Error: data.csv not found. Please export your Google Sheet to CSV.")
        return

    # 2. Connect to DB
    prisma = Prisma()
    await prisma.connect()

    # 3. Insert Data
    print("Inserting data... this may take a moment.")
    count = 0
    for _, row in df.iterrows():
       
        try:
            await prisma.stockdata.create(
                data={
                    "datetime": pd.to_datetime(row['datetime']), 
                    "open": Decimal(str(row['open'])),
                    "high": Decimal(str(row['high'])),
                    "low": Decimal(str(row['low'])),
                    "close": Decimal(str(row['close'])),
                    "volume": int(row['volume']),
                }
            )
            count += 1
        except Exception as e:
            print(f"Skipping row due to error: {e}")

    print(f"Successfully inserted {count} records.")
    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())