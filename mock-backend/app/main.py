import os
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException, status

from .kafka_producer import send_order_to_kafka
from .models import OrderCreate, OrderResponse

app = FastAPI(title="Ozon-like Order System", version="1.0.0")
orders_db: dict[str, dict] = {}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/order", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    order_id = str(uuid.uuid4())
    order_data = {
        "order_id": order_id,
        "status": "created",
        "item": order.item,
        "amount": order.amount,
        "customer_id": order.customer_id,
        "created_at": datetime.now(),
    }
    orders_db[order_id] = order_data
    send_order_to_kafka(order_data)
    return order_data


@app.get("/order/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]


@app.get("/orders", response_model=list[OrderResponse])
def get_orders():
    return list(orders_db.values())


@app.delete("/order/{order_id}")
def delete_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    del orders_db[order_id]
    return {"order_id": order_id, "status": "deleted"}
