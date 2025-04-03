import polars as pl
import numpy as np

from typing import List
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
    table: List[List]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Hello there, General Kenobi."}


@app.post("/response")
async def get_response(item: Item):
    print(item)


@app.post("/test")
async def get_test(data: Test):
    print(data)


@app.post("/ppto")
async def get_ppto(ppto: Hot):
    matrix = np.matrix(ppto.table).transpose().tolist()
    df = pl.DataFrame(
        matrix,
        schema={
            "Level": pl.Int32,
            "Tipo": pl.String,
            "Item": pl.String,
            "Descripción": pl.String,
            "Unidad": pl.String,
            "Metrado": pl.Float32,
            "Precio": pl.Float32,
            "Parcial": pl.String,
        },
    )
    df = df.with_columns(
        (pl.col("Metrado") * pl.col("Precio")).alias("Parcial"),
    )
    print(df)
