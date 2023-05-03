from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime


class Nota(Base):
    __tablename__ = 'nota'

    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String(100), nullable=False)
    nota = Column(String(100), nullable=False)
    data = Column(String(100), nullable=False)


    def __repr__(self):
        return f'Titulo da nota = {self.titulo}, id = {self.id}'
