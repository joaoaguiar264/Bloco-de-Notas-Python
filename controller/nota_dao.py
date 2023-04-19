import sqlite3
from model.nota import Nota
from datetime import datetime


class Database:
    def __init__(self, nome='system.db'):
        self.connection = None
        self.name = nome

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as ex:
            print(ex)

    def create_table_nota(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS nota(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                nota TEXT,
                data TEXT
            );
            """
        )
        self.close_connection()

    def registrar_nota(self, nota: Nota):
        self.connect()
        cursor = self.connection.cursor()
        campos_nota = ('titulo', 'nota', 'data')
        valores = f"'{nota.titulo}', '{str(nota.nota)}', '{nota.data}'"

        try:
            cursor.execute(
                f"""
                INSERT INTO nota {campos_nota}
                VALUES ({valores});
                """
            )
            self.connection.commit()
            return 'OK'
        except sqlite3.Error as ex:
            return ex
        finally:
            self.close_connection()

    def consultar_todas_notas(self):
        self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""
                SELECT * FROM nota
                """
            )
            return cursor.fetchall()
        except sqlite3.Error as ex:
            return None
        finally:
            self.close_connection()

    def deletar_nota(self, id):
        self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""
                DELETE FROM nota WHERE id = '{id}'
                """
            )
            self.connection.commit()
            return 'OK'
        except sqlite3.Error as ex:
            print(ex)
        finally:
            self.close_connection()

    def atualizar_nota(self, nota: Nota):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""UPDATE NOTA SET
            TITULO = '{nota.titulo}',
            nota = '{nota.nota}'
            WHERE ID = '{nota.id}'""")

            self.connection.commit()
            return 'OK'
        except sqlite3.Error as ex:
            print(ex)
        finally:
            self.close_connection()


