import cassandra as cs
from tqdm import tqdm


def insert_test_values(database_name):

    db = cs.Database(database_name)
    db.check()

    unidades = [('Mano de Obra', '%mo'),
                ('Bolsa', 'bol'),
                ('Galón', 'gal'),
                ('Global', 'glb'),
                ('Hora Equipo', 'he'),
                ('Hora Hombre', 'hh'),
                ('Hora Máquina', 'hm'),
                ('Kilogramo', 'kg'),
                ('Metro Lineal', 'm'),
                ('Metro Cuadrado', 'm2'),
                ('Metro Cúbico', 'm3'),
                ('Mes', 'mes'),
                ('Pie Cuadrado', 'p2'),
                ('Par', 'par'),
                ('Plancha', 'pln'),
                ('Rollo', 'rll'),
                ('Unidad', 'und')]
    for unidad in tqdm(unidades, desc='Unidades'):
        cs.Unidad(db.name, unidad[0], unidad[1]).add()

    insumos = [('Herramientas Manuales', 'eq', '%mo', 0, 'pen'),
               ('Operario', 'mo', 'hh', 27.49, 'pen'),
               ('Oficial', 'mo', 'hh', 21.62, 'pen'),
               ('Peón', 'mo', 'hh', 19.57, 'pen'),
               ('Clavos', 'ma', 'kg', 3.90, 'pen'),
               ('Piedra', 'ma', 'm3', 42, 'pen'),
               ('Madera', 'ma', 'p2', 6.65, 'pen'),
               ('Gigantografía', 'ma', 'und', 345.60, 'pen'),
               ('Excavadora', 'eq', 'hm', 190, 'pen')]
    for insumo in tqdm(insumos, desc='Insumos'):
        cs.Insumo(db.name, insumo[0], insumo[1],
                  insumo[2], insumo[3], insumo[4]).add()

    partidas = [('Cartel de Identificación de la Obra', 'und', 1, 2),
                ('Corte de Terreno Natural', 'm3', 7567.42, 350)]
    for partida in tqdm(partidas, desc='Partidas'):
        cs.Partida(db.name, partida[0], partida[1],
                   partida[2], partida[3]).add()
    apus = [(1, 2, 1),
            (1, 3, 1),
            (1, 4, 1),
            (1, 5, 2),
            (1, 6, 0.5),
            (1, 7, 70),
            (1, 8, 1),
            (1, 1, 3),
            (2, 2, 1),
            (2, 4, 1),
            (2, 1, 3),
            (2, 9, 1)]
    for apu in tqdm(apus, desc='APUs'):
        cs.APU(database_name, apu[0], apu[1], apu[2],).add()


def insert_apus_manually(database_name):
    db = cs.Database(database_name)
    partidaID = db.select_ID('Partidas')
    insumoID = db.select_ID('Insumos')
    cantidad = float(input("Ingresa la cantidad del recurso: "))
    cs.APU(db.name, partidaID, insumoID, cantidad).add()


@cs.timer
def main():
    db = cs.Database('test')
    # db.check()
    # insert_test_values(db.name)
    apu = db.process_apu()
    print("\n", apu)
    ppto = db.process_ppto()
    print("\n", ppto)


if __name__ == '__main__':
    main()
