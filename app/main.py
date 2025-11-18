from fastapi import FastAPI
from app.api import routes_users, routes_bodega
from app.db.database import Base, engine
from app.models import producto_model

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi primera API con FastAPI")

# Registrar rutas
app.include_router(routes_users.router)
app.include_router(routes_bodega.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a mi API 🚀"}