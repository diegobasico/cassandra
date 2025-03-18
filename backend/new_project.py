from sqlalchemy import Table, ForeignKey, Column, Integer, String, Float
import logging

import polars as pl
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

### set global variables ####

logging.basicConfig(
    filename="debug.log",
    filemode="a+",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

db_path = "data/database.db"
engine = create_engine(f"sqlite:///{db_path}", echo=True)
metadata = MetaData()
# metadata.reflect(bind=engine)


partidas_table = Table(
    "partidas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("item", String),
    Column("name", String),
    Column("pu", Float),
)

titulos_table = Table(
    "titulos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("item", String),
    Column("name", String),
)

insumos_table = Table(
    "insumos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("rubro_id", ForeignKey("rubros.id"), nullable=False),
    Column("moneda_id", ForeignKey("monedas.id")),
    Column("pu", Float),
)

apus_table = Table(
    "apus",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("partida_id", ForeignKey("partidas.id"), nullable=False),
    Column("insumo_id", ForeignKey("insumos.id"), nullable=False),
    Column("insumo_cantidad", Float),
)

rubros_table = Table(
    "rubros",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("code", String),
)

monedas_table = Table(
    "monedas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("code", String),
)


metadata.create_all(engine)
