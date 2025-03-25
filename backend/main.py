import polars as pl

from typing import Any, List

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class Item(BaseModel):
    name: str
    price: float
    quantity: int


class Test(BaseModel):
    text: str


class Hot(BaseModel):
    table: List


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pl.DataFrame({
    "ID": [1, 2, 3],
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 22],
})


@app.get("/")
def home():
    return {"message": "Hello there, General Kenobi."}


@app.get("/data")
def get_data():
    return df.to_dicts()


@app.post("/response")
async def get_response(item: Item):
    print(item)


@app.post("/test")
async def get_test(data: Test):
    print(data)


@app.post("/ppto")
async def get_ppto(ppto: Hot):
    print(ppto)
