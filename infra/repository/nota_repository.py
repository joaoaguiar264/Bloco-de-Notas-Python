from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota

class NotaRepository:
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

    def select(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).filter(Nota.id == id).first()
            return data

    def insert(self, titulo, nota, data):
        with DBConnectionHandler() as db:
            data_insert = Nota(titulo=titulo, nota=nota, data=data)
            db.session.add(data_insert)
            db.session.commit()

    def delete(self, id):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id).delete()
            db.session.commit()

    def update(self, id, titulo, nota):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id).update({'titulo' : titulo, 'nota' : nota})
            db.session.commit()
