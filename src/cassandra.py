import sqlite3
import pandas as pd
from time import time
from dataclasses import dataclass, field
from tabulate import tabulate
from pathlib import Path

from unidad import Unidad
from insumo import Insumo
from partida import Partida
from apu import APU


def timer(func):
    def wrap(*args, **kw):
        ts = time()
        result = func(*args, **kw)
        te = time()
        print(f"\n'{func.__name__}' took: {te-ts:2.4f} sec")
        return result
    return wrap


class SQLiteError(Exception):
    pass


class Unidad(Unidad):
    pass


class Insumo(Insumo):
    pass


class Partida(Partida):
    pass


class APU(APU):
    pass


@dataclass(eq=True, order=True)
class Database:

    name: str
    path: str = field(init=False)
    exists: bool = field(init=False)
    df: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.path = str(Path().resolve().parent.joinpath(
            'db', self.name + '.db'))
        self.exists = Path(self.path).is_file()

    def check(self):
        if not self.exists:
            values = {"y": True, "n": False}
            create = values[input(f'La base de datos "{
                                  self.name}" no existe. ¿Crear? [y/n]: ').lower()]
            if create:
                self.create()
            else:
                raise SQLiteError(f'La base de datos "{
                                  self.name}" no fue creada.')

    def create(self):
        try:
            conn = sqlite3.connect(self.path)
            conn.setconfig(1002)
            cursor = conn.cursor()
            sql = """
                CREATE TABLE "Unidades" (
                    "ID" INTEGER PRIMARY KEY,
                    "Nombre" TEXT UNIQUE,
                    "Code" TEXT UNIQUE
                );
            """
            cursor.execute(sql)
            sql = """
                CREATE TABLE "Rubros" (
                    "ID" INTEGER PRIMARY KEY,
                    "Nombre" TEXT UNIQUE,
                    "Code" TEXT UNIQUE
                );
            """
            cursor.execute(sql)
            sql = """
                INSERT INTO Rubros("Nombre", "Code")
                VALUES (?,?)
            """
            data = [
                ("Mano de Obra", "MO"),
                ("Materiales", "MA"),
                ("Equipos y Maquinaria", "EQ"),
                ("SubContratos", "SC")
            ]
            cursor.executemany(sql, data)
            sql = """
                CREATE TABLE "Monedas" (
                    "ID" INTEGER PRIMARY KEY,
                    "Nombre" TEXT UNIQUE,
                    "Code" TEXT UNIQUE
                );
            """
            cursor.execute(sql)
            sql = """
                INSERT INTO Monedas("Nombre", "Code")
                VALUES (?,?)
            """
            data = [
                ("Sol", "PEN"),
                ("Dólar Americano", "USD")
            ]
            cursor.executemany(sql, data)
            sql = """
                CREATE TABLE "Insumos" (
                	"ID" INTEGER PRIMARY KEY,
                	"Nombre" TEXT UNIQUE,
                	"Rubro" TEXT,
                	"Unidad" INTEGER,
                	"Precio" REAL,
                    "Moneda" INTEGER,
                    FOREIGN KEY("Unidad") REFERENCES "Unidades"("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
                    FOREIGN KEY("Rubro") REFERENCES "Rubros"("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
                    FOREIGN KEY("Moneda") REFERENCES "Monedas"("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
                );
            """
            cursor.execute(sql)
            sql = """
                CREATE TABLE "Partidas" (
                    "ID" INTEGER PRIMARY KEY,
                    "Nombre" TEXT UNIQUE,
                    "Unidad" TEXT,
                    "Metrado" REAL,
                    "Rendimiento" REAL,
                    FOREIGN KEY("Unidad") REFERENCES "Unidades"("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
                );
            """
            cursor.execute(sql)
            sql = """
                CREATE TABLE "APUs" (
                    "ID" INTEGER PRIMARY KEY,
                	"Partida" INTEGER NOT NULL,
                	"Insumo" INTEGER NOT NULL,
                	"Cantidad" REAL NOT NULL,
                    UNIQUE("Partida", "Insumo") ON CONFLICT ABORT
                    FOREIGN KEY("Partida") REFERENCES "Partidas"("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
                    FOREIGN KEY("Insumo") REFERENCES "Insumos"("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
                );
            """
            cursor.execute(sql)
            conn.commit()
        except sqlite3.Error as e:
            SQLiteError(e)
        finally:
            conn.close()

    # =XLOOKUP(lookup_value;lookup_array;return_array)
    def xlookup(self, table, lookup_value, lookup_column, return_column):
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            sql = f"""
                    SELECT {return_column}
                    FROM {table}
                    WHERE {lookup_column} = ?
                """
            cursor.execute(sql, [lookup_value])
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            raise SQLiteError(e)
        finally:
            conn.close()

    def get_column(self, table, column):
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            sql = f"""
                    SELECT {column}
                    FROM {table}
                """
            cursor.execute(sql)
            results = cursor.fetchall()
            array = [result[0] for result in results]
            return array
        except sqlite3.Error as e:
            raise SQLiteError(e)
        finally:
            conn.close()

    def select_ID(self, table):
        ID = self.get_column(table, 'ID')
        Nombre = self.get_column(table, 'Nombre')
        zipped = list(zip(ID, Nombre))
        print(tabulate(zipped, headers=['ID', 'Partida']))
        selection = int(input('Selecciona un ID: '))
        if selection in ID:
            return selection
        else:
            raise SQLiteError(f'"{selection}" no es un ID válido.')

    def to_df(self):
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            sql = """
                    SELECT Partida, Insumo, Cantidad
                    FROM APUs
                """
            cursor.execute(sql)
            results = cursor.fetchall()
            Partida = [result[0] for result in results]
            Rubro = map(lambda x: self.xlookup('Rubros', x, 'ID', 'Code'), [
                        self.xlookup('Insumos', result[1], 'ID', 'Rubro') for result in results])
            Insumo = [self.xlookup('Insumos', result[1], 'ID', 'Nombre')
                      for result in results]
            Unidad = map(lambda x: self.xlookup('Unidades', x, 'ID', 'Code'), [
                         self.xlookup('Insumos', result[1], 'ID', 'Unidad') for result in results])
            Cantidad = [result[2] for result in results]
            Precio = [self.xlookup('Insumos', result[1], 'ID', 'Precio')
                      for result in results]
        except sqlite3.Error as e:
            raise SQLiteError(e)
        finally:
            conn.close()
        data = {'Partida': Partida,
                'Rubro': Rubro,
                'Insumo': Insumo,
                'Unidad': Unidad,
                'Cantidad': Cantidad,
                'Precio': Precio}
        df = pd.DataFrame(data)
        df['Cantidad'] = df['Cantidad'].round(decimals=4)
        df['Precio'] = df['Precio'].round(decimals=2)
        Parcial = df.Precio * df.Cantidad
        df['Parcial'] = Parcial
        df['Parcial'] = df['Parcial'].round(decimals=2)
        return df

    def calculate_mo(self):
        ID = self.xlookup('Unidades', '%mo', 'Code', 'ID')
        mo_array = []
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            sql = """
                    SELECT ID
                    FROM APUs
                    WHERE Insumo = ?
                """
            cursor.execute(sql, [ID])
            results = cursor.fetchall()
            id_array = [result[0] for result in results]
            id_array = [x - 1 for x in id_array]
        except sqlite3.Error as e:
            raise SQLiteError(e)
        finally:
            conn.close()

        df = self.to_df()
        for ID in id_array:
            partida = df.iloc[ID, 0]
            df_by_partida = df[df['Partida'] == partida]
            df_by_mo = df_by_partida[df_by_partida['Rubro'] == 'MO']
            mo = df_by_mo['Parcial'].sum()
            mo = mo.item()  # converts np.int64 to float
            mo_array.append(mo)
        return id_array, mo_array

    # =REPLACE(lookup_value;lookup_array;replace_array;replace_value)
    def replace(self, table, lookup_value, lookup_column, replace_column, replace_value):
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            sql = f"""
                    UPDATE {table}
                    SET {replace_column} = ?
                    WHERE {lookup_column} = {lookup_value};
                """
            cursor.execute(sql, [replace_value])
            conn.commit()
        except sqlite3.Error as e:
            raise SQLiteError(e)
        finally:
            conn.close()

    def process_apu(self):
        id_array, mo_array = self.calculate_mo()
        df = self.to_df()
        for i, mo in enumerate(mo_array):
            df.iloc[id_array[i], 5] = round(mo, 4)
            df.iloc[id_array[i], 6] = round(mo*df.iloc[id_array[i], 4]/100, 2)
        return df

    def process_ppto(self):
        df = self.process_apu()
        parcial_sum = df.groupby('Partida')['Parcial'].sum()
        nombre_partidas = self.get_column('Partidas', 'Nombre')
        metrado_partidas = self.get_column('Partidas', 'Metrado')
        df = pd.DataFrame({'Partida': nombre_partidas,
                           'Metrado': metrado_partidas,
                           'Precio': parcial_sum})
        df['Precio'] = df['Precio'].round(decimals=2)
        df['Metrado'] = df['Metrado'].round(decimals=2)
        parcial = df.Precio * df.Metrado
        df['Parcial'] = parcial
        df['Parcial'] = df['Parcial'].round(decimals=2)
        return df
