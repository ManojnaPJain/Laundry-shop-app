
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Laundry Shop API")


class OrderCreate(BaseModel):
    customer: str = Field(min_length=1)
    amount: float = Field(gt=0)


orders = []
next_id = 1


@app.get("/")
def home():
    return {"message": "Laundry Shop API is running"}


@app.get("/orders")
def get_orders():
    return orders


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    global next_id

    new_order = {
        "id": next_id,
        "customer": order.customer,
        "amount": order.amount,
        "status": "pending"
    }

    orders.append(new_order)
    next_id += 1

    return new_order


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )