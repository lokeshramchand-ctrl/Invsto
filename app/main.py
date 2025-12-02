from fastapi import FastAPI, HTTPException
from prisma import Prisma
from typing import List
from contextlib import asynccontextmanager
from app.models import StockDataCreate, StockDataResponse
from app.strategy import calculate_strategy

prisma = Prisma()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "ok", "docs": "/docs"}

@app.get("/data", response_model=List[StockDataResponse])
async def get_data():
    return await prisma.stockdata.find_many(order={"datetime": "asc"})

@app.post("/data", response_model=StockDataResponse)
async def create_data(record: StockDataCreate):
    try:
        new_record = await prisma.stockdata.create(
            data={
                "datetime": record.datetime,
                "open": record.open,
                "high": record.high,
                "low": record.low,
                "close": record.close,
                "volume": record.volume,
            }
        )
        return new_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/strategy/performance")
async def get_strategy_performance():
    # Fetch all data for strategy calculation
    records = await prisma.stockdata.find_many(order={"datetime": "asc"})
    
    if len(records) < 50:
        return {"message": "Not enough data points to calculate 50-period moving average."}
        
    result = calculate_strategy(records)
    return result