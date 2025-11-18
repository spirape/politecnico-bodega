from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP, func
from app.db.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    existencias = Column(Integer, nullable=False, default=0)
    sku = Column(String(100), unique=True, nullable=True, index=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_actualizacion = Column(TIMESTAMP, nullable=True, onupdate=func.now())

    def __repr__(self):
        return f"<Producto(id={self.id_producto}, nombre={self.nombre})>"
