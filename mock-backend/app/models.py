from datetime import datetime

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    item: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    customer_id: int = Field(gt=0)


class OrderResponse(BaseModel):
    order_id: str
    status: str
    item: str
    amount: float
    customer_id: int
    created_at: datetime
