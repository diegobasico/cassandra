import sqlite3
import cassandra as cs
from dataclasses import dataclass, field


@dataclass(eq=True, order=True)
class Unidad:
    database: str
    nombre: str
    code: str
    dbpath: str = field(init=False)
    dbexists: str = field(init=False)

    def __post_init__(self):
        db = cs.Database(self.database)
        self.dbpath = db.path
        self.dbexists = db.exists

    def add(self):

        if not self.dbexists:
            raise cs.SQLiteError('La base de datos no existe.')

        try:
            conn = sqlite3.connect(self.dbpath)
            conn.setconfig(1002)
            cursor = conn.cursor()
            sql = """
                INSERT INTO Unidades("Nombre", "Code")
                VALUES (?,?)
            """
            cursor.execute(sql, (self.nombre, self.code))
            conn.commit()
        except sqlite3.Error as e:
            if "UNIQUE constraint failed" in str(e):
                raise cs.SQLiteError(f'La unidad "{self.nombre}" ya existe.')
            else:
                raise cs.SQLiteError(e)
        finally:
            conn.close()