import sqlite3
import cassandra as cs
from dataclasses import dataclass, field


@dataclass(eq=True, order=True)
class Insumo:

    # rubro, unidad y moneda se ingresan por código. Ej: (test, mano de obra, mo, hh, 21.12, pen)
    database: str
    nombre: str
    rubro_code: str
    unidad_code: str
    precio: float
    moneda_code: str
    dbpath: str = field(init=False)
    unidad_ID: int = field(init=False)
    rubro_ID: int = field(init=False)
    moneda_ID: int = field(init=False)

    def __post_init__(self):
        db = cs.Database(self.database)
        self.dbpath = db.path
        self.dbexists = db.exists
        self.unidad_ID = db.xlookup('Unidades',self.unidad_code,'Code', 'ID')
        self.rubro_ID = db.xlookup('Rubros', self.rubro_code.upper(), 'Code', 'ID')
        self.moneda_ID = db.xlookup('Monedas', self.moneda_code.upper(), 'Code', 'ID')

    def add(self):

        if not self.dbexists:
            raise cs.SQLiteError('La base de datos no existe.')

        try:
            conn = sqlite3.connect(self.dbpath)
            conn.setconfig(1002)
            cursor = conn.cursor()
            sql = """
                INSERT INTO Insumos("Nombre", "Rubro", "Unidad", "Precio", "Moneda")
                VALUES (?,?,?,?,?)
            """
            cursor.execute(sql, (self.nombre, self.rubro_ID, self.unidad_ID, self.precio, self.moneda_ID))
            conn.commit()
        except sqlite3.Error as e:
            if "UNIQUE constraint failed" in str(e):
                raise cs.SQLiteError(f'El insumo "{self.nombre}" ya existe.')
            else:
                raise cs.SQLiteError(e)
        finally:
            conn.close()