from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.producto_service import ProductoService
from app.schemas.producto_schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
    DisminuirStock
)

router = APIRouter(prefix="/bodega", tags=["Bodega"])

@router.get("/productos", response_model=list[ProductoResponse])
def get_productos(db: Session = Depends(get_db)):
    """Devuelve todos los productos de la base de datos"""
    return ProductoService.get_all_productos(db)

@router.get("/productos/{id_producto}", response_model=ProductoResponse)
def get_producto(id_producto: int, db: Session = Depends(get_db)):
    """Devuelve los detalles de un producto específico"""
    return ProductoService.get_producto_by_id(db, id_producto)

@router.post("/productos", response_model=ProductoResponse, status_code=201)
def create_producto(producto_data: ProductoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo producto en la base de datos"""
    return ProductoService.create_producto(db, producto_data)

@router.put("/productos/{id_producto}", response_model=ProductoResponse)
def update_producto(
    id_producto: int,
    producto_data: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un producto existente"""
    return ProductoService.update_producto(db, id_producto, producto_data)

@router.delete("/productos/{id_producto}")
def delete_producto(id_producto: int, db: Session = Depends(get_db)):
    """Elimina un producto de la base de datos"""
    return ProductoService.delete_producto(db, id_producto)

@router.post("/productos/{id_producto}/disminuir")
def disminuir_stock(
    id_producto: int,
    datos: DisminuirStock,
    db: Session = Depends(get_db)
):
    """Disminuye el stock de un producto"""
    return ProductoService.disminuir_stock(db, id_producto, datos.cantidad)

@router.post("/productos/{id_producto}/aumentar")
def aumentar_stock(
    id_producto: int,
    datos: DisminuirStock,
    db: Session = Depends(get_db)
):
    """Aumenta el stock de un producto"""
    return ProductoService.aumentar_stock(db, id_producto, datos.cantidad)