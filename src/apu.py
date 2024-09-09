import sqlite3
import cassandra as cs
from dataclasses import dataclass, field


@dataclass(eq=True, order=True)
class APU:

    # rubro, unidad y moneda se ingresan por ID. Ej: (test, 1, 2, 66.90)
    # la cantidad es cuadrilla si la unidad es hh o hm
    database: str
    partida_ID: int
    insumo_ID: int
    cantidad: float
    cuadrilla: float = field(init=False)
    dbpath: str = field(init=False)
    partida_nombre: str = field(init=False)
    insumo_nombre: str = field(init=False)
    insumo_unidad_code: str = field(init=False)

    def __post_init__(self):
        db = cs.Database(self.database)
        self.dbpath = db.path
        self.dbexists = db.exists
        self.rendimiento = db.xlookup('Partidas', self.partida_ID, 'ID', 'Rendimiento')
        self.insumo_unidad_ID = db.xlookup('Insumos', self.insumo_ID, 'ID', 'Unidad')
        self.insumo_unidad_code = db.xlookup('Unidades', self.insumo_unidad_ID, 'ID', 'Code')
        if self.insumo_unidad_code == 'hh' or self.insumo_unidad_code == 'hm':
            self.cuadrilla = self.cantidad
            self.cantidad = self.cuadrilla*8/self.rendimiento
        self.partida_nombre = db.xlookup('Partidas', self.partida_ID, 'ID', 'Nombre')
        self.insumo_nombre = db.xlookup('Insumos', self.insumo_ID, 'ID', 'Nombre')

    def add(self):

        if not self.dbexists:
            raise cs.SQLiteError('La base de datos no existe.')

        try:
            conn = sqlite3.connect(self.dbpath)
            conn.setconfig(1002)
            cursor = conn.cursor()
            sql = """
                INSERT INTO APUs("Partida", "Insumo", "Cantidad")
                VALUES (?,?,?)
            """
            cursor.execute(sql, (self.partida_ID, self.insumo_ID, self.cantidad))
            conn.commit()
        except sqlite3.Error as e:
            if "UNIQUE constraint failed" in str(e):
                raise cs.SQLiteError(f'El insumo "{self.insumo_nombre}" ya existe en la partida "{self.partida_nombre}".')
            else:
                raise cs.SQLiteError(e)
        finally:
            conn.close()