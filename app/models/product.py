from sqlalchemy import Column, Integer, String, Float
from app.db import Base


class Product(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    unidad_de_medida = Column(String)
    precio_base = Column(Float)
