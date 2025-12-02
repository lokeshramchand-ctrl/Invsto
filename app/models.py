from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal

class StockDataCreate(BaseModel):
    datetime: datetime
    open: Decimal = Field(..., gt=0, description="Opening price must be positive")
    high: Decimal = Field(..., gt=0)
    low: Decimal = Field(..., gt=0)
    close: Decimal = Field(..., gt=0)
    volume: int = Field(..., ge=0, description="Volume cannot be negative")

    @field_validator('low')
    def validate_low(cls, v, values):
        if 'high' in values.data and v > values.data['high']:
            raise ValueError('Low price cannot be greater than High price')
        return v

class StockDataResponse(StockDataCreate):
    id: int
    
    class Config:
        from_attributes = True