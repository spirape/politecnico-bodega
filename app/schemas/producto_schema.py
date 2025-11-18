from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    precio: Decimal = Field(..., decimal_places=2, ge=0)
    existencias: int = Field(default=0, ge=0)
    sku: Optional[str] = Field(None, max_length=100)

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(None, decimal_places=2, ge=0)
    existencias: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, max_length=100)

class ProductoResponse(ProductoBase):
    id_producto: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class DisminuirStock(BaseModel):
    cantidad: int = Field(..., gt=0, description="Cantidad a disminuir (debe ser > 0)")
