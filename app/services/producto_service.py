from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.producto_model import Producto
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate

class ProductoService:
    @staticmethod
    def get_all_productos(db: Session):
        """Obtiene todos los productos de la BD"""
        return db.query(Producto).all()

    @staticmethod
    def get_producto_by_id(db: Session, id_producto: int):
        """Obtiene un producto por ID"""
        producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto con ID {id_producto} no existe")
        return producto

    @staticmethod
    def get_producto_by_sku(db: Session, sku: str):
        """Obtiene un producto por SKU"""
        producto = db.query(Producto).filter(Producto.sku == sku).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto con SKU {sku} no existe")
        return producto

    @staticmethod
    def create_producto(db: Session, producto_data: ProductoCreate):
        """Crea un nuevo producto en la BD"""
        # Validar SKU único
        if producto_data.sku:
            existing = db.query(Producto).filter(Producto.sku == producto_data.sku).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"SKU {producto_data.sku} ya existe")
        
        db_producto = Producto(**producto_data.dict())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto

    @staticmethod
    def update_producto(db: Session, id_producto: int, producto_data: ProductoUpdate):
        """Actualiza un producto existente"""
        producto = ProductoService.get_producto_by_id(db, id_producto)
        
        # Validar SKU único si se proporciona uno nuevo
        if producto_data.sku and producto_data.sku != producto.sku:
            existing = db.query(Producto).filter(Producto.sku == producto_data.sku).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"SKU {producto_data.sku} ya existe")
        
        # Actualizar solo los campos proporcionados
        update_data = producto_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(producto, field, value)
        
        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def delete_producto(db: Session, id_producto: int):
        """Elimina un producto"""
        producto = ProductoService.get_producto_by_id(db, id_producto)
        db.delete(producto)
        db.commit()
        return {"message": f"Producto {id_producto} eliminado exitosamente"}

    @staticmethod
    def disminuir_stock(db: Session, id_producto: int, cantidad: int):
        """Disminuye el stock de un producto"""
        producto = ProductoService.get_producto_by_id(db, id_producto)
        
        if cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")
        
        if cantidad > producto.existencias:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Disponible: {producto.existencias}, solicitado: {cantidad}"
            )
        
        producto.existencias -= cantidad
        db.commit()
        db.refresh(producto)
        return {
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "cantidad_restada": cantidad,
            "existencias_actuales": producto.existencias
        }

    @staticmethod
    def aumentar_stock(db: Session, id_producto: int, cantidad: int):
        """Aumenta el stock de un producto"""
        producto = ProductoService.get_producto_by_id(db, id_producto)
        
        if cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")
        
        producto.existencias += cantidad
        db.commit()
        db.refresh(producto)
        return {
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "cantidad_agregada": cantidad,
            "existencias_actuales": producto.existencias
        }
