import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class TipoDireccion(str, enum.Enum):
    FACTURACION = "FACTURACIÓN"
    ENVIO = "ENVÍO"


class Client(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    razon_social = Column(String, index=True)
    nombre_comercial = Column(String, index=True)
    rfc = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)

    domicilios = relationship(
        "Domicilio", back_populates="cliente", cascade="all, delete-orphan"
    )


class Domicilio(Base):
    __tablename__ = "domicilios"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    domicilio = Column(String)
    colonia = Column(String)
    municipio = Column(String)
    estado = Column(String)
    tipo_de_direccion = Column(Enum(TipoDireccion), default=TipoDireccion.FACTURACION)

    cliente = relationship("Client", back_populates="domicilios")
