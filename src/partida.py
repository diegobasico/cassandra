import sqlite3
import cassandra as cs
from dataclasses import dataclass, field


@dataclass(eq=True, order=True)
class Partida:

    # rubro, unidad y moneda se ingresan por código. Ej: (test, carpeta, m2, 21.12, 13.31)
    database: str
    nombre: str
    unidad_code: str
    metrado: float
    rendimiento: float
    dbpath: str = field(init=False)
    unidad_ID: int = field(init=False)

    def __post_init__(self):
        db = cs.Database(self.database)
        self.dbpath = db.path
        self.dbexists = db.exists
        self.unidad_ID = db.xlookup('Unidades', self.unidad_code, 'Code', 'ID')

    def add(self):

        if not self.dbexists:
            raise cs.SQLiteError('La base de datos no existe.')

        try:
            conn = sqlite3.connect(self.dbpath)
            conn.setconfig(1002)
            cursor = conn.cursor()
            sql = """
                INSERT INTO Partidas("Nombre", "Unidad", "Metrado", "Rendimiento")
                VALUES (?,?,?,?)
            """
            cursor.execute(sql, (self.nombre, self.unidad_ID,
                           self.metrado, self.rendimiento))
            conn.commit()
        except sqlite3.Error as e:
            if "UNIQUE constraint failed" in str(e):
                raise cs.SQLiteError(f'La partida "{self.nombre}" ya existe.')
            else:
                raise cs.SQLiteError(e)
        finally:
            conn.close()
