import sqlite3
import pandas as pd
from tqdm import tqdm


def table_to_df(cursor, table):
    query = f"""
        SELECT * FROM {table};
    """
    cursor.execute(query)

    df = pd.DataFrame(
        cursor.fetchall(),
        columns=[description[0] for description in cursor.description],
    ).set_index("ID")

    return df


def find_children(cursor, table_name, primary_key_column, parent_id_column, start_row_id):
    query = f"""
        WITH RECURSIVE ChildHierarchy AS (
        SELECT {primary_key_column}, {parent_id_column}, 1 AS depth
        FROM {table_name}
        WHERE {primary_key_column} = {start_row_id}

        UNION ALL

        SELECT t.{primary_key_column}, t.{parent_id_column}, c.depth + 1
        FROM {table_name} t
        JOIN ChildHierarchy c ON c.{primary_key_column} = t.{parent_id_column}
        )

        SELECT t.{primary_key_column}, t.{parent_id_column}, t.depth
        FROM ChildHierarchy t
        WHERE t.{primary_key_column} != {start_row_id};
    """

    cursor.execute(query)
    result = cursor.fetchall()
    return result


def main():

    db = r"database\dummy.db"

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        table = "Títulos"  # working table

        df = table_to_df(cursor, table)
        df["Predecessor"] = df["Predecessor"].fillna(0).astype(int)
        df = df.sort_values(by="Predecessor")
        empty_predecessor_counter = 0  # empty_predecessor = título sin predecesor

        for index in tqdm(df.index):
            if df.at[index, "Predecessor"] == 0:
                empty_predecessor_counter = empty_predecessor_counter + 1
                df.at[index, "ID_Visible"] = str(empty_predecessor_counter).zfill(2)
                df.at[index, "ID_GUI"] = str(empty_predecessor_counter).zfill(2)
                df.at[index, "Ruta_Título"] = df.at[index, "Título"]

            result = find_children(cursor, table, "ID", "Predecessor", index)

            for r_index, (ID, parent, depth) in enumerate(result):
                if parent == index:
                    df.at[ID, "ID_Visible"] = df.at[index,
                                                    "ID_Visible"] + str(r_index + 1).zfill(2)
                    df.at[ID, "ID_GUI"] = df.at[index, "ID_GUI"] + "." + str(r_index + 1).zfill(2)
                    df.at[ID, "Ruta_Título"] = df.at[index, "Ruta_Título"] + ";" + df.at[ID, "Título"]

        df = df.sort_index()
        df["Predecessor"] = df["Predecessor"].replace(0, pd.NA)

        df = df.sort_values(by="ID_Visible")

        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=True,
            dtype={"ID": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"},
        )

        conn.commit()
        cursor.close()


if __name__ == "__main__":
    main()